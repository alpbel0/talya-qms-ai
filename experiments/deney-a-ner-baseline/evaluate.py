"""Step 4-5: score NER predictions against our labels and collect error analysis.

The NER models only know PER/ORG/LOC, so two settings are reported:

  span_only         label-agnostic. Does a predicted span overlap a gold entity at
                    all? Precision = share of predicted spans that overlap some
                    gold entity; recall per gold label = share of that label's
                    gold entities overlapped by some prediction.
  map_ORG=DEPARTMENT  a mapping fixed BEFORE looking at results: ORG -> DEPARTMENT,
                    PER/LOC -> unmapped (always a false positive). Then the usual
                    per-label P/R/F1 over our 6 labels, in two match modes:
                      exact   = same surface text and same label
                      partial = character spans overlap and same label

A gold entity counts as overlapped if ANY occurrence of its text in the sentence
overlaps the prediction (the CSV lists each surface string once).

Relations: these models produce no relations, so relation metrics are not
applicable for Experiment A and are not written.
"""
import csv
import json
import re
from collections import Counter, defaultdict

from common import (LABELS, PRED_DIR, RESULTS, load_clean, load_gold_ids,
                    read_jsonl)
from ner_baseline import MODELS, slug

MAPPING = {"ORG": "DEPARTMENT"}
ABBREVIATIONS = ["HK", "F&B", "DÖF", "PMS", "KPI", "TS", "FO", "AHU", "FCU", "IT"]


def occurrences(text, sub):
    out, i = [], text.find(sub)
    while i >= 0:
        out.append((i, i + len(sub)))
        i = text.find(sub, i + 1)
    return out


def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]


def prf(tp_p, n_pred, tp_r, n_gold):
    p = tp_p / n_pred if n_pred else None
    r = tp_r / n_gold if n_gold else None
    f = 2 * p * r / (p + r) if p is not None and r is not None and (p + r) else (0.0 if p is not None and r is not None else None)
    return p, r, f


def gold_spans(rec):
    return [(e, occurrences(rec["text"], e["text"])) for e in rec["entities"]]


def score(recs, preds_by_id):
    """Return {(setting, match, label): [tp_p, n_pred, tp_r, n_gold]}."""
    c = defaultdict(lambda: [0, 0, 0, 0])
    for rec in recs:
        gs = gold_spans(rec)
        ps = preds_by_id[rec["id"]]

        # span_only
        for p in ps:
            hit = any(overlaps((p["start"], p["end"]), o) for _, occ in gs for o in occ)
            c[("span_only", "partial", "ALL")][0] += hit
            c[("span_only", "partial", "ALL")][1] += 1
        for e, occ in gs:
            hit = any(overlaps((p["start"], p["end"]), o) for p in ps for o in occ)
            for lab in (e["label"], "ALL"):
                c[("span_only", "partial", lab)][2] += hit
                c[("span_only", "partial", lab)][3] += 1

        # mapped
        mp = [dict(p, mlabel=MAPPING.get(p["label"], "UNMAPPED")) for p in ps]
        for mode in ("exact", "partial"):
            key = lambda lab: ("map_ORG=DEPARTMENT", mode, lab)

            def match(p, e, occ):
                if p["mlabel"] != e["label"]:
                    return False
                if mode == "exact":
                    return p["text"] == e["text"]
                return any(overlaps((p["start"], p["end"]), o) for o in occ)

            for p in mp:
                hit = any(match(p, e, occ) for e, occ in gs)
                for lab in ({p["mlabel"], "MICRO"} if p["mlabel"] in LABELS else {"MICRO"}):
                    c[key(lab)][0] += hit
                    c[key(lab)][1] += 1
            for e, occ in gs:
                hit = any(match(p, e, occ) for p in mp)
                for lab in (e["label"], "MICRO"):
                    c[key(lab)][2] += hit
                    c[key(lab)][3] += 1
    return c


def breakdowns(recs, gold):
    out = [("all", recs)]
    g = [r for r in recs if r["id"] in gold]
    if g:
        out.append(("gold", g))
    for name, pool in (("all", recs), ("gold", g)):
        if not pool:
            continue
        tags = sorted({d for r in pool for d in r["difficulty"]})
        for t in tags:
            out.append((f"{name}|difficulty={t}", [r for r in pool if t in r["difficulty"]]))
    for dt in sorted({r["doc_type"] for r in recs}):
        out.append((f"all|doc_type={dt}", [r for r in recs if r["doc_type"] == dt]))
    return out


def error_analysis(recs, preds_by_id, gold):
    """Label-agnostic misses, false positives, label confusions, abbreviations, negatives."""
    ex = {"missed": defaultdict(list), "false_pos": [], "mislabel": [], "confusion": Counter(),
          "abbrev": [], "negatives": {"n_texts": 0, "n_pred": 0, "n_pred_no_gold": 0, "examples": []}}
    for rec in recs:
        gs = gold_spans(rec)
        ps = preds_by_id[rec["id"]]
        for e, occ in gs:
            if not any(overlaps((p["start"], p["end"]), o) for p in ps for o in occ):
                ex["missed"][e["label"]].append({"id": rec["id"], "text": rec["text"], "entity": e["text"],
                                                 "pred": [(p["text"], p["label"]) for p in ps]})
        for p in ps:
            hits = [e for e, occ in gs if any(overlaps((p["start"], p["end"]), o) for o in occ)]
            if not hits:
                ex["confusion"][(p["label"], "NONE")] += 1
                ex["false_pos"].append({"id": rec["id"], "text": rec["text"], "pred": (p["text"], p["label"])})
            for e in hits:
                ex["confusion"][(p["label"], e["label"])] += 1
                if MAPPING.get(p["label"], "UNMAPPED") != e["label"]:
                    ex["mislabel"].append({"id": rec["id"], "text": rec["text"], "pred": (p["text"], p["label"]),
                                           "gold": (e["text"], e["label"])})
        for ab in ABBREVIATIONS:
            for m in re.finditer(r"(?<![\wÇĞİÖŞÜçğıöşü&])" + re.escape(ab) + r"(?![A-Za-zÇĞİÖŞÜ&])", rec["text"]):
                span = (m.start(), m.end())
                gl = [e["label"] for e, occ in gs if any(overlaps(span, o) for o in occ)]
                pl = [(p["text"], p["label"]) for p in ps if overlaps((p["start"], p["end"]), span)]
                ex["abbrev"].append({"id": rec["id"], "abbr": ab, "gold_labels": gl, "pred": pl,
                                     "exact": any(t == ab for t, _ in pl)})
        if "negative" in rec["difficulty"]:
            n = ex["negatives"]
            n["n_texts"] += 1
            n["n_pred"] += len(ps)
            for p in ps:
                if not any(overlaps((p["start"], p["end"]), o) for _, occ in gs for o in occ):
                    n["n_pred_no_gold"] += 1
                    n["examples"].append({"id": rec["id"], "text": rec["text"], "pred": (p["text"], p["label"])})
    ex["missed"] = dict(ex["missed"])
    ex["confusion"] = {f"{a}->{b}": v for (a, b), v in sorted(ex["confusion"].items())}
    return ex


def main():
    recs = load_clean()
    gold = load_gold_ids()
    rows, analysis = [], {}
    for name in MODELS:
        preds = {r["id"]: r["pred"] for r in read_jsonl(PRED_DIR / f"{slug(name)}.jsonl")}
        for bname, pool in breakdowns(recs, gold):
            c = score(pool, preds)
            for (setting, match, label), (tp_p, n_pred, tp_r, n_gold) in sorted(c.items()):
                p, r, f = prf(tp_p, n_pred, tp_r, n_gold)
                rows.append({"model": name, "setting": setting, "match": match, "breakdown": bname,
                             "n_texts": len(pool), "label": label,
                             "P": None if p is None else round(p, 4), "R": None if r is None else round(r, 4),
                             "F1": None if f is None else round(f, 4),
                             "tp_pred": tp_p, "n_pred": n_pred, "tp_gold": tp_r, "n_gold": n_gold})
        analysis[name] = {"all": error_analysis(recs, preds, gold),
                          "gold": error_analysis([r for r in recs if r["id"] in gold], preds, gold)}
    with open(RESULTS / "metrics.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (RESULTS / "error_analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"metrics rows: {len(rows)}")


if __name__ == "__main__":
    main()
