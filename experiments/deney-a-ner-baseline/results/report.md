# Deney A Raporu: Hazır Türkçe NER Modellerinin Otel Kalite Metinlerindeki Performansı

> Bu rapor `experiments/make_report.py` tarafından otomatik üretilmiştir. Tablolardaki tüm sayılar `results/metrics.csv`, `results/error_analysis.json`, `results/data_stats.json` ve `results/ner_run_meta.json` dosyalarından okunur.

## Özet

- **`akdeniz27/bert-base-turkish-cased-ner`** (gold, n=60): bizim varlıklarımızın yalnızca **5.3%**'ine herhangi bir span ile dokunuyor (tahminlerinin 93.8%'i bir varlığımızla örtüşüyor). ORG → DEPARTMENT eşlemesiyle DEPARTMENT F1 = 0.203 (exact) / 0.430 (partial); 6 etiket MICRO F1 = 0.049 / 0.100.
- **`savasy/bert-base-turkish-ner-cased`** (gold, n=60): bizim varlıklarımızın yalnızca **20.2%**'ine herhangi bir span ile dokunuyor (tahminlerinin 94.2%'i bir varlığımızla örtüşüyor). ORG → DEPARTMENT eşlemesiyle DEPARTMENT F1 = 0.404 (exact) / 0.586 (partial); 6 etiket MICRO F1 = 0.136 / 0.194.
- EVENT, ROOT_CAUSE, KPI ve ACTION varlıkları — yani nedensellik analizinin asıl taşıyıcıları — genel amaçlı NER tarafından neredeyse hiç görülmüyor (§5, §6.5).
- Yakalanan şey büyük ölçüde büyük harfle yazılmış departman ve sistem adları/kısaltmaları; ORG etiketi departman, ekipman ve süreç kısaltmalarını ayırt etmiyor (§6.3).
- Sentetik etiketlerin kalitesi de bir bulgu: gold incelemesinde satırların 19/60'ında eksik/hatalı etiket bulundu (§2.1).

## 1. Kapsam ve önemli uyarılar

- **Yalnızca Deney A (hazır BERTurk NER) çalıştırıldı.** Planlanan Deney B (yerel LLM ile zero-/few-shot çıkarım) proje sahibinin kararıyla bu çalışmanın **kapsamı dışında bırakıldı**; çalıştırılmadı ve bu raporda LLM sonucu yoktur.
- **İlişki çıkarımı ölçülmedi.** NER modelleri yalnızca varlık sınırı + PER/ORG/LOC etiketi üretir; (head, type, tail) üçlüsü üretmedikleri için ilişki P/R/F1 bu deney için *uygulanamaz*. Dolayısıyla "örtük nedensellik yakalandı mı" ve "negatiflerde uydurma ilişki" soruları bu deneyle yanıtlanamaz (bkz. §6.5).
- **Etiketler LLM üretimidir.** Veri seti ve etiketleri Claude Sonnet 5.5 ile sentetik olarak üretildi. Tüm set sonuçları bu otomatik etiketlere dayanır.
- **Gold alt küme insan doğrulaması değildir.** 60 satırlık alt küme Claude (Opus 5.5) tarafından satır satır incelenip 19 satırı düzeltildi. İnceleyen model, üreten modelle aynı ailedendir; ortak hataları gözden kaçırmış olabilir. Bitirme raporunda bu alt kümenin en azından bir kısmının insan tarafından kontrol edilmesi önerilir (`data/synthetic/gold_review.md`).
- **Model etiket uzayı uyuşmuyor.** Modeller bizim 6 etiketimizi bilmez; amaç skor değil, neyin yakalanıp neyin kaçırıldığını göstermektir. Bu yüzden iki ayar raporlanır (§4).

## 2. Veri

- Kaynak: `data/synthetic/synthetic_hotel_quality.csv`, 300 satır.
- Doğrulama: her entity metninin metinde birebir alt dize olması, her relation head/tail'inin entities içinde olması, etiket/ilişki türü ve yönünün şemaya uyması kontrol edildi. **Hatalı satır: 0** (`data/synthetic/invalid_rows.csv`), teste giren satır: 300.
- Her entity'e metindeki ilk geçtiği yerin karakter offset'i (`start`, `end`) eklendi (`data/synthetic/clean.jsonl`). Partial eşleşmede bir entity'nin metindeki *tüm* geçişleri dikkate alınır.
- Ortalama metin uzunluğu: 15.2 kelime.

**Dağılım (tüm set / gold):**

| doc_type | Tüm set | Gold |
|---|---|---|
| BAKIM | 75 | 15 |
| DENETIM | 75 | 15 |
| DOF | 75 | 15 |
| SIKAYET | 75 | 15 |

| difficulty etiketi* | Tüm set | Gold |
|---|---|---|
| explicit (açık) | 104 | 15 |
| implicit (örtük) | 95 | 15 |
| multi_cause (çoklu neden) | 33 | 5 |
| chain (zincir) | 37 | 10 |
| abbreviation (kısaltma) | 23 | 9 |
| informal (günlük dil) | 14 | 3 |
| negative (negatif) | 24 | 12 |

\* Birleşik etiketli satırlar (örn. `abbreviation|implicit`) her bileşende sayılır.

| Varlık etiketi | Tüm set | Gold |
|---|---|---|
| DEPARTMENT | 207 | 43 |
| EQUIPMENT | 145 | 29 |
| KPI | 29 | 10 |
| EVENT | 410 | 85 |
| ROOT_CAUSE | 249 | 46 |
| ACTION | 68 | 15 |
| **Toplam** | 1108 | 228 |

| İlişki türü | Tüm set | Gold |
|---|---|---|
| CAUSES | 438 | 90 |
| ADDRESSED_BY | 64 | 14 |
| OCCURS_IN | 137 | 24 |
| **Toplam** | 639 | 128 |

### 2.1 Gold alt küme

Her doc_type × zorluk grubu (açık, örtük, çoklu/zincir, kısaltma/günlük dil, negatif) hücresinden 3 satır sabit tohumla (seed=42) seçildi: 4 × 5 × 3 = 60 satır. Her satır okunup etiketleri kontrol edildi; **19/60 satırda (32%) düzeltme gerekti.** Düzeltmeler ham CSV'yi değiştirmez; `data/synthetic/gold_corrections.json` içinde gerekçesiyle tutulur ve doğrulama adımında uygulanır (düzeltilmiş satırlar tüm set hesaplarında da düzeltilmiş hâliyle yer alır).

Bu oran, üretici LLM'in etiketlerinin en çok **zincirin ara/son halkasını** ve **departman/aksiyon bağlantılarını atladığını** gösteriyor:

| id | Düzeltme gerekçesi |
|---|---|
| BAKIM-004 | Zincirde su sızıntısı → pano atması → karartma halkası eksikti. |
| BAKIM-006 | Usta müdahalesi ACTION olarak etiketlenmemişti. |
| BAKIM-008 | Asıl kök neden (kondenserde kireç) etiketlenmemişti. |
| BAKIM-039 | Olayın gerçekleştiği departman (HK'da) bağlanmamıştı. |
| BAKIM-066 | Zincir eksikti; 'kanallar gelmedi' Ön Büro'da değil odalarda oldu, Ön Büro'daki olay telefon yoğunluğu. |
| DENETIM-008 | 'DÖF açıldı' aksiyonu etiketlenmemişti. |
| DENETIM-027 | Zincirin son halkası (revire götürülme) eksikti. |
| DENETIM-032 | Zincirin sonucu (hijyen puanının düşmesi) EVENT olarak yoktu. |
| DENETIM-040 | Zincirin sonucu (memnuniyet puanının düşmesi) EVENT olarak yoktu. |
| DENETIM-041 | FO (Front Office) kısaltması departman olarak etiketlenmemişti. |
| DENETIM-049 | 'Resepsiyon' departmanı etiketlenmemişti. |
| DENETIM-063 | Asansör ve ara olay eksikti; OCCURS_IN yanlış olaya bağlıydı. |
| DENETIM-068 | 'Spa' departmanı etiketlenmemişti. |
| DOF-015 | İkinci neden (eşzamanlı jeneratör testi) etiketlenmemişti. |
| DOF-045 | F&B'deki olayın departman bağlantısı eksikti. |
| SIKAYET-013 | Zincirin ara halkası (tavanı ıslattı) eksikti. |
| SIKAYET-027 | İkinci sonuç (valizin karışması) etiketlenmemişti. |
| SIKAYET-052 | Olayın gerçekleştiği departman (HK) bağlanmamıştı. |
| SIKAYET-067 | Aradaki gözlem (barmenin yorgunluğu) EVENT olarak yoktu. |

## 3. Modeller ve donanım

| Model (Hugging Face) | Commit | Etiketler | Birleştirme | Bulunan span | Süre (300 metin) |
|---|---|---|---|---|---|
| [`akdeniz27/bert-base-turkish-cased-ner`](https://huggingface.co/akdeniz27/bert-base-turkish-cased-ner) | `99995f7d2be4` | B-LOC, B-ORG, B-PER, I-LOC, I-ORG, I-PER | first | 59 | 15.8 sn (53 ms/metin) |
| [`savasy/bert-base-turkish-ner-cased`](https://huggingface.co/savasy/bert-base-turkish-ner-cased) | `7678083d645a` | B-LOC, B-ORG, B-PER, I-LOC, I-ORG, I-PER | first | 215 | 15.7 sn (52 ms/metin) |

İki model de BERTurk (`dbmdz/bert-base-turkish-cased`) tabanlıdır ve PER/ORG/LOC ile eğitilmiştir. Modeller tam commit hash'iyle sabitlenerek yüklenir (`experiments/ner_baseline.py`).

**Birleştirme stratejisi notu:** İlk denemede `aggregation_strategy="simple"` kullanıldı ve kısaltmalar alt-kelimelerine bölündü (örn. `HK` → `H` + `K`, `DÖF` → `DÖ` + `F`). Modeller kelime düzeyinde eğitildiği için kelimenin etiketini ilk alt-kelimeden alan `first` stratejisine geçildi; raporlanan tüm sonuçlar `first` iledir.

| Donanım / yazılım | Değer |
|---|---|
| CPU | 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz |
| Mantıksal çekirdek / torch thread | 8 / 4 |
| RAM | 39.8 GB |
| Hızlandırıcı | Yok (CPU). CUDA: False |
| İşletim sistemi | Windows-10-10.0.26200-SP0 |
| Python / torch / transformers | 3.11.9 / 2.11.0+cpu / 5.5.4 |

## 4. Değerlendirme yöntemi

1. **`span_only` (etiketten bağımsız örtüşme):** Model hangi etiketi verirse versin, bulduğu span bizim bir varlığımızla karakter düzeyinde örtüşüyor mu? *P* = örtüşen tahmin oranı, *R* (etiket bazında) = o etiketteki gold varlıkların herhangi bir tahminle örtüşme oranı ("kapsama").
2. **`map_ORG=DEPARTMENT` (önceden sabitlenmiş eşleme):** Sonuçlara bakılmadan ORG → DEPARTMENT eşlemesi seçildi; PER ve LOC hiçbir etikete eşlenmez ve her zaman yanlış pozitif sayılır. Ardından 6 etiket üzerinden P/R/F1 iki modda hesaplanır: **exact** (metin + etiket birebir aynı) ve **partial** (span örtüşmesi + aynı etiket). MICRO satırı tüm etiketlerin toplamıdır; DEPARTMENT dışındaki etiketler için model hiç tahmin üretmediğinden P tanımsızdır (—) ve R = 0'dır.

## 5. Sonuçlar

### 5.1 Ana sonuç: gold alt küme (n = 60 metin)

| Model | Ölçüm | P | R | F1 | Doğru tahmin / tahmin | Bulunan gold / gold |
|---|---|---|---|---|---|---|
| akdeniz27 | Etiketten bağımsız örtüşme | 0.938 | 0.053 | 0.100 | 15/16 | 12/228 |
| akdeniz27 | DEPARTMENT, exact | 0.375 | 0.140 | 0.203 | 6/16 | 6/43 |
| akdeniz27 | DEPARTMENT, partial | 0.938 | 0.279 | 0.430 | 15/16 | 12/43 |
| akdeniz27 | 6 etiket MICRO, exact | 0.375 | 0.026 | 0.049 | 6/16 | 6/228 |
| akdeniz27 | 6 etiket MICRO, partial | 0.938 | 0.053 | 0.100 | 15/16 | 12/228 |
| savasy | Etiketten bağımsız örtüşme | 0.942 | 0.202 | 0.332 | 49/52 | 46/228 |
| savasy | DEPARTMENT, exact | 0.372 | 0.442 | 0.404 | 19/51 | 19/43 |
| savasy | DEPARTMENT, partial | 0.549 | 0.628 | 0.586 | 28/51 | 27/43 |
| savasy | 6 etiket MICRO, exact | 0.365 | 0.083 | 0.136 | 19/52 | 19/228 |
| savasy | 6 etiket MICRO, partial | 0.538 | 0.118 | 0.194 | 28/52 | 27/228 |

**Etiket bazında kapsama (span_only R, gold):** model, bizim etiketimizdeki varlıkların ne kadarına herhangi bir span ile dokunabiliyor?

| Etiket | Gold varlık | akdeniz27 | savasy |
|---|---|---|---|
| DEPARTMENT | 43 | 27.9% (12) | 62.8% (27) |
| EQUIPMENT | 29 | 0.0% (0) | 51.7% (15) |
| KPI | 10 | 0.0% (0) | 0.0% (0) |
| EVENT | 85 | 0.0% (0) | 0.0% (0) |
| ROOT_CAUSE | 46 | 0.0% (0) | 4.3% (2) |
| ACTION | 15 | 0.0% (0) | 13.3% (2) |

### 5.2 Tüm set (LLM üretimi etiketler) (n = 300 metin)

> Bu tablo, doğrulanmamış LLM üretimi etiketlere dayanır; ana sonuç olarak gold tablosu kullanılmalıdır.

| Model | Ölçüm | P | R | F1 | Doğru tahmin / tahmin | Bulunan gold / gold |
|---|---|---|---|---|---|---|
| akdeniz27 | Etiketten bağımsız örtüşme | 0.932 | 0.043 | 0.083 | 55/59 | 48/1108 |
| akdeniz27 | DEPARTMENT, exact | 0.436 | 0.106 | 0.171 | 24/55 | 22/207 |
| akdeniz27 | DEPARTMENT, partial | 0.818 | 0.193 | 0.313 | 45/55 | 40/207 |
| akdeniz27 | 6 etiket MICRO, exact | 0.407 | 0.020 | 0.038 | 24/59 | 22/1108 |
| akdeniz27 | 6 etiket MICRO, partial | 0.763 | 0.036 | 0.069 | 45/59 | 40/1108 |
| savasy | Etiketten bağımsız örtüşme | 0.898 | 0.173 | 0.290 | 193/215 | 192/1108 |
| savasy | DEPARTMENT, exact | 0.335 | 0.338 | 0.337 | 70/209 | 70/207 |
| savasy | DEPARTMENT, partial | 0.493 | 0.493 | 0.493 | 103/209 | 102/207 |
| savasy | 6 etiket MICRO, exact | 0.326 | 0.063 | 0.106 | 70/215 | 70/1108 |
| savasy | 6 etiket MICRO, partial | 0.479 | 0.092 | 0.154 | 103/215 | 102/1108 |

**Etiket bazında kapsama (span_only R, all):** model, bizim etiketimizdeki varlıkların ne kadarına herhangi bir span ile dokunabiliyor?

| Etiket | Gold varlık | akdeniz27 | savasy |
|---|---|---|---|
| DEPARTMENT | 207 | 19.3% (40) | 49.3% (102) |
| EQUIPMENT | 145 | 2.1% (3) | 38.6% (56) |
| KPI | 29 | 0.0% (0) | 10.3% (3) |
| EVENT | 410 | 0.2% (1) | 2.9% (12) |
| ROOT_CAUSE | 249 | 0.8% (2) | 4.8% (12) |
| ACTION | 68 | 2.9% (2) | 10.3% (7) |

### 5.3 Difficulty türüne göre

**Tüm set:** span_only R (tüm etiketler) ve DEPARTMENT partial F1.

| difficulty | Metin | Gold varlık | akdeniz27 kapsama | akdeniz27 DEPT F1 | savasy kapsama | savasy DEPT F1 |
|---|---|---|---|---|---|---|
| explicit (açık) | 104 | 389 | 4.1% | 0.293 | 19.5% | 0.535 |
| implicit (örtük) | 95 | 332 | 3.9% | 0.289 | 13.6% | 0.452 |
| multi_cause (çoklu neden) | 33 | 139 | 4.3% | 0.500 | 13.0% | 0.373 |
| chain (zincir) | 37 | 163 | 3.1% | 0.588 | 8.6% | 0.400 |
| abbreviation (kısaltma) | 23 | 122 | 17.2% | 0.526 | 36.1% | 0.519 |
| informal (günlük dil) | 14 | 50 | 0.0% | — | 4.0% | 0.182 |
| negative (negatif) | 24 | 40 | 2.5% | 0.105 | 45.0% | 0.611 |

**Gold alt küme — hücreler küçük, yorumlarken dikkat:** span_only R (tüm etiketler) ve DEPARTMENT partial F1.

| difficulty | Metin | Gold varlık | akdeniz27 kapsama | akdeniz27 DEPT F1 | savasy kapsama | savasy DEPT F1 |
|---|---|---|---|---|---|---|
| explicit (açık) | 15 | 58 | 6.9% | 0.571 | 22.4% | 0.696 |
| implicit (örtük) | 15 | 59 | 5.1% | 0.400 | 20.3% | 0.560 |
| multi_cause (çoklu neden) | 5 | 24 | 4.2% | 0.667 | 16.7% | 0.750 |
| chain (zincir) | 10 | 47 | 4.3% | 0.800 | 6.4% | 0.286 |
| abbreviation (kısaltma) | 9 | 48 | 16.7% | 0.647 | 33.3% | 0.585 |
| informal (günlük dil) | 3 | 11 | 0.0% | — | 0.0% | — |
| negative (negatif) | 12 | 21 | 0.0% | — | 42.9% | 0.632 |

### 5.4 Doküman türüne göre (tüm set)

| doc_type | akdeniz27 kapsama | akdeniz27 DEPT R | akdeniz27 DEPT P | savasy kapsama | savasy DEPT R | savasy DEPT P |
|---|---|---|---|---|---|---|
| BAKIM | 3.6% | 14.9% | 58.3% | 24.5% | 61.7% | 35.8% |
| DENETIM | 7.2% | 27.3% | 89.5% | 19.8% | 60.0% | 61.8% |
| DOF | 4.5% | 25.0% | 88.2% | 12.8% | 44.2% | 54.8% |
| SIKAYET | 2.4% | 9.4% | 85.7% | 10.8% | 32.1% | 54.8% |

## 6. Hata analizi

Örnekler mümkün olduğunca gold alt kümeden, yoksa tüm setten seçilmiştir (id sırasıyla ilk örnekler).

### 6.1 `akdeniz27/bert-base-turkish-cased-ner`

**En çok kaçırılan 3 etiket** (gold, hiçbir tahminle örtüşmeyen gold varlık oranı): EVENT %100 (85/85), ROOT_CAUSE %100 (46/46), EQUIPMENT %100 (29/29).

**En düşük kapsamalı 3 difficulty türü** (tüm set, span_only R): informal (günlük dil) %0.0, negative (negatif) %2.5, chain (zincir) %3.1.

**Karışıklık matrisi** (tüm set; satır = model etiketi, sütun = örtüştüğü gold etiketi, NONE = hiçbir gold varlıkla örtüşmüyor). Bir tahmin birden çok gold varlıkla örtüşebilir.

| Model ↓ / Gold → | DEPARTMENT | EQUIPMENT | KPI | EVENT | ROOT_CAUSE | ACTION | NONE |
|---|---|---|---|---|---|---|---|
| LOC | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| ORG | 45 | 3 | 0 | 1 | 3 | 2 | 3 |
| PER | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

**Örnek — kaçırılan varlıklar:**

- **BAKIM-002**: "AHU-3 fan motoru yandı, HK çamaşır odası havalandırması durdu. TS motoru değiştirdi, DÖF açıldı."  
  Beklenen: `TS` / DEPARTMENT — Modelin çıktısı: `HK`/ORG
- **BAKIM-004**: "Yağmur olukları tıkalı olduğundan teras suyu taştı, su aşağıdaki koridora sızdı, elektrik panosu atınca masaj odaları karardı."  
  Beklenen: `elektrik panosu` / EQUIPMENT — Modelin çıktısı: *(hiç span yok)*
- **BAKIM-006**: "klima yine bozuldu valla, 507 de misafir bağırdı. filtre hiç temizlenmemiş zaten, usta geldi baktı bi kaç saatte düzeldi"  
  Beklenen: `filtre hiç temizlenmemiş` / ROOT_CAUSE — Modelin çıktısı: *(hiç span yok)*

**Örnek — etiket uyuşmazlığı** (span bizim bir varlığımızla örtüşüyor ama eşlenen etiket farklı):

- **BAKIM-009**: "FCU su kaçağı nedeniyle 118 OOO yapıldı, PMS güncellendi. TS tamir etti."  
  Beklenen: `FCU` / EQUIPMENT — Modelin çıktısı: `FCU` / ORG
- **BAKIM-010**: "Yedek conta stokta yoktu ve bakım planında kontrol atlandı. Sonuç olarak 220'deki FCU üç gün çalışmadı."  
  Beklenen: `FCU` / EQUIPMENT — Modelin çıktısı: `FCU` / ORG
- **BAKIM-069**: "KPI: ort. arıza giderme süresi 3,5 saat. TS'de AHU-2 ve FCU arızaları ard arda geldi, vardiya sayısı yetersiz kaldı. DÖF için HK raporu bekleniyor."  
  Beklenen: `DÖF` / ACTION — Modelin çıktısı: `DÖF` / ORG

**Örnek — yanlış pozitif** (hiçbir gold varlıkla örtüşmeyen span):

- **BAKIM-074**: "PMS interface kopması nedeniyle F&B adisyonları odaya yansımadı; ön büro mutabakatta zorlandı. IT patch yükledi."  
  Modelin çıktısı: `IT` / ORG
- **DOF-022**: "DÖF: HK'da PMS oda statüsü geç girildiği için KPI hedefi tutmadı. Anlık giriş zorunlu kılındı."  
  Modelin çıktısı: `DÖF` / PER
- **DOF-026**: "Rezervasyon sistemindeki yazılım hatası yüzünden aynı odaya iki misafir yerleştirildi. Ön Büro misafirleri üst kategoriye aldı ve hata IT'ye iletildi."  
  Modelin çıktısı: `IT` / ORG

### 6.2 `savasy/bert-base-turkish-ner-cased`

**En çok kaçırılan 3 etiket** (gold, hiçbir tahminle örtüşmeyen gold varlık oranı): EVENT %100 (85/85), KPI %100 (10/10), ROOT_CAUSE %96 (44/46).

**En düşük kapsamalı 3 difficulty türü** (tüm set, span_only R): informal (günlük dil) %4.0, chain (zincir) %8.6, multi_cause (çoklu neden) %13.0.

**Karışıklık matrisi** (tüm set; satır = model etiketi, sütun = örtüştüğü gold etiketi, NONE = hiçbir gold varlıkla örtüşmüyor). Bir tahmin birden çok gold varlıkla örtüşebilir.

| Model ↓ / Gold → | DEPARTMENT | EQUIPMENT | KPI | EVENT | ROOT_CAUSE | ACTION | NONE |
|---|---|---|---|---|---|---|---|
| LOC | 0 | 2 | 0 | 2 | 0 | 0 | 0 |
| ORG | 103 | 56 | 3 | 11 | 14 | 8 | 22 |
| PER | 1 | 1 | 0 | 0 | 0 | 0 | 0 |

**Örnek — kaçırılan varlıklar:**

- **BAKIM-039**: "KPI: AHU filtre değişimi gecikti (TS), buna bağlı HK'da oda havası hijyen puanı 82'ye geriledi. DÖF açıldı."  
  Beklenen: `TS` / DEPARTMENT — Modelin çıktısı: *(hiç span yok)*
- **BAKIM-004**: "Yağmur olukları tıkalı olduğundan teras suyu taştı, su aşağıdaki koridora sızdı, elektrik panosu atınca masaj odaları karardı."  
  Beklenen: `elektrik panosu` / EQUIPMENT — Modelin çıktısı: *(hiç span yok)*
- **BAKIM-006**: "klima yine bozuldu valla, 507 de misafir bağırdı. filtre hiç temizlenmemiş zaten, usta geldi baktı bi kaç saatte düzeldi"  
  Beklenen: `filtre hiç temizlenmemiş` / ROOT_CAUSE — Modelin çıktısı: *(hiç span yok)*

**Örnek — etiket uyuşmazlığı** (span bizim bir varlığımızla örtüşüyor ama eşlenen etiket farklı):

- **BAKIM-002**: "AHU-3 fan motoru yandı, HK çamaşır odası havalandırması durdu. TS motoru değiştirdi, DÖF açıldı."  
  Beklenen: `AHU-3` / EQUIPMENT — Modelin çıktısı: `AHU` / ORG
- **BAKIM-008**: "Chiller kondenser borularında kireç var, son temizlik 14 ay önce yapılmış. Öğleden sonra soğutma kapasitesi düştü, lobide sıcaklık 27'yi gördü."  
  Beklenen: `Chiller` / EQUIPMENT — Modelin çıktısı: `Chiller` / ORG
- **BAKIM-012**: "Havuz pompa dairesi haftalık kontrol listesi dolduruldu. Basınç değerleri normal, kaçak yok, kimyasal stok yeterli."  
  Beklenen: `pompa` / EQUIPMENT — Modelin çıktısı: `Havuz pompa dairesi` / ORG

**Örnek — yanlış pozitif** (hiçbir gold varlıkla örtüşmeyen span):

- **BAKIM-002**: "AHU-3 fan motoru yandı, HK çamaşır odası havalandırması durdu. TS motoru değiştirdi, DÖF açıldı."  
  Modelin çıktısı: `odası` / ORG
- **BAKIM-020**: "Spa buhar odası jeneratöründe kireç birikmiş, periyodik detartraj yapılmamıştı. Buhar odası iki gün kapalı kaldı."  
  Modelin çıktısı: `Buhar` / ORG
- **BAKIM-026**: "Bakım personeli izinde, ayrıca yedek sensör gelmedi. 3. kat yangın dedektörü arızası 4 gün açık kaldı."  
  Modelin çıktısı: `3` / ORG

### 6.3 Kısaltmalar

Metinlerde kelime olarak geçen her kısaltma için: model bir span ile dokundu mu, span tam olarak kısaltmanın kendisi mi, hangi etiketi verdi; gold'da bu kısaltma hangi etiketle (bir varlığın parçası olarak) işaretlenmiş? (tüm set)

| Kısaltma | Geçiş | Gold etiketi | akdeniz27: dokundu (tam) etiket | savasy: dokundu (tam) etiket |
|---|---|---|---|---|
| `PMS` | 18 | EQUIPMENT 9, ROOT_CAUSE 5, etiketsiz 3, EVENT 1 | 3/18 (tam: 3) ORG:3 | 13/18 (tam: 9) ORG:13 |
| `HK` | 21 | DEPARTMENT 20, ROOT_CAUSE 2 | 13/21 (tam: 13) ORG:13 | 8/21 (tam: 7) ORG:8 |
| `F&B` | 12 | DEPARTMENT 11, ROOT_CAUSE 1, EVENT 1 | 5/12 (tam: 2) ORG:8 | 12/12 (tam: 8) ORG:12 |
| `DÖF` | 15 | ACTION 8, etiketsiz 7 | 4/15 (tam: 4) ORG:3 PER:1 | 9/15 (tam: 7) ORG:9 |
| `KPI` | 12 | etiketsiz 8, KPI 4, EVENT 1, ACTION 1 | 0/12 (tam: 0)  | 6/12 (tam: 4) ORG:6 |
| `IT` | 2 | etiketsiz 2 | 2/2 (tam: 2) ORG:2 | 1/2 (tam: 0) ORG:1 |
| `FO` | 2 | DEPARTMENT 1, etiketsiz 1 | 0/2 (tam: 0)  | 1/2 (tam: 1) ORG:1 |
| `TS` | 5 | DEPARTMENT 5 | 0/5 (tam: 0)  | 4/5 (tam: 4) ORG:4 |
| `AHU` | 3 | EQUIPMENT 3 | 0/3 (tam: 0)  | 1/3 (tam: 1) ORG:1 |
| `FCU` | 6 | EQUIPMENT 6, EVENT 1 | 2/6 (tam: 2) ORG:2 | 5/6 (tam: 4) ORG:5 |

Gözlemler: ORG etiketi, bu modellerde departman kısaltmaları (HK, F&B, TS) ile sistem/ekipman kısaltmalarını (PMS, FCU, AHU) ve süreç kısaltmalarını (DÖF, KPI) **ayırt etmeden** kullanılan tek "büyük harfli kısaltma" sınıfı gibi davranıyor; bu yüzden ORG → DEPARTMENT eşlemesi kısaltmalarda EQUIPMENT/ACTION'a ait span'ları da DEPARTMENT'a çekiyor. `F&B` WordPiece ön-tokenizasyonunda `&` işaretinden bölündüğü için kelime düzeyinde birleştirmede bile `F` ve `B` ayrı span olarak çıkabiliyor.

### 6.4 Büyük/küçük harf etkisi

Gold DEPARTMENT varlıklarının 17/207'i küçük harfle başlıyor; bunlar çoğunlukla misafir şikâyetlerindeki günlük ifadeler ("resepsiyona", "kat görevlisi", "ön büro"). Kaçırılan DEPARTMENT varlıklarının yazım biçimine göre dağılımı (tüm set):

| Model | Küçük harfli DEPARTMENT kaçırılan | Büyük harfli DEPARTMENT kaçırılan | Büyük harfle başlayan, DEPARTMENT olmayan ORG span |
|---|---|---|---|
| akdeniz27 | 17/17 (100%) | 150/190 (79%) | 0 |
| savasy | 16/17 (94%) | 89/190 (47%) | 60 |

Son sütun, cümle başında ya da özel ad gibi yazılmış sıradan isimlerin (örn. "Bulaşık makinesi", "Kombi", "Sauna") ORG olarak etiketlenip departman olmayan bir varlığa ya da hiçbir varlığa denk gelmesini sayar (tamamı büyük harf olan kısaltmalar hariç).

### 6.5 Örtük nedensellik ve negatif örnekler

- **Örtük nedensellik:** NER modelleri ilişki üretmediğinden örtük CAUSES ilişkilerinin yakalanıp yakalanmadığı bu deneyle **ölçülemez**. Ölçülebilen tek şey, nedenselliğin uçlarını oluşturan ROOT_CAUSE ve EVENT varlıklarına dokunma oranıdır:
  - `akdeniz27`: explicit ROOT_CAUSE R=0.0%, EVENT R=0.0%; implicit ROOT_CAUSE R=1.3%, EVENT R=0.0%; multi_cause ROOT_CAUSE R=0.0%, EVENT R=2.1%; chain ROOT_CAUSE R=0.0%, EVENT R=0.0%
  - `savasy`: explicit ROOT_CAUSE R=2.4%, EVENT R=2.4%; implicit ROOT_CAUSE R=3.9%, EVENT R=0.8%; multi_cause ROOT_CAUSE R=8.1%, EVENT R=8.3%; chain ROOT_CAUSE R=6.7%, EVENT R=2.1%
  Yani hazır NER, nedensellik zincirinin uç varlıklarını neredeyse hiç görmüyor; bu, ilişki çıkarımına geçmeden önce bile alan-özel varlık tanımanın gerektiğini gösteriyor.
- **Negatif örnekler (ilişkisiz metinler):** İlişki üretilmediği için "uydurma ilişki" sorusu bu deney için geçerli değildir. Varlık düzeyinde:
  - `akdeniz27`: 24 negatif metinde 1 span; bunlardan 0 tanesi hiçbir gold varlıkla örtüşmüyor (örnek: yok).
  - `savasy`: 24 negatif metinde 18 span; bunlardan 1 tanesi hiçbir gold varlıkla örtüşmüyor (örnek: SIKAYET-060: `hayvan`/ORG).
  Negatif metinlerdeki gold varlıkların çoğu departman adıdır; §5.3'teki negatif satırında kapsamanın görece yüksek çıkması bundan kaynaklanır, modelin negatifleri "anladığı" anlamına gelmez.

## 7. Yorum ve iyileştirme önerileri

Bulgulardan çıkan sonuçlar ve öneriler (sayılar §5–6'daki tablolardan):

1. **Genel amaçlı NER bu görev için yetersiz.** Modellerin etiket uzayı (PER/ORG/LOC) bizim olay/kök neden/aksiyon gibi *yüklem içeren, çok kelimeli* varlıklarımızla örtüşmüyor; EVENT, ROOT_CAUSE, ACTION ve KPI kapsaması sıfıra yakın. Yakalanan şey neredeyse yalnızca büyük harfle başlayan departman/sistem adları.
2. **Alan-özel ince ayar (fine-tuning):** BERTurk tabanı korunup 6 etiketlik BIO şemasıyla token sınıflandırma eğitimi yapılması en doğrudan iyileştirme. Ancak eğitim verisi olarak bu sentetik seti kullanmadan önce etiket kalitesi artırılmalı (gold incelemesinde satırların yaklaşık üçte birinde eksik etiket bulundu). İlişkiler için varlık çiftleri üzerinde ayrı bir ilişki sınıflandırıcı eklenebilir.
3. **Kural tabanlı kısaltma sözlüğü:** HK, F&B, TS, FO → DEPARTMENT; PMS, AHU, FCU → EQUIPMENT; DÖF → süreç/aksiyon bağlamı gibi sabit bir sözlük, hem bir ön işleme adımı (kısaltma açma) hem de bir post-processing katmanı olarak ORG etiketinin belirsizliğini doğrudan giderir. `F&B` gibi işaret içeren kısaltmalar tokenizasyondan önce korunmalı.
4. **Büyük harf yanlılığı (§6.4):** Cased modeller küçük harfle yazılmış departman adlarını neredeyse tamamen kaçırıyor; savasy ayrıca büyük harfle başlayan sıradan isimleri ORG sanıyor. SIKAYET metinlerinde DEPARTMENT recall'unun en düşük olması (§5.4) bununla tutarlı. Departman sözlüğüyle normalizasyon veya günlük dil örnekleriyle eğitim gerekli.
5. **LLM tabanlı çıkarım (Deney B) ileride:** Bu çalışmada kapsam dışı bırakılan zero-/few-shot LLM deneyi, etiket uzayı uyuşmazlığını prompt ile çözebileceği ve ilişkileri de üretebileceği için bir sonraki adım olarak önerilir; few-shot örnek sayısını artırmak ve kısaltma sözlüğünü prompt'a eklemek denenebilir.
6. **Değerlendirme verisi:** Gold alt kümenin insan tarafından doğrulanması ve tercihen iki anotatörle uyum (Cohen's κ) ölçülmesi, sonuçların rapor için güvenilirliğini artırır.

## 8. Tekrarlanabilirlik

Tüm adımlar `python experiments/run_all.py` ile baştan çalışır (bkz. `README.md`). Modeller commit hash'iyle sabitlenmiştir; NER çıkarımı deterministiktir (örnekleme yok). Gold seçimi sabit tohumla (seed=42) yapılır, gold düzeltmeleri `experiments/gold_review_edits.py` içinde kayıtlıdır. Ham tahminler: `results/predictions/*.jsonl`; tüm metrikler: `results/metrics.csv`.
