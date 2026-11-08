# API (FastAPI)

İskelet. Şu an çalışan tek uç: `GET /health` → `{"status": "ok"}`.

| Uç | Dosya | Durum |
|---|---|---|
| `GET /health` | `app/main.py` | çalışıyor |
| `POST /recommendations` | `app/routers/recommendations.py` | planlandı (501) |
| `POST /qa` | `app/routers/qa.py` | planlandı (501) |
| `GET /review-queue` | `app/routers/review.py` | planlandı (501) |
| `POST /imports` | `app/routers/imports.py` | planlandı (501) |

Router dosyaları yer tutucudur ve bilerek `app/main.py`'ye bağlanmamıştır.

## Yerel geliştirme (Python 3.11)

```bash
python -m venv .venv
# Linux/macOS : source .venv/bin/activate
# PowerShell  : .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload      # http://localhost:8000/health
pytest
ruff check . && ruff format --check .
```

CORS kaynakları `API_CORS_ORIGINS` ortam değişkeninden (virgülle ayrılmış) okunur.
