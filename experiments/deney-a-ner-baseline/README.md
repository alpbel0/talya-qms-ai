# Otel kalite metinlerinde NER — Deney A

Sentetik Türkçe otel kalite metinleri (`../../data/synthetic/synthetic_hotel_quality.csv`, 300 satır) üzerinde hazır
BERTurk NER modellerinin bizim varlık şemamızdaki (DEPARTMENT, EQUIPMENT, KPI, EVENT, ROOT_CAUSE, ACTION)
neyi yakalayıp neyi kaçırdığını ölçer. Sonuç raporu: `results/report.md`.

Yalnızca Deney A (hazır NER) kapsamdadır; LLM deneyi (Deney B) bu çalışmada çalıştırılmadı.

## Kurulum

Python 3.11 ile test edildi. GPU gerekmez (CPU'da ~30 sn).

Depo kökünden, sanal ortamla (PowerShell ve Linux/macOS için ayrı satırlar):

```bash
python -m venv .venv
# Linux/macOS : source .venv/bin/activate
# PowerShell  : .venv\Scripts\Activate.ps1
pip install -r experiments/deney-a-ner-baseline/requirements.txt
```

İlk çalıştırmada iki model Hugging Face Hub'dan indirilir (~0.9 GB), internet gerekir.

## Çalıştırma (tek komut)

```bash
python experiments/deney-a-ner-baseline/run_all.py
```

Windows konsolunda Türkçe karakter hatası alırsanız: `python -X utf8 experiments/deney-a-ner-baseline/run_all.py`.

Girdi ve türetilmiş ara veri dosyaları depo kökündeki `data/synthetic/` altındadır;
çıktılar bu klasördeki `results/` altına yazılır. Bu deney CI'ya dahil değildir (model indirmesi gerektirir).

## Adımlar

| Adım | Script | Çıktı |
|---|---|---|
| Veri doğrulama, offset ekleme, istatistik | `validate_data.py` | `data/synthetic/clean.jsonl`, `data/synthetic/invalid_rows.csv`, `results/data_stats.json` |
| Gold aday seçimi (4 doc_type × 5 zorluk grubu × 3, seed=42) | `select_gold.py` | `data/synthetic/gold_candidates.txt`, `data/synthetic/gold_review.md` |
| Gold düzeltmeleri (kayıtlı, gerekçeli) | `gold_review_edits.py` | `data/synthetic/gold_corrections.json`, `data/synthetic/gold_ids.txt` |
| NER çıkarımı (commit'e sabitli 2 model) | `ner_baseline.py` | `results/predictions/*.jsonl`, `results/ner_run_meta.json` |
| Değerlendirme + hata analizi | `evaluate.py` | `results/metrics.csv`, `results/error_analysis.json` |
| Rapor | `make_report.py` | `results/report.md` |

## `results/metrics.csv` kolonları

`model, setting, match, breakdown, n_texts, label, P, R, F1, tp_pred, n_pred, tp_gold, n_gold`

- `setting`: `span_only` (etiketten bağımsız örtüşme) veya `map_ORG=DEPARTMENT` (önceden sabit eşleme)
- `match`: `exact` (metin + etiket aynı) veya `partial` (span örtüşmesi + aynı etiket)
- `breakdown`: `all`, `gold`, `all|difficulty=<tür>`, `gold|difficulty=<tür>`, `all|doc_type=<tür>`
- P/R boş ise tanımsızdır (payda 0).

## Önemli uyarı

Gold alt küme Claude ile incelenmiştir, insan doğrulaması değildir. Ayrıntılar `results/report.md` §1 ve §2.1'de.
