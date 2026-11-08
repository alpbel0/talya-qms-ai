"""Shared paths, schema constants, and data helpers."""
import csv
import json
from pathlib import Path

# Bu dosya: <repo>/experiments/deney-a-ner-baseline/common.py
EXP_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXP_DIR.parents[1]
DATA = REPO_ROOT / "data" / "synthetic"   # girdi + türetilmiş ara dosyalar (yalnızca sentetik)
RESULTS = EXP_DIR / "results"
PRED_DIR = RESULTS / "predictions"

RAW_CSV = DATA / "synthetic_hotel_quality.csv"
GOLD_IDS = DATA / "gold_ids.txt"
GOLD_CORRECTIONS = DATA / "gold_corrections.json"
INVALID_CSV = DATA / "invalid_rows.csv"
CLEAN_JSONL = DATA / "clean.jsonl"

HEADER = ["id", "doc_type", "text", "difficulty", "entities", "relations"]
LABELS = ["DEPARTMENT", "EQUIPMENT", "KPI", "EVENT", "ROOT_CAUSE", "ACTION"]
REL_TYPES = {
    "CAUSES": ({"ROOT_CAUSE", "EVENT", "EQUIPMENT"}, {"EVENT"}),
    "ADDRESSED_BY": ({"EVENT", "ROOT_CAUSE"}, {"ACTION"}),
    "OCCURS_IN": ({"EVENT"}, {"DEPARTMENT"}),
}
DIFFICULTIES = ["explicit", "implicit", "multi_cause", "chain",
                "abbreviation", "informal", "negative"]

# The five groups used for the original 8/7/5/5 design (multi_cause and chain
# share a group, as do the three "challenging" kinds except negative).
DIFF_GROUP = {
    "explicit": "explicit", "implicit": "implicit",
    "multi_cause": "multi_cause/chain", "chain": "multi_cause/chain",
    "abbreviation": "abbreviation/informal", "informal": "abbreviation/informal",
    "negative": "negative",
}

SEED = 42


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if rows[0] != HEADER:
        raise ValueError(f"unexpected header in {path}: {rows[0]}")
    return rows[1:]


def load_clean():
    with open(CLEAN_JSONL, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_gold_ids():
    if not GOLD_IDS.exists():
        return set()
    return {l.strip() for l in GOLD_IDS.read_text(encoding="utf-8").splitlines() if l.strip()}


def primary_difficulty(rec):
    return rec["difficulty"][0]


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]
