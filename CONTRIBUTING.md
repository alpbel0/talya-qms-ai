# Katkı Rehberi

## Çalışma akışı: GitHub Flow

- `main` dalı **her zaman çalışır durumda** olmalıdır. Doğrudan `main`'e commit atılmaz.
- Her iş, `main`'den açılan **`feature/<kısa-ad>`** dalında yapılır (ör. `feature/ontoloji-iskelet`,
  `feature/ingestion-csv`).
- İş bitince pull request açılır ve **diğer ekip üyesinin onayıyla** birleştirilir. Kendi PR'ınızı
  onaylamayın.
- Birleştirmeden önce CI (api: ruff + pytest, ui: lint + build) yeşil olmalıdır.

```bash
git switch main && git pull
git switch -c feature/kisa-ad
# ... çalış, commit'le ...
git push -u origin feature/kisa-ad     # sonra GitHub'da pull request aç
```

## Commit mesajları: Conventional Commits

Biçim: `<tür>(<isteğe bağlı kapsam>): <kısa açıklama>`

| Tür | Kullanım | Örnek |
|---|---|---|
| `feat` | yeni özellik | `feat(api): /review-queue ucunu uygula` |
| `fix` | hata düzeltme | `fix(ui): menüde aktif sayfa vurgusu` |
| `docs` | dokümantasyon | `docs: mimari belgesine RAG akışını ekle` |
| `chore` | bakım, yapılandırma | `chore(docker): neo4j etiketini güncelle` |
| `ci` | CI/CD | `ci: ui işine önbellek ekle` |
| `exp` | deney / araştırma kodu | `exp: Deney B için LLM çıkarım scripti` |
| `test` | testler | `test(api): imports uçları için test` |
| `refactor` | davranışı değiştirmeyen yeniden düzenleme | `refactor(extraction): ortak yardımcıları ayır` |

## Veri kuralları (çok önemli)

- **Gerçek otel verisi, demo otel verisi, kişisel veri, API anahtarı, parola ve `.env`
  dosyaları asla commit'lenmez.** Yanlışlıkla commit'lendiyse geçmişten de temizlenmesi gerekir;
  hemen ekibe haber verin.
- Repoya yalnızca **sentetik** veri girer ve yalnızca `data/synthetic/` altına konur.
- Gerçek veri yalnızca anonimleştirilmiş hâliyle ve yalnızca yerel makinede işlenir.
- Örnek ayarlar `.env.example` içinde, **yalnızca örnek değerlerle** tutulur.
- Bağımlılık ve Docker imaj sürümleri sabitlenir (`latest` ve sürüm aralığı kullanılmaz); yeni
  sürüm seçerken yayınlanmasının üzerinden en az iki hafta geçmiş olmasına dikkat edin.

## Yerel kontroller

```bash
# API (api/ içinde)
ruff check . && ruff format --check . && pytest
# UI (ui/ içinde)
npm ci && npm run lint && npm run build
```
