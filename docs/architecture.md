# Mimari

> **Durum:** Bu belge **hedef mimariyi** anlatır. Proje tasarım aşamasındadır. Bileşenlerden
> yalnızca `api` (yalnızca `/health`) ve `ui` (boş sayfalar) iskelet olarak mevcuttur; Docker
> Compose'ta Neo4j ve Ollama servisleri tanımlıdır ama içlerinde şema ya da model yoktur.
> Diğerleri **planlandı**.

## Katmanlar

| Katman | Bileşenler |
|---|---|
| Veri | `ingestion` |
| Bilgi | `ontology`, `extraction`, Neo4j bilgi grafı + vektör indeksi |
| Analitik | `rag`, yerel LLM (Ollama) |
| Etkileşim | `api`, `ui` |

## Akış (hedef)

```
CSV/Excel --> ingestion --> extraction --> Neo4j (bilgi grafı + vektör indeksi)
 (anonim)    (doğrula,     (NER + neden-         ^              |
              anonimleştir) sonuç ilişkisi)       |              v
                              ontology -----------+        rag <--> Ollama (yerel LLM)
                           (şema / kısıtlar)                  |
                                                              v
                                                      api (FastAPI) --> ui (React)
```

## Bileşenler ve sorumlulukları

| Bileşen | Sorumluluk | Durum |
|---|---|---|
| **ingestion** | CSV/Excel dosyalarını okur, şemaya göre doğrular, kişisel veriyi anonimleştirir, temiz kayıtları bilgi katmanına iletir. Gerçek veri yalnızca anonim ve yerelde işlenir. | planlandı |
| **ontology** | HQMO (Hotel Quality Management Ontology), OWL 2 DL: varlık sınıfları (DEPARTMENT, EQUIPMENT, KPI, EVENT, ROOT_CAUSE, ACTION), ilişkiler (ör. CAUSES, ADDRESSED_BY, OCCURS_IN) ve kısıtlar. Graf şemasının ve çıkarım etiketlerinin tek kaynağı olması hedeflenir. | planlandı |
| **extraction** | Türkçe serbest metinden varlık (NER) ve neden-sonuç ilişkisi çıkarır; ontoloji ile uyumlu çıktı üretir. Düşük güvenli sonuçlar onay kuyruğuna gider. Ön çalışma: Deney A (hazır NER modellerinin bu şemayı ne kadar karşıladığını ölçer). | planlandı |
| **Neo4j bilgi grafı + vektör indeksi** | Vakaları, varlıkları ve ilişkileri saklar; vektör indeksi benzer vaka aramasını sağlar. APOC ve neosemantics (n10s; RDF/OWL içe aktarma) eklentileri kullanılır. | Compose'ta tanımlı, şema yok |
| **rag** | `neo4j-graphrag` ile graf + vektör araması yapar; bulunan benzer vakaları ve nedenleri LLM'e bağlam olarak verip DÖF önerisi ve soru-cevap yanıtı üretir; kaynak vakaları gösterir. | planlandı |
| **Yerel LLM (Ollama)** | Metin üretimi ve (gerekirse) gömme (embedding) için yerel çıkarım; veri makineyi terk etmez. Model seçimi henüz yapılmadı. | Compose'ta tanımlı, model yok |
| **api** | FastAPI servisi: `/recommendations`, `/qa`, `/review-queue`, `/imports` uçları ve `/health`. | iskelet (yalnızca `/health`) |
| **ui** | React + TypeScript arayüzü: panel, departmanlar, yeni uygunsuzluk, vakalar, soru-cevap, graf gezgini, onay kuyruğu, veri yükleme, risk ve nedensellik. | iskelet (boş sayfalar) |

## Veri ve gizlilik ilkeleri

- Repoya yalnızca sentetik veri girer (`data/synthetic/`).
- Gerçek veri anonimleştirilmeden işlenmez ve makineden dışarı çıkmaz (yerel LLM tercihinin nedeni).
- Parolalar ve anahtarlar yalnızca `.env` dosyasındadır (commit'lenmez).

## Deneyler

`experiments/` altındaki çalışmalar ürün kodu değildir ve CI'ya dahil edilmez. Deney A: sentetik
300 satırlık metin üzerinde iki hazır BERTurk NER modelinin ölçümü
(bkz. `experiments/deney-a-ner-baseline/results/report.md`).
