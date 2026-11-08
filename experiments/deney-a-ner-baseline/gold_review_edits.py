"""Record of the gold review: which candidate rows were corrected and how.

Run once after select_gold.py; writes data/synthetic/gold_corrections.json (full corrected
entity/relation lists for each edited row) and data/synthetic/gold_ids.txt (all reviewed
candidates). The review was done by Claude (Opus 5.5), not by a human annotator.
Each edit is expressed as a delta on the original labels so it can be audited.
"""
import json

from common import DATA, GOLD_CORRECTIONS, GOLD_IDS, RAW_CSV, read_csv

E = lambda t, l: {"text": t, "label": l}
R = lambda h, t, tl: {"head": h, "type": t, "tail": tl}

EDITS = {
    "BAKIM-004": dict(note="Zincirde su sızıntısı → pano atması → karartma halkası eksikti.",
        add_rel=[R("su aşağıdaki koridora sızdı", "CAUSES", "masaj odaları karardı")]),
    "BAKIM-006": dict(note="Usta müdahalesi ACTION olarak etiketlenmemişti.",
        add_ent=[E("usta geldi baktı", "ACTION")],
        add_rel=[R("klima yine bozuldu", "ADDRESSED_BY", "usta geldi baktı")]),
    "BAKIM-008": dict(note="Asıl kök neden (kondenserde kireç) etiketlenmemişti.",
        add_ent=[E("kondenser borularında kireç var", "ROOT_CAUSE")],
        add_rel=[R("kondenser borularında kireç var", "CAUSES", "soğutma kapasitesi düştü")]),
    "BAKIM-039": dict(note="Olayın gerçekleştiği departman (HK'da) bağlanmamıştı.",
        add_rel=[R("82'ye geriledi", "OCCURS_IN", "HK")]),
    "BAKIM-066": dict(note="Zincir eksikti; 'kanallar gelmedi' Ön Büro'da değil odalarda oldu, Ön Büro'daki olay telefon yoğunluğu.",
        add_ent=[E("kanal listesini kaybetti", "EVENT"), E("telefonlarla boğuştu", "EVENT")],
        del_rel=[R("güncelleme", "CAUSES", "kanallar gelmedi"), R("kanallar gelmedi", "OCCURS_IN", "Ön Büro")],
        add_rel=[R("güncelleme", "CAUSES", "kanal listesini kaybetti"),
                 R("kanal listesini kaybetti", "CAUSES", "kanallar gelmedi"),
                 R("kanallar gelmedi", "CAUSES", "telefonlarla boğuştu"),
                 R("telefonlarla boğuştu", "OCCURS_IN", "Ön Büro")]),
    "DENETIM-008": dict(note="'DÖF açıldı' aksiyonu etiketlenmemişti.",
        add_ent=[E("DÖF açıldı", "ACTION")],
        add_rel=[R("porsiyon standardı eğitimi eksikliği", "ADDRESSED_BY", "DÖF açıldı")]),
    "DENETIM-027": dict(note="Zincirin son halkası (revire götürülme) eksikti.",
        add_ent=[E("revire götürüldü", "EVENT")],
        add_rel=[R("fıstıklı ikram yedi", "CAUSES", "revire götürüldü")]),
    "DENETIM-032": dict(note="Zincirin sonucu (hijyen puanının düşmesi) EVENT olarak yoktu.",
        add_ent=[E("hijyen puanı sınırın altına indi", "EVENT")],
        add_rel=[R("klor dağılımı bozuldu", "CAUSES", "hijyen puanı sınırın altına indi")]),
    "DENETIM-040": dict(note="Zincirin sonucu (memnuniyet puanının düşmesi) EVENT olarak yoktu.",
        add_ent=[E("memnuniyet puanı düştü", "EVENT")],
        add_rel=[R("misafirler başka otele yönlendirildi", "CAUSES", "memnuniyet puanı düştü")]),
    "DENETIM-041": dict(note="FO (Front Office) kısaltması departman olarak etiketlenmemişti.",
        add_ent=[E("FO", "DEPARTMENT")]),
    "DENETIM-049": dict(note="'Resepsiyon' departmanı etiketlenmemişti.",
        add_ent=[E("Resepsiyon", "DEPARTMENT")]),
    "DENETIM-063": dict(note="Asansör ve ara olay eksikti; OCCURS_IN yanlış olaya bağlıydı.",
        add_ent=[E("Asansör", "EQUIPMENT"), E("periyodik kontrolleri yapamadı", "EVENT")],
        del_rel=[R("bakım sözleşmesinin süresi dolduğundan", "CAUSES", "iki kat servis dışı kaldı"),
                 R("iki kat servis dışı kaldı", "OCCURS_IN", "Teknik Servis")],
        add_rel=[R("bakım sözleşmesinin süresi dolduğundan", "CAUSES", "periyodik kontrolleri yapamadı"),
                 R("periyodik kontrolleri yapamadı", "CAUSES", "iki kat servis dışı kaldı"),
                 R("periyodik kontrolleri yapamadı", "OCCURS_IN", "Teknik Servis")]),
    "DENETIM-068": dict(note="'Spa' departmanı etiketlenmemişti.",
        add_ent=[E("Spa", "DEPARTMENT")],
        add_rel=[R("süresi dolmuş belgeyle çalışırken yakalandı", "OCCURS_IN", "Spa")]),
    "DOF-015": dict(note="İkinci neden (eşzamanlı jeneratör testi) etiketlenmemişti.",
        add_ent=[E("jeneratör testi yapılıyordu", "ROOT_CAUSE")],
        add_rel=[R("jeneratör testi yapılıyordu", "CAUSES", "40 dakika geç ulaştı")]),
    "DOF-045": dict(note="F&B'deki olayın departman bağlantısı eksikti.",
        add_rel=[R("yanlış kişi sayısıyla hazırlık yaptı", "OCCURS_IN", "F&B")]),
    "SIKAYET-013": dict(note="Zincirin ara halkası (tavanı ıslattı) eksikti.",
        add_ent=[E("tavanı ıslattı", "EVENT")],
        del_rel=[R("Su kaçağı", "CAUSES", "halı koktu")],
        add_rel=[R("Su kaçağı", "CAUSES", "tavanı ıslattı"), R("tavanı ıslattı", "CAUSES", "halı koktu")]),
    "SIKAYET-027": dict(note="İkinci sonuç (valizin karışması) etiketlenmemişti.",
        add_ent=[E("valizim karışmıştı", "EVENT")],
        add_rel=[R("odamıza yetkisiz biri girmiş", "CAUSES", "valizim karışmıştı")]),
    "SIKAYET-052": dict(note="Olayın gerçekleştiği departman (HK) bağlanmamıştı.",
        add_rel=[R("4 saat olmuş", "OCCURS_IN", "HK")]),
    "SIKAYET-067": dict(note="Aradaki gözlem (barmenin yorgunluğu) EVENT olarak yoktu.",
        add_ent=[E("barmen çok yorgun görünüyordu", "EVENT")],
        add_rel=[R("tek kişi çalışıyormuş", "CAUSES", "barmen çok yorgun görünüyordu")]),
}


def main():
    candidates = (DATA / "gold_candidates.txt").read_text(encoding="utf-8").split()
    unknown = set(EDITS) - set(candidates)
    assert not unknown, f"edits for non-candidates: {unknown}"
    raw = {r[0]: r for r in read_csv(RAW_CSV)}
    out = {}
    for rid, ed in EDITS.items():
        ents = json.loads(raw[rid][4]) + ed.get("add_ent", [])
        rels = json.loads(raw[rid][5])
        for d in ed.get("del_rel", []):
            assert d in rels, f"{rid}: relation to delete not found {d}"
            rels.remove(d)
        rels += ed.get("add_rel", [])
        out[rid] = {"entities": ents, "relations": rels, "note": ed["note"]}
    GOLD_CORRECTIONS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    GOLD_IDS.write_text("\n".join(candidates) + "\n", encoding="utf-8")
    print(f"gold ids: {len(candidates)}, corrected: {len(out)}")


if __name__ == "__main__":
    main()
