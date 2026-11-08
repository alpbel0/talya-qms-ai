"""Draw the stratified subset that is reviewed by hand to form the gold set.

Picks 3 rows per (doc_type x difficulty group) cell -> 4 x 5 x 3 = 60 ids, with a
fixed seed. Writes data/synthetic/gold_candidates.txt and a readable review sheet
data/synthetic/gold_review.md. It never touches data/synthetic/gold_ids.txt: that file is written
only after the review, from the ids that passed it.
"""
import random
from collections import defaultdict

from common import DATA, DIFF_GROUP, SEED, load_clean

PER_CELL = 3


def main():
    recs = load_clean()
    cells = defaultdict(list)
    for r in recs:
        cells[(r["doc_type"], DIFF_GROUP[r["difficulty"][0]])].append(r)
    rng = random.Random(SEED)
    chosen = []
    for key in sorted(cells):
        pool = sorted(cells[key], key=lambda r: r["id"])
        chosen += rng.sample(pool, min(PER_CELL, len(pool)))
    chosen.sort(key=lambda r: r["id"])

    (DATA / "gold_candidates.txt").write_text("\n".join(r["id"] for r in chosen) + "\n", encoding="utf-8")

    lines = ["# Gold aday alt kümesi — inceleme tablosu", "",
             f"{len(chosen)} satır, her doc_type × zorluk grubu hücresinden {PER_CELL} adet (seed={SEED}).", ""]
    for r in chosen:
        lines += [f"## {r['id']}  ·  {'|'.join(r['difficulty'])}", "", f"> {r['text']}", "",
                  "| Varlık | Etiket |", "|---|---|"]
        lines += [f"| {e['text']} | {e['label']} |" for e in r["entities"]]
        lines += ["", "İlişkiler:" if r["relations"] else "İlişkiler: *(yok)*"]
        lines += [f"- {x['head']} —{x['type']}→ {x['tail']}" for x in r["relations"]]
        lines.append("")
    (DATA / "gold_review.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"selected {len(chosen)} candidates")


if __name__ == "__main__":
    main()
