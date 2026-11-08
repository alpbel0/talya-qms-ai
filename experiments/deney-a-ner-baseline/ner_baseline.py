"""Experiment A: run off-the-shelf BERTurk NER models (PER/ORG/LOC) on every text.

Models are pinned to exact Hub commits so the run is reproducible. Writes one
JSONL of raw predictions per model to results/predictions/ and run metadata to
results/ner_run_meta.json.
"""
import json
import platform
import time

import torch
import transformers
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from common import PRED_DIR, RESULTS, load_clean, write_jsonl

AGGREGATION = "first"  # word-level: a word takes its first sub-token's label

MODELS = {
    "akdeniz27/bert-base-turkish-cased-ner": "99995f7d2be4b3a28c74f0d36ee97f8c04ee0571",
    "savasy/bert-base-turkish-ner-cased": "7678083d645af39967e0ebe8213a6049deb6e2cc",
}


def slug(name):
    return name.replace("/", "__")


def hardware():
    info = {"platform": platform.platform(), "processor": platform.processor(),
            "python": platform.python_version(), "torch": torch.__version__,
            "transformers": transformers.__version__,
            "cuda_available": torch.cuda.is_available(), "device": "cpu",
            "torch_threads": torch.get_num_threads()}
    try:
        import psutil
        info["ram_gb"] = round(psutil.virtual_memory().total / 2**30, 1)
        info["logical_cpus"] = psutil.cpu_count()
    except ImportError:
        pass
    try:  # human-readable CPU name on Windows
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        info["cpu_name"] = winreg.QueryValueEx(k, "ProcessorNameString")[0].strip()
    except (ImportError, OSError):
        pass
    return info


def main():
    torch.manual_seed(0)
    recs = load_clean()
    meta = {"hardware": hardware(), "models": {}}
    for name, rev in MODELS.items():
        tok = AutoTokenizer.from_pretrained(name, revision=rev)
        model = AutoModelForTokenClassification.from_pretrained(name, revision=rev)
        model.eval()
        ner = pipeline("token-classification", model=model, tokenizer=tok,
                       aggregation_strategy=AGGREGATION, device=-1)
        t0 = time.perf_counter()
        out = []
        with torch.no_grad():
            for r in recs:
                preds = []
                for p in ner(r["text"]):
                    s, e = int(p["start"]), int(p["end"])
                    preds.append({"text": r["text"][s:e], "label": p["entity_group"],
                                  "start": s, "end": e, "score": round(float(p["score"]), 4)})
                out.append({"id": r["id"], "text": r["text"], "pred": preds})
        secs = time.perf_counter() - t0
        write_jsonl(PRED_DIR / f"{slug(name)}.jsonl", out)
        meta["models"][name] = {
            "revision": rev, "labels": sorted(set(model.config.id2label.values())),
            "base": getattr(model.config, "_name_or_path", None),
            "n_texts": len(recs), "n_pred": sum(len(o["pred"]) for o in out),
            "seconds": round(secs, 1), "sec_per_text": round(secs / len(recs), 4),
            "fast_tokenizer": tok.is_fast, "aggregation_strategy": AGGREGATION,
        }
        print(f"{name}: {meta['models'][name]['n_pred']} spans in {secs:.1f}s")
    (RESULTS / "ner_run_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
