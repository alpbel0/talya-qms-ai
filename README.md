# Talya QMS-AI

Otel kalite yönetimi için **ontoloji + bilgi grafı + Türkçe bilgi çıkarımı + RAG tabanlı DÖF
(düzeltici/önleyici faaliyet) öneri sistemi**. Akdeniz Üniversitesi CSE 491 bitirme projesi.

Amaç: otellerde serbest metin olarak tutulan uygunsuzluk, şikâyet, denetim ve bakım kayıtlarından
varlıkları (departman, ekipman, KPI, olay, kök neden, aksiyon) ve aralarındaki neden-sonuç
ilişkilerini çıkarmak, bunları bir bilgi grafında birleştirmek ve benzer geçmiş vakalara
dayanarak yeni uygunsuzluklar için DÖF önerileri üretmek. Yapay zekâ bileşenlerinin yerel
çalışacak şekilde (Ollama) kurgulanması hedeflenmektedir.

> **Durum: tasarım aşamasında.** Bu depo bir **proje iskeletidir**. Çalışan tek parçalar,
> ön çalışma niteliğindeki [Deney A](experiments/deney-a-ner-baseline) (hazır Türkçe NER
> modellerinin ölçümü) ile API'deki `GET /health` ucudur. Ontoloji, bilgi çıkarımı, RAG ve içe
> aktarma modülleri **henüz yazılmamıştır**; arayüzdeki sayfalar boştur.

## Mimari özeti

Sistem dört katmandan oluşur (ayrıntı: [docs/architecture.md](docs/architecture.md)):

1. **Veri katmanı** — CSV/Excel içe aktarma, doğrulama ve anonimleştirme (`ingestion/`).
2. **Bilgi katmanı** — HQMO ontolojisi, Türkçe NER + ilişki çıkarımı, Neo4j bilgi grafı ve vektör indeksi (`ontology/`, `extraction/`, Neo4j).
3. **Analitik katman** — RAG ile DÖF önerisi, soru-cevap, risk ve nedensellik analizi (`rag/`, yerel LLM/Ollama).
4. **Etkileşim katmanı** — FastAPI servisi ve React arayüzü (`api/`, `ui/`).

## Klasör yapısı

```
.
├── README.md, CONTRIBUTING.md, LICENSE
├── docker-compose.yml, .env.example
├── docs/                 # mimari dokümanı, görseller
├── ontology/             # HQMO ontolojisi (OWL 2 DL)             - planlandı
├── extraction/           # Türkçe NER + neden-sonuç çıkarımı       - planlandı
├── rag/                  # RAG / DÖF öneri motoru (neo4j-graphrag) - planlandı
├── ingestion/            # CSV/Excel içe aktarma + anonimleştirme  - planlandı
├── api/                  # FastAPI iskeleti (yalnızca /health çalışır)
├── ui/                   # React + TypeScript (Vite) iskeleti, boş sayfalar
├── experiments/
│   └── deney-a-ner-baseline/   # Deney A: hazır BERTurk NER ölçümü
├── data/synthetic/       # yalnızca sentetik veri
└── .github/workflows/ci.yml
```

## Kurulum

Gereksinimler: Git, Docker (Compose v2). Komutlar Windows PowerShell ve Linux/macOS'ta aynıdır;
tek fark `.env` kopyalama satırıdır.

```bash
git clone https://github.com/alpbel0/talya-qms-ai.git
cd talya-qms-ai

# .env.example dosyasını .env olarak kopyalayın ve parolayı değiştirin
cp .env.example .env              # Linux/macOS
# Copy-Item .env.example .env     # PowerShell

docker compose up --build
```

| Servis | Adres |
|---|---|
| UI | http://localhost:3000 |
| API (`/health`, `/docs`) | http://localhost:8000 |
| Neo4j Browser | http://localhost:7474 |
| Ollama | http://localhost:11434 |

Notlar: Neo4j eklentileri (APOC, neosemantics) ilk açılışta indirilir, bu yüzden internet gerekir.
Ollama'ya henüz model yüklenmez; model seçimi tasarım aşamasındadır.

Bileşenleri tek tek çalıştırmak için bkz. [api/README.md](api/README.md) ve [ui/README.md](ui/README.md).

## Deneyi çalıştırma (Deney A)

Deney Docker dışında, yerelde çalışır; ilk çalıştırmada iki Hugging Face modeli (~0.9 GB) iner.
Ayrıntı: [experiments/deney-a-ner-baseline/README.md](experiments/deney-a-ner-baseline/README.md).

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate      PowerShell: .venv\Scripts\Activate.ps1
pip install -r experiments/deney-a-ner-baseline/requirements.txt
python experiments/deney-a-ner-baseline/run_all.py
```

Windows'ta Türkçe karakter hatası alırsanız `python -X utf8 experiments/deney-a-ner-baseline/run_all.py`
kullanın. Sonuç raporu: `experiments/deney-a-ner-baseline/results/report.md`. Deney CI'ya dahil değildir.

## Proje durumu

İş paketi tanımları proje önerisinden (CSE 491 Project Proposal, Grup 17) alınmıştır.

| İş paketi | Kapsam | Durum |
|---|---|---|
| WP1 | Gereksinimler, HQMO ontolojisi (USALI / ISO 9001 / GSTC / KPI modülleri), graf veritabanı kurulumu | **Devam ediyor (%30):** gereksinimler, mimari ve veri modeli tasarlandı; ontoloji kaynak doküman incelemesi sürüyor; ontoloji ve Neo4j şeması başlamadı |
| WP2 | Türkçe veri seti (toplama, anonimleştirme, etiketleme); varlık ve neden-sonuç çıkarımı (ince ayarlı model ve LLM few-shot karşılaştırması); bilgi grafını doldurma | **Devam ediyor (%20):** etiket şeması, 300 metinlik sentetik veri seti, 60 metinlik doğrulanmış altın alt küme ve baseline deney (Deney A) tamam; gerçek veri, ince ayar ve LLM karşılaştırması başlamadı |
| WP3 | Zamansal nedensellik keşfi: KPI'lar arası gecikmeli ilişkiler (PCMCI+) | **Başlamadı** (gelecek dönem) |
| WP4 | Hibrit kalite grafı; GNN ile anomali tespiti ve departman bazlı risk skorları | **Başlamadı** (gelecek dönem) |
| WP5 | RAG tabanlı DÖF öneri motoru (benzer vaka, olası kök neden, kaynaklı aksiyon) | **Tasarımda (%10):** teknoloji seçimi yapıldı, kod yok |
| WP6 | Role dayalı Türkçe raporlama (şablon güdümlü LLM, sayısal tutarlılık denetimi) | **Başlamadı** (gelecek dönem) |
| WP7 | Servis entegrasyonu, demo arayüzü, performans testi ve değerlendirme | **Başladı (%5):** repo iskeleti, CI ve Docker Compose kuruldu ve doğrulandı |

Depo bileşenlerinin gerçek durumu:

| Bileşen | Durum |
|---|---|
| Deney A (hazır NER ölçümü, sentetik veri) | Ön çalışma tamamlandı; sonuçlar `results/` altında |
| API | İskelet; yalnızca `GET /health`, diğer uçlar 501 |
| UI | İskelet; 9 boş sayfa, işlev yok |
| Docker Compose / CI | Yapılandırıldı |
| Ontoloji, bilgi çıkarımı, RAG, içe aktarma | **Planlandı**, kod yok |

## Veri ve gizlilik

Gerçek otel verisi, demo otel verisi, API anahtarı veya kişisel veri **repoya asla girmez**.
Gerçek veri yalnızca **anonimleştirildikten sonra ve yalnızca yerelde** işlenir. `.gitignore`
`data/synthetic/` dışındaki tüm veri yollarını yok sayar. Repodaki tek veri sentetik veridir.

## Ekip

- Yiğitalp Bel
- Kenan Akar

Danışman: Prof. Dr. Alper Bilge — Akdeniz Üniversitesi, CSE 491 (Bitirme Projesi).

## Lisans

Tüm hakları saklıdır; açık kaynak değildir. Bkz. [LICENSE](LICENSE).
