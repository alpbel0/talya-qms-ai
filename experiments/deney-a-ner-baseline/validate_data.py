"""Step 1: validate the synthetic CSV, add character offsets, write statistics.

Outputs:
  data/synthetic/clean.jsonl          valid rows, entities with first-occurrence offsets
  data/synthetic/invalid_rows.csv     rows that failed validation (+ reason column)
  results/data_stats.json   distribution statistics
"""
import csv
import json
from collections import Counter

from common import (CLEAN_JSONL, DIFF_GROUP, DIFFICULTIES, GOLD_CORRECTIONS,
                    HEADER, INVALID_CSV, LABELS, RAW_CSV, REL_TYPES, RESULTS,
                    load_gold_ids, read_csv)


def check_row(row, corrections):
    rid, doc_type, text, difficulty, ents_s, rels_s = row
    problems = []
    try:
        ents = json.loads(ents_s)
        rels = json.loads(rels_s)
    except json.JSONDecodeError as e:
        return None, [f"JSON parse error: {e}"]

    corrected = rid in corrections
    if corrected:
        ents = corrections[rid]["entities"]
        rels = corrections[rid]["relations"]

    diffs = difficulty.split("|")
    bad = [d for d in diffs if d not in DIFFICULTIES]
    if bad:
        problems.append(f"unknown difficulty {bad}")

    entities, seen = [], {}
    for e in ents:
        t, lab = e.get("text"), e.get("label")
        if lab not in LABELS:
            problems.append(f"unknown label {lab!r} for {t!r}")
        start = text.find(t) if t else -1
        if start < 0:
            problems.append(f"entity not an exact substring: {t!r}")
            continue
        if t in seen:
            continue  # spec: list each surface string once
        seen[t] = lab
        entities.append({"text": t, "label": lab, "start": start, "end": start + len(t)})

    relations = []
    for r in rels:
        h, typ, tl = r.get("head"), r.get("type"), r.get("tail")
        if typ not in REL_TYPES:
            problems.append(f"unknown relation type {typ!r}")
            continue
        if h not in seen or tl not in seen:
            problems.append(f"relation head/tail not in entities: {h!r} -> {tl!r}")
            continue
        heads, tails = REL_TYPES[typ]
        if seen[h] not in heads or seen[tl] not in tails:
            problems.append(f"relation direction {seen[h]}-{typ}->{seen[tl]} not in schema")
            continue
        relations.append({"head": h, "type": typ, "tail": tl})

    rec = {"id": rid, "doc_type": doc_type, "text": text, "difficulty": diffs,
           "entities": entities, "relations": relations, "corrected": corrected}
    return rec, problems


def main():
    rows = read_csv(RAW_CSV)
    corrections = {}
    if GOLD_CORRECTIONS.exists():
        corrections = json.loads(GOLD_CORRECTIONS.read_text(encoding="utf-8"))

    clean, invalid = [], []
    for row in rows:
        if len(row) != len(HEADER):
            invalid.append(row + [f"expected {len(HEADER)} columns, got {len(row)}"])
            continue
        rec, problems = check_row(row, corrections)
        if problems:
            invalid.append(row + ["; ".join(problems)])
        else:
            clean.append(rec)

    with open(CLEAN_JSONL, "w", encoding="utf-8") as f:
        for r in clean:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(INVALID_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(HEADER + ["reason"])
        w.writerows(invalid)

    gold = load_gold_ids()

    def stats(recs):
        return {
            "n_texts": len(recs),
            "doc_type": dict(Counter(r["doc_type"] for r in recs)),
            "difficulty_tag": dict(Counter(d for r in recs for d in r["difficulty"])),
            "difficulty_primary": dict(Counter(r["difficulty"][0] for r in recs)),
            "difficulty_group": dict(Counter(DIFF_GROUP[r["difficulty"][0]] for r in recs)),
            "entity_label": dict(Counter(e["label"] for r in recs for e in r["entities"])),
            "relation_type": dict(Counter(x["type"] for r in recs for x in r["relations"])),
            "n_entities": sum(len(r["entities"]) for r in recs),
            "n_relations": sum(len(r["relations"]) for r in recs),
            "avg_words": round(sum(len(r["text"].split()) for r in recs) / max(len(recs), 1), 1),
        }

    out = {
        "source": str(RAW_CSV.relative_to(RAW_CSV.parent.parent)),
        "n_rows_raw": len(rows),
        "n_invalid": len(invalid),
        "n_valid": len(clean),
        "n_gold_corrected": sum(r["corrected"] for r in clean),
        "all": stats(clean),
        "gold": stats([r for r in clean if r["id"] in gold]) if gold else None,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "data_stats.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"raw={len(rows)} valid={len(clean)} invalid={len(invalid)} "
          f"gold={len(gold)} corrected={out['n_gold_corrected']}")
    for row in invalid:
        print("  INVALID", row[0], "->", row[-1])


if __name__ == "__main__":
    main()
