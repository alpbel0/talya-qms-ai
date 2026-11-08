"""Build results/report.md from the files the earlier steps wrote.

Every number in the report is read from results/*.json / metrics.csv / data/*,
so re-running the pipeline regenerates a consistent report.
"""
import csv
import json
from collections import defaultdict

from common import DATA, GOLD_CORRECTIONS, LABELS, RESULTS, load_clean, load_gold_ids

DIFF_TR = {"explicit": "açık", "implicit": "örtük", "multi_cause": "çoklu neden", "chain": "zincir",
           "abbreviation": "kısaltma", "informal": "günlük dil", "negative": "negatif"}


def f(x, pct=False):
    if x in ("", None):
        return "—"
    x = float(x)
    return f"{x:.1%}" if pct else f"{x:.3f}"


def load_metrics():
    m = {}
    with open(RESULTS / "metrics.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            m[(r["model"], r["setting"], r["match"], r["breakdown"], r["label"])] = r
    return m


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def short(name):
    return name.split("/")[0]


def pick(items, k=3, key="id", seen=None):
    seen = set() if seen is None else seen
    out = []
    for it in sorted(items, key=lambda x: x[key]):
        if it[key] in seen:
            continue
        seen.add(it[key])
        out.append(it)
        if len(out) == k:
            break
    return out


def main():
    stats = json.loads((RESULTS / "data_stats.json").read_text(encoding="utf-8"))
    meta = json.loads((RESULTS / "ner_run_meta.json").read_text(encoding="utf-8"))
    ea = json.loads((RESULTS / "error_analysis.json").read_text(encoding="utf-8"))
    corr = json.loads(GOLD_CORRECTIONS.read_text(encoding="utf-8")) if GOLD_CORRECTIONS.exists() else {}
    M = load_metrics()
    models = list(meta["models"])
    recs = load_clean()
    gold = load_gold_ids()
    hw = meta["hardware"]
    A, G = stats["all"], stats["gold"]

    def get(model, setting, match, bd, label, col):
        r = M.get((model, setting, match, bd, label))
        return None if r is None else r[col]

    # case sensitivity: DEPARTMENT gold entities written in lowercase vs capitalised
    case = {}
    dept = [e["text"] for r in recs for e in r["entities"] if e["label"] == "DEPARTMENT"]
    n_low = sum(t[:1].islower() for t in dept)
    for m in models:
        miss = ea[m]["all"]["missed"].get("DEPARTMENT", [])
        ml = sum(i["entity"][:1].islower() for i in miss)
        cap_wrong = sum(1 for i in ea[m]["all"]["mislabel"] + ea[m]["all"]["false_pos"]
                        if i["pred"][1] == "ORG" and i["pred"][0][:1].isupper() and not i["pred"][0].isupper()
                        and i.get("gold", ("", "NONE"))[1] != "DEPARTMENT")
        case[m] = {"low_missed": ml, "low_total": n_low,
                   "up_missed": len(miss) - ml, "up_total": len(dept) - n_low, "cap_wrong": cap_wrong}

    L = []
    w = L.append
    w("# Deney A Raporu: Hazır Türkçe NER Modellerinin Otel Kalite Metinlerindeki Performansı\n")
    w("> Bu rapor `experiments/make_report.py` tarafından otomatik üretilmiştir. Tablolardaki tüm sayılar "
      "`results/metrics.csv`, `results/error_analysis.json`, `results/data_stats.json` ve "
      "`results/ner_run_meta.json` dosyalarından okunur.\n")

    w("## Özet\n")
    for m in models:
        g = lambda s, mt, lab, c: get(m, s, mt, "gold", lab, c)
        w(f"- **`{m}`** (gold, n={len(gold)}): bizim varlıklarımızın yalnızca "
          f"**{f(g('span_only', 'partial', 'ALL', 'R'), True)}**'ine herhangi bir span ile dokunuyor "
          f"(tahminlerinin {f(g('span_only', 'partial', 'ALL', 'P'), True)}'i bir varlığımızla örtüşüyor). "
          f"ORG → DEPARTMENT eşlemesiyle DEPARTMENT F1 = {f(g('map_ORG=DEPARTMENT', 'exact', 'DEPARTMENT', 'F1'))} "
          f"(exact) / {f(g('map_ORG=DEPARTMENT', 'partial', 'DEPARTMENT', 'F1'))} (partial); 6 etiket MICRO F1 = "
          f"{f(g('map_ORG=DEPARTMENT', 'exact', 'MICRO', 'F1'))} / {f(g('map_ORG=DEPARTMENT', 'partial', 'MICRO', 'F1'))}.")
    w("- EVENT, ROOT_CAUSE, KPI ve ACTION varlıkları — yani nedensellik analizinin asıl taşıyıcıları — genel amaçlı "
      "NER tarafından neredeyse hiç görülmüyor (§5, §6.5).")
    w("- Yakalanan şey büyük ölçüde büyük harfle yazılmış departman ve sistem adları/kısaltmaları; ORG etiketi "
      "departman, ekipman ve süreç kısaltmalarını ayırt etmiyor (§6.3).")
    w("- Sentetik etiketlerin kalitesi de bir bulgu: gold incelemesinde satırların "
      f"{len(corr)}/{len(gold)}'ında eksik/hatalı etiket bulundu (§2.1).\n")

    # ---------------------------------------------------------------- scope
    w("## 1. Kapsam ve önemli uyarılar\n")
    w("- **Yalnızca Deney A (hazır BERTurk NER) çalıştırıldı.** Planlanan Deney B (yerel LLM ile zero-/few-shot "
      "çıkarım) proje sahibinin kararıyla bu çalışmanın **kapsamı dışında bırakıldı**; çalıştırılmadı ve bu raporda "
      "LLM sonucu yoktur.")
    w("- **İlişki çıkarımı ölçülmedi.** NER modelleri yalnızca varlık sınırı + PER/ORG/LOC etiketi üretir; "
      "(head, type, tail) üçlüsü üretmedikleri için ilişki P/R/F1 bu deney için *uygulanamaz*. Dolayısıyla "
      "\"örtük nedensellik yakalandı mı\" ve \"negatiflerde uydurma ilişki\" soruları bu deneyle yanıtlanamaz "
      "(bkz. §6.5).")
    w("- **Etiketler LLM üretimidir.** Veri seti ve etiketleri Claude Sonnet 5.5 ile sentetik olarak üretildi. "
      "Tüm set sonuçları bu otomatik etiketlere dayanır.")
    w(f"- **Gold alt küme insan doğrulaması değildir.** {len(gold)} satırlık alt küme Claude (Opus 5.5) tarafından "
      f"satır satır incelenip {len(corr)} satırı düzeltildi. İnceleyen model, üreten modelle aynı ailedendir; "
      "ortak hataları gözden kaçırmış olabilir. Bitirme raporunda bu alt kümenin en azından bir kısmının insan "
      "tarafından kontrol edilmesi önerilir (`data/synthetic/gold_review.md`).")
    w("- **Model etiket uzayı uyuşmuyor.** Modeller bizim 6 etiketimizi bilmez; amaç skor değil, neyin yakalanıp "
      "neyin kaçırıldığını göstermektir. Bu yüzden iki ayar raporlanır (§4).\n")

    # ---------------------------------------------------------------- data
    w("## 2. Veri\n")
    w(f"- Kaynak: `data/synthetic/synthetic_hotel_quality.csv`, {stats['n_rows_raw']} satır.")
    w(f"- Doğrulama: her entity metninin metinde birebir alt dize olması, her relation head/tail'inin entities "
      f"içinde olması, etiket/ilişki türü ve yönünün şemaya uyması kontrol edildi. **Hatalı satır: "
      f"{stats['n_invalid']}** (`data/synthetic/invalid_rows.csv`), teste giren satır: {stats['n_valid']}.")
    w("- Her entity'e metindeki ilk geçtiği yerin karakter offset'i (`start`, `end`) eklendi (`data/synthetic/clean.jsonl`). "
      "Partial eşleşmede bir entity'nin metindeki *tüm* geçişleri dikkate alınır.")
    w(f"- Ortalama metin uzunluğu: {A['avg_words']} kelime.\n")

    w("**Dağılım (tüm set / gold):**\n")
    rows = [[k, A["doc_type"].get(k, 0), (G or {}).get("doc_type", {}).get(k, 0)] for k in sorted(A["doc_type"])]
    w(table(["doc_type", "Tüm set", "Gold"], rows) + "\n")
    rows = [[f"{k} ({DIFF_TR[k]})", A["difficulty_tag"].get(k, 0), (G or {}).get("difficulty_tag", {}).get(k, 0)]
            for k in DIFF_TR]
    w(table(["difficulty etiketi*", "Tüm set", "Gold"], rows))
    w("\n\\* Birleşik etiketli satırlar (örn. `abbreviation|implicit`) her bileşende sayılır.\n")
    rows = [[k, A["entity_label"].get(k, 0), (G or {}).get("entity_label", {}).get(k, 0)] for k in LABELS]
    rows.append(["**Toplam**", A["n_entities"], (G or {}).get("n_entities", 0)])
    w(table(["Varlık etiketi", "Tüm set", "Gold"], rows) + "\n")
    rows = [[k, A["relation_type"].get(k, 0), (G or {}).get("relation_type", {}).get(k, 0)]
            for k in ("CAUSES", "ADDRESSED_BY", "OCCURS_IN")]
    rows.append(["**Toplam**", A["n_relations"], (G or {}).get("n_relations", 0)])
    w(table(["İlişki türü", "Tüm set", "Gold"], rows) + "\n")

    w("### 2.1 Gold alt küme\n")
    w(f"Her doc_type × zorluk grubu (açık, örtük, çoklu/zincir, kısaltma/günlük dil, negatif) hücresinden 3 satır "
      f"sabit tohumla (seed=42) seçildi: 4 × 5 × 3 = {len(gold)} satır. Her satır okunup etiketleri kontrol edildi; "
      f"**{len(corr)}/{len(gold)} satırda ({len(corr)/max(len(gold),1):.0%}) düzeltme gerekti.** Düzeltmeler ham "
      "CSV'yi değiştirmez; `data/synthetic/gold_corrections.json` içinde gerekçesiyle tutulur ve doğrulama adımında "
      "uygulanır (düzeltilmiş satırlar tüm set hesaplarında da düzeltilmiş hâliyle yer alır).\n")
    w("Bu oran, üretici LLM'in etiketlerinin en çok **zincirin ara/son halkasını** ve **departman/aksiyon "
      "bağlantılarını atladığını** gösteriyor:\n")
    w(table(["id", "Düzeltme gerekçesi"], [[k, v["note"]] for k, v in sorted(corr.items())]) + "\n")

    # ---------------------------------------------------------------- models
    w("## 3. Modeller ve donanım\n")
    rows = []
    for name, mm in meta["models"].items():
        rows.append([f"[`{name}`](https://huggingface.co/{name})", f"`{mm['revision'][:12]}`",
                     ", ".join(l for l in mm["labels"] if l != "O"), mm["aggregation_strategy"],
                     mm["n_pred"], f"{mm['seconds']} sn ({mm['sec_per_text']*1000:.0f} ms/metin)"])
    w(table(["Model (Hugging Face)", "Commit", "Etiketler", "Birleştirme", "Bulunan span", "Süre (300 metin)"], rows))
    w("\nİki model de BERTurk (`dbmdz/bert-base-turkish-cased`) tabanlıdır ve PER/ORG/LOC ile eğitilmiştir. "
      "Modeller tam commit hash'iyle sabitlenerek yüklenir (`experiments/ner_baseline.py`).\n")
    w("**Birleştirme stratejisi notu:** İlk denemede `aggregation_strategy=\"simple\"` kullanıldı ve kısaltmalar "
      "alt-kelimelerine bölündü (örn. `HK` → `H` + `K`, `DÖF` → `DÖ` + `F`). Modeller kelime düzeyinde eğitildiği "
      "için kelimenin etiketini ilk alt-kelimeden alan `first` stratejisine geçildi; raporlanan tüm sonuçlar "
      "`first` iledir.\n")
    w(table(["Donanım / yazılım", "Değer"], [
        ["CPU", hw.get("cpu_name", hw.get("processor"))],
        ["Mantıksal çekirdek / torch thread", f"{hw.get('logical_cpus', '?')} / {hw['torch_threads']}"],
        ["RAM", f"{hw.get('ram_gb', '?')} GB"],
        ["Hızlandırıcı", "Yok (CPU). CUDA: " + str(hw["cuda_available"])],
        ["İşletim sistemi", hw["platform"]],
        ["Python / torch / transformers", f"{hw['python']} / {hw['torch']} / {hw['transformers']}"],
    ]) + "\n")

    # ---------------------------------------------------------------- method
    w("## 4. Değerlendirme yöntemi\n")
    w("1. **`span_only` (etiketten bağımsız örtüşme):** Model hangi etiketi verirse versin, bulduğu span bizim bir "
      "varlığımızla karakter düzeyinde örtüşüyor mu? *P* = örtüşen tahmin oranı, *R* (etiket bazında) = o "
      "etiketteki gold varlıkların herhangi bir tahminle örtüşme oranı (\"kapsama\").")
    w("2. **`map_ORG=DEPARTMENT` (önceden sabitlenmiş eşleme):** Sonuçlara bakılmadan ORG → DEPARTMENT eşlemesi "
      "seçildi; PER ve LOC hiçbir etikete eşlenmez ve her zaman yanlış pozitif sayılır. Ardından 6 etiket üzerinden "
      "P/R/F1 iki modda hesaplanır: **exact** (metin + etiket birebir aynı) ve **partial** (span örtüşmesi + aynı "
      "etiket). MICRO satırı tüm etiketlerin toplamıdır; DEPARTMENT dışındaki etiketler için model hiç tahmin "
      "üretmediğinden P tanımsızdır (—) ve R = 0'dır.\n")

    # ---------------------------------------------------------------- results
    w("## 5. Sonuçlar\n")
    for bd, title in (("gold", "5.1 Ana sonuç: gold alt küme"), ("all", "5.2 Tüm set (LLM üretimi etiketler)")):
        n = len(gold) if bd == "gold" else len(recs)
        w(f"### {title} (n = {n} metin)\n")
        if bd == "all":
            w("> Bu tablo, doğrulanmamış LLM üretimi etiketlere dayanır; ana sonuç olarak gold tablosu "
              "kullanılmalıdır.\n")
        rows = []
        for m in models:
            for setting, match, label, desc in (
                ("span_only", "partial", "ALL", "Etiketten bağımsız örtüşme"),
                ("map_ORG=DEPARTMENT", "exact", "DEPARTMENT", "DEPARTMENT, exact"),
                ("map_ORG=DEPARTMENT", "partial", "DEPARTMENT", "DEPARTMENT, partial"),
                ("map_ORG=DEPARTMENT", "exact", "MICRO", "6 etiket MICRO, exact"),
                ("map_ORG=DEPARTMENT", "partial", "MICRO", "6 etiket MICRO, partial"),
            ):
                g = lambda c: get(m, setting, match, bd, label, c)
                rows.append([short(m), desc, f(g("P")), f(g("R")), f(g("F1")),
                             f"{g('tp_pred')}/{g('n_pred')}", f"{g('tp_gold')}/{g('n_gold')}"])
        w(table(["Model", "Ölçüm", "P", "R", "F1", "Doğru tahmin / tahmin", "Bulunan gold / gold"], rows) + "\n")

        w(f"**Etiket bazında kapsama (span_only R, {bd}):** model, bizim etiketimizdeki varlıkların ne kadarına "
          "herhangi bir span ile dokunabiliyor?\n")
        rows = []
        for lab in LABELS:
            row = [lab, get(models[0], "span_only", "partial", bd, lab, "n_gold")]
            for m in models:
                row.append(f"{f(get(m, 'span_only', 'partial', bd, lab, 'R'), True)} "
                           f"({get(m, 'span_only', 'partial', bd, lab, 'tp_gold')})")
            rows.append(row)
        w(table(["Etiket", "Gold varlık"] + [short(m) for m in models], rows) + "\n")

    w("### 5.3 Difficulty türüne göre\n")
    for bd, note in (("all", "tüm set"), ("gold", "gold alt küme — hücreler küçük, yorumlarken dikkat")):
        w(f"**{note.capitalize()}:** span_only R (tüm etiketler) ve DEPARTMENT partial F1.\n")
        rows = []
        for t in DIFF_TR:
            key = f"{bd}|difficulty={t}"
            nt = M.get((models[0], "span_only", "partial", key, "ALL"))
            if nt is None:
                continue
            row = [f"{t} ({DIFF_TR[t]})", nt["n_texts"], nt["n_gold"]]
            for m in models:
                row += [f(get(m, "span_only", "partial", key, "ALL", "R"), True),
                        f(get(m, "map_ORG=DEPARTMENT", "partial", key, "DEPARTMENT", "F1"))]
            rows.append(row)
        hdr = ["difficulty", "Metin", "Gold varlık"]
        for m in models:
            hdr += [f"{short(m)} kapsama", f"{short(m)} DEPT F1"]
        w(table(hdr, rows) + "\n")

    w("### 5.4 Doküman türüne göre (tüm set)\n")
    rows = []
    for dt in sorted(A["doc_type"]):
        key = f"all|doc_type={dt}"
        row = [dt]
        for m in models:
            row += [f(get(m, "span_only", "partial", key, "ALL", "R"), True),
                    f(get(m, "map_ORG=DEPARTMENT", "partial", key, "DEPARTMENT", "R"), True),
                    f(get(m, "map_ORG=DEPARTMENT", "partial", key, "DEPARTMENT", "P"), True)]
        rows.append(row)
    hdr = ["doc_type"]
    for m in models:
        hdr += [f"{short(m)} kapsama", f"{short(m)} DEPT R", f"{short(m)} DEPT P"]
    w(table(hdr, rows) + "\n")

    # ---------------------------------------------------------------- errors
    w("## 6. Hata analizi\n")
    w("Örnekler mümkün olduğunca gold alt kümeden, yoksa tüm setten seçilmiştir (id sırasıyla ilk örnekler).\n")
    for m in models:
        x, xg = ea[m]["all"], ea[m]["gold"]
        w(f"### 6.{models.index(m) + 1} `{m}`\n")

        # top-3 labels by miss rate on gold (fallback all)
        src = "gold" if gold else "all"
        lab_rows = []
        for lab in LABELS:
            n = int(get(m, "span_only", "partial", src, lab, "n_gold") or 0)
            hit = int(get(m, "span_only", "partial", src, lab, "tp_gold") or 0)
            if n:
                lab_rows.append((1 - hit / n, n - hit, lab, n))
        lab_rows.sort(key=lambda t: (-t[0], -t[1]))
        w(f"**En çok kaçırılan 3 etiket** ({src}, hiçbir tahminle örtüşmeyen gold varlık oranı): " +
          ", ".join(f"{lab} %{r*100:.0f} ({miss}/{n})" for r, miss, lab, n in lab_rows[:3]) + ".\n")

        d_rows = []
        for t in DIFF_TR:
            r = get(m, "span_only", "partial", f"all|difficulty={t}", "ALL", "R")
            if r not in (None, ""):
                d_rows.append((float(r), t))
        d_rows.sort()
        w("**En düşük kapsamalı 3 difficulty türü** (tüm set, span_only R): " +
          ", ".join(f"{t} ({DIFF_TR[t]}) %{r*100:.1f}" for r, t in d_rows[:3]) + ".\n")

        conf = x["confusion"]
        ner_labels = sorted({k.split("->")[0] for k in conf})
        cols = LABELS + ["NONE"]
        rows = [[nl] + [conf.get(f"{nl}->{c}", 0) for c in cols] for nl in ner_labels]
        w("**Karışıklık matrisi** (tüm set; satır = model etiketi, sütun = örtüştüğü gold etiketi, NONE = hiçbir "
          "gold varlıkla örtüşmüyor). Bir tahmin birden çok gold varlıkla örtüşebilir.\n")
        w(table(["Model ↓ / Gold →"] + cols, rows) + "\n")

        def ex_missed(pool):
            items = []
            for lab in ("EVENT", "ROOT_CAUSE", "EQUIPMENT", "DEPARTMENT"):
                items += [dict(i, lab=lab) for i in pool.get(lab, [])]
            return items

        w("**Örnek — kaçırılan varlıklar:**\n")
        miss = ex_missed(xg["missed"]) or ex_missed(x["missed"])
        by_lab = defaultdict(list)
        for i in miss:
            by_lab[i["lab"]].append(i)
        chosen, seen_ids = [], set()
        for lab in ("DEPARTMENT", "EQUIPMENT", "ROOT_CAUSE"):
            chosen += pick(by_lab[lab], 1, seen=seen_ids)
        for i in chosen:
            pr = ", ".join(f"`{t}`/{l}" for t, l in i["pred"]) or "*(hiç span yok)*"
            w(f"- **{i['id']}**: \"{i['text']}\"  \n  Beklenen: `{i['entity']}` / {i['lab']} — Modelin çıktısı: {pr}")
        w("")

        w("**Örnek — etiket uyuşmazlığı** (span bizim bir varlığımızla örtüşüyor ama eşlenen etiket farklı):\n")
        for i in pick(xg["mislabel"] or x["mislabel"], 3):
            w(f"- **{i['id']}**: \"{i['text']}\"  \n  Beklenen: `{i['gold'][0]}` / {i['gold'][1]} — "
              f"Modelin çıktısı: `{i['pred'][0]}` / {i['pred'][1]}")
        w("")

        fps = pick(x["false_pos"], 3)
        w("**Örnek — yanlış pozitif** (hiçbir gold varlıkla örtüşmeyen span):\n")
        if fps:
            for i in fps:
                w(f"- **{i['id']}**: \"{i['text']}\"  \n  Modelin çıktısı: `{i['pred'][0]}` / {i['pred'][1]}")
        else:
            w("- Yok.")
        w("")

    # abbreviations
    w(f"### 6.{len(models) + 1} Kısaltmalar\n")
    w("Metinlerde kelime olarak geçen her kısaltma için: model bir span ile dokundu mu, span tam olarak kısaltmanın "
      "kendisi mi, hangi etiketi verdi; gold'da bu kısaltma hangi etiketle (bir varlığın parçası olarak) "
      "işaretlenmiş? (tüm set)\n")
    abbrs = []
    for r in ea[models[0]]["all"]["abbrev"]:
        if r["abbr"] not in abbrs:
            abbrs.append(r["abbr"])
    rows = []
    for ab in abbrs:
        base = [r for r in ea[models[0]]["all"]["abbrev"] if r["abbr"] == ab]
        gl = defaultdict(int)
        for r in base:
            for lab in sorted(set(r["gold_labels"])) or ["etiketsiz"]:
                gl[lab] += 1
        row = [f"`{ab}`", len(base), ", ".join(f"{k} {v}" for k, v in sorted(gl.items(), key=lambda t: -t[1]))]
        for m in models:
            rr = [r for r in ea[m]["all"]["abbrev"] if r["abbr"] == ab]
            tagged = sum(bool(r["pred"]) for r in rr)
            exact = sum(r["exact"] for r in rr)
            labs = defaultdict(int)
            for r in rr:
                for _, l in r["pred"]:
                    labs[l] += 1
            row.append(f"{tagged}/{len(rr)} (tam: {exact}) " + " ".join(f"{k}:{v}" for k, v in sorted(labs.items())))
        rows.append(row)
    w(table(["Kısaltma", "Geçiş", "Gold etiketi"] + [f"{short(m)}: dokundu (tam) etiket" for m in models], rows) + "\n")
    w("Gözlemler: ORG etiketi, bu modellerde departman kısaltmaları (HK, F&B, TS) ile sistem/ekipman "
      "kısaltmalarını (PMS, FCU, AHU) ve süreç kısaltmalarını (DÖF, KPI) **ayırt etmeden** kullanılan tek "
      "\"büyük harfli kısaltma\" sınıfı gibi davranıyor; bu yüzden ORG → DEPARTMENT eşlemesi kısaltmalarda "
      "EQUIPMENT/ACTION'a ait span'ları da DEPARTMENT'a çekiyor. `F&B` WordPiece ön-tokenizasyonunda `&` "
      "işaretinden bölündüğü için kelime düzeyinde birleştirmede bile `F` ve `B` ayrı span olarak çıkabiliyor.\n")

    # case sensitivity
    w(f"### 6.{len(models) + 2} Büyük/küçük harf etkisi\n")
    w(f"Gold DEPARTMENT varlıklarının {n_low}/{len(dept)}'i küçük harfle başlıyor; bunlar çoğunlukla misafir "
      "şikâyetlerindeki günlük ifadeler (\"resepsiyona\", \"kat görevlisi\", \"ön büro\"). "
      "Kaçırılan DEPARTMENT varlıklarının yazım biçimine göre dağılımı (tüm set):\n")
    rows = []
    for m in models:
        c = case[m]
        rows.append([short(m), f"{c['low_missed']}/{c['low_total']} ({c['low_missed']/max(c['low_total'],1):.0%})",
                     f"{c['up_missed']}/{c['up_total']} ({c['up_missed']/max(c['up_total'],1):.0%})", c["cap_wrong"]])
    w(table(["Model", "Küçük harfli DEPARTMENT kaçırılan", "Büyük harfli DEPARTMENT kaçırılan",
             "Büyük harfle başlayan, DEPARTMENT olmayan ORG span"], rows) + "\n")
    w("Son sütun, cümle başında ya da özel ad gibi yazılmış sıradan isimlerin (örn. \"Bulaşık makinesi\", "
      "\"Kombi\", \"Sauna\") ORG olarak etiketlenip departman olmayan bir varlığa ya da hiçbir varlığa denk "
      "gelmesini sayar (tamamı büyük harf olan kısaltmalar hariç).\n")

    # implicit / negatives
    w(f"### 6.{len(models) + 3} Örtük nedensellik ve negatif örnekler\n")
    w("- **Örtük nedensellik:** NER modelleri ilişki üretmediğinden örtük CAUSES ilişkilerinin yakalanıp "
      "yakalanmadığı bu deneyle **ölçülemez**. Ölçülebilen tek şey, nedenselliğin uçlarını oluşturan ROOT_CAUSE ve "
      "EVENT varlıklarına dokunma oranıdır:")
    for m in models:
        parts = []
        for t in ("explicit", "implicit", "multi_cause", "chain"):
            key = f"all|difficulty={t}"
            parts.append(f"{t} ROOT_CAUSE R={f(get(m, 'span_only', 'partial', key, 'ROOT_CAUSE', 'R'), True)}, "
                         f"EVENT R={f(get(m, 'span_only', 'partial', key, 'EVENT', 'R'), True)}")
        w(f"  - `{short(m)}`: " + "; ".join(parts))
    w("  Yani hazır NER, nedensellik zincirinin uç varlıklarını neredeyse hiç görmüyor; bu, ilişki çıkarımına "
      "geçmeden önce bile alan-özel varlık tanımanın gerektiğini gösteriyor.")
    w("- **Negatif örnekler (ilişkisiz metinler):** İlişki üretilmediği için \"uydurma ilişki\" sorusu bu deney için "
      "geçerli değildir. Varlık düzeyinde:")
    for m in models:
        n = ea[m]["all"]["negatives"]
        exs = "; ".join(f"{e['id']}: `{e['pred'][0]}`/{e['pred'][1]}" for e in n["examples"][:3]) or "yok"
        w(f"  - `{short(m)}`: {n['n_texts']} negatif metinde {n['n_pred']} span; bunlardan {n['n_pred_no_gold']} "
          f"tanesi hiçbir gold varlıkla örtüşmüyor (örnek: {exs}).")
    w("  Negatif metinlerdeki gold varlıkların çoğu departman adıdır; §5.3'teki negatif satırında kapsamanın "
      "görece yüksek çıkması bundan kaynaklanır, modelin negatifleri \"anladığı\" anlamına gelmez.")
    w("")

    # ---------------------------------------------------------------- suggestions
    w("## 7. Yorum ve iyileştirme önerileri\n")
    w("Bulgulardan çıkan sonuçlar ve öneriler (sayılar §5–6'daki tablolardan):\n")
    w("1. **Genel amaçlı NER bu görev için yetersiz.** Modellerin etiket uzayı (PER/ORG/LOC) bizim olay/kök neden/"
      "aksiyon gibi *yüklem içeren, çok kelimeli* varlıklarımızla örtüşmüyor; EVENT, ROOT_CAUSE, ACTION ve KPI "
      "kapsaması sıfıra yakın. Yakalanan şey neredeyse yalnızca büyük harfle başlayan departman/sistem adları.")
    w("2. **Alan-özel ince ayar (fine-tuning):** BERTurk tabanı korunup 6 etiketlik BIO şemasıyla token "
      "sınıflandırma eğitimi yapılması en doğrudan iyileştirme. Ancak eğitim verisi olarak bu sentetik seti "
      "kullanmadan önce etiket kalitesi artırılmalı (gold incelemesinde satırların yaklaşık üçte birinde eksik etiket "
      "bulundu). İlişkiler için varlık çiftleri üzerinde ayrı bir ilişki sınıflandırıcı eklenebilir.")
    w("3. **Kural tabanlı kısaltma sözlüğü:** HK, F&B, TS, FO → DEPARTMENT; PMS, AHU, FCU → EQUIPMENT; DÖF → "
      "süreç/aksiyon bağlamı gibi sabit bir sözlük, hem bir ön işleme adımı (kısaltma açma) hem de bir post-"
      "processing katmanı olarak ORG etiketinin belirsizliğini doğrudan giderir. `F&B` gibi işaret içeren "
      "kısaltmalar tokenizasyondan önce korunmalı.")
    w("4. **Büyük harf yanlılığı (§6." + str(len(models) + 2) + "):** Cased modeller küçük harfle yazılmış "
      "departman adlarını neredeyse tamamen kaçırıyor; savasy ayrıca büyük harfle başlayan sıradan isimleri ORG "
      "sanıyor. SIKAYET metinlerinde DEPARTMENT recall'unun en düşük olması (§5.4) bununla tutarlı. Departman "
      "sözlüğüyle normalizasyon veya günlük dil örnekleriyle eğitim gerekli.")
    w("5. **LLM tabanlı çıkarım (Deney B) ileride:** Bu çalışmada kapsam dışı bırakılan zero-/few-shot LLM deneyi, "
      "etiket uzayı uyuşmazlığını prompt ile çözebileceği ve ilişkileri de üretebileceği için bir sonraki adım "
      "olarak önerilir; few-shot örnek sayısını artırmak ve kısaltma sözlüğünü prompt'a eklemek denenebilir.")
    w("6. **Değerlendirme verisi:** Gold alt kümenin insan tarafından doğrulanması ve tercihen iki anotatörle "
      "uyum (Cohen's κ) ölçülmesi, sonuçların rapor için güvenilirliğini artırır.\n")

    w("## 8. Tekrarlanabilirlik\n")
    w("Tüm adımlar `python experiments/run_all.py` ile baştan çalışır (bkz. `README.md`). Modeller commit hash'iyle "
      "sabitlenmiştir; NER çıkarımı deterministiktir (örnekleme yok). Gold seçimi sabit tohumla (seed=42) yapılır, "
      "gold düzeltmeleri `experiments/gold_review_edits.py` içinde kayıtlıdır. Ham tahminler: "
      "`results/predictions/*.jsonl`; tüm metrikler: `results/metrics.csv`.\n")

    (RESULTS / "report.md").write_text("\n".join(L), encoding="utf-8")
    print("wrote results/report.md")


if __name__ == "__main__":
    main()
