"""Run the whole Experiment A pipeline end to end.

    python experiments/deney-a-ner-baseline/run_all.py
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

STEPS = [
    ("1/7 veri doğrulama", "validate_data.py"),
    ("2/7 gold aday seçimi", "select_gold.py"),
    ("3/7 gold düzeltmeleri", "gold_review_edits.py"),
    ("4/7 veri doğrulama (düzeltmelerle)", "validate_data.py"),
    ("5/7 NER çıkarımı", "ner_baseline.py"),
    ("6/7 değerlendirme", "evaluate.py"),
    ("7/7 rapor", "make_report.py"),
]

if __name__ == "__main__":
    for title, script in STEPS:
        print(f"== {title}: {script}", flush=True)
        runpy.run_path(str(HERE / script), run_name="__main__")
