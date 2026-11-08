# Gold aday alt kümesi — inceleme tablosu

60 satır, her doc_type × zorluk grubu hücresinden 3 adet (seed=42).

## BAKIM-002  ·  abbreviation

> AHU-3 fan motoru yandı, HK çamaşır odası havalandırması durdu. TS motoru değiştirdi, DÖF açıldı.

| Varlık | Etiket |
|---|---|
| AHU-3 | EQUIPMENT |
| fan motoru yandı | EVENT |
| havalandırması durdu | EVENT |
| HK | DEPARTMENT |
| TS | DEPARTMENT |
| motoru değiştirdi | ACTION |
| DÖF açıldı | ACTION |

İlişkiler:
- fan motoru yandı —CAUSES→ havalandırması durdu
- havalandırması durdu —ADDRESSED_BY→ motoru değiştirdi
- havalandırması durdu —OCCURS_IN→ HK

## BAKIM-004  ·  chain

> Yağmur olukları tıkalı olduğundan teras suyu taştı, su aşağıdaki koridora sızdı, elektrik panosu atınca masaj odaları karardı.

| Varlık | Etiket |
|---|---|
| Yağmur olukları tıkalı | ROOT_CAUSE |
| teras suyu taştı | EVENT |
| su aşağıdaki koridora sızdı | EVENT |
| elektrik panosu | EQUIPMENT |
| masaj odaları karardı | EVENT |

İlişkiler:
- Yağmur olukları tıkalı —CAUSES→ teras suyu taştı
- teras suyu taştı —CAUSES→ su aşağıdaki koridora sızdı
- elektrik panosu —CAUSES→ masaj odaları karardı
- su aşağıdaki koridora sızdı —CAUSES→ masaj odaları karardı

## BAKIM-006  ·  informal

> klima yine bozuldu valla, 507 de misafir bağırdı. filtre hiç temizlenmemiş zaten, usta geldi baktı bi kaç saatte düzeldi

| Varlık | Etiket |
|---|---|
| klima | EQUIPMENT |
| klima yine bozuldu | EVENT |
| misafir bağırdı | EVENT |
| filtre hiç temizlenmemiş | ROOT_CAUSE |
| usta geldi baktı | ACTION |

İlişkiler:
- filtre hiç temizlenmemiş —CAUSES→ klima yine bozuldu
- klima yine bozuldu —CAUSES→ misafir bağırdı
- klima yine bozuldu —ADDRESSED_BY→ usta geldi baktı

## BAKIM-008  ·  implicit

> Chiller kondenser borularında kireç var, son temizlik 14 ay önce yapılmış. Öğleden sonra soğutma kapasitesi düştü, lobide sıcaklık 27'yi gördü.

| Varlık | Etiket |
|---|---|
| Chiller | EQUIPMENT |
| son temizlik 14 ay önce yapılmış | ROOT_CAUSE |
| soğutma kapasitesi düştü | EVENT |
| lobide sıcaklık 27'yi gördü | EVENT |
| kondenser borularında kireç var | ROOT_CAUSE |

İlişkiler:
- son temizlik 14 ay önce yapılmış —CAUSES→ soğutma kapasitesi düştü
- soğutma kapasitesi düştü —CAUSES→ lobide sıcaklık 27'yi gördü
- kondenser borularında kireç var —CAUSES→ soğutma kapasitesi düştü

## BAKIM-012  ·  negative

> Havuz pompa dairesi haftalık kontrol listesi dolduruldu. Basınç değerleri normal, kaçak yok, kimyasal stok yeterli.

| Varlık | Etiket |
|---|---|
| Havuz | DEPARTMENT |
| pompa | EQUIPMENT |

İlişkiler: *(yok)*

## BAKIM-015  ·  explicit

> Havuz sirkülasyon pompasının rulman aşınması yüzünden pompa devre dışı kaldı, havuz suyu bir gün boyunca filtrelenemedi.

| Varlık | Etiket |
|---|---|
| Havuz sirkülasyon pompası | EQUIPMENT |
| rulman aşınması | ROOT_CAUSE |
| pompa devre dışı kaldı | EVENT |
| havuz suyu bir gün boyunca filtrelenemedi | EVENT |

İlişkiler:
- rulman aşınması —CAUSES→ pompa devre dışı kaldı
- pompa devre dışı kaldı —CAUSES→ havuz suyu bir gün boyunca filtrelenemedi

## BAKIM-019  ·  implicit

> Havuz otomatik klor dozaj pompasının hortumu çatlak bulundu. Serbest klor 0,3 ppm'e düştü, havuz bir saat kapatıldı.

| Varlık | Etiket |
|---|---|
| klor dozaj pompası | EQUIPMENT |
| hortumu çatlak | ROOT_CAUSE |
| Serbest klor 0,3 ppm'e düştü | EVENT |
| havuz bir saat kapatıldı | EVENT |

İlişkiler:
- hortumu çatlak —CAUSES→ Serbest klor 0,3 ppm'e düştü
- Serbest klor 0,3 ppm'e düştü —CAUSES→ havuz bir saat kapatıldı

## BAKIM-023  ·  negative

> Aylık periyodik bakım: 6 adet FCU filtresi temizlendi, chiller yağ seviyesi normal, jeneratör 15 dk yüksüz çalıştırıldı. Bulgu yok.

| Varlık | Etiket |
|---|---|
| FCU | EQUIPMENT |
| chiller | EQUIPMENT |
| jeneratör | EQUIPMENT |

İlişkiler: *(yok)*

## BAKIM-025  ·  explicit

> Asansör kabin kapı sensörü kirlendiği için B Blok asansörü gün içinde 3 kez kapıda takıldı.

| Varlık | Etiket |
|---|---|
| B Blok asansörü | EQUIPMENT |
| kapı sensörü kirlendiği | ROOT_CAUSE |
| kapıda takıldı | EVENT |

İlişkiler:
- kapı sensörü kirlendiği —CAUSES→ kapıda takıldı
- B Blok asansörü —CAUSES→ kapıda takıldı

## BAKIM-028  ·  explicit

> Buz makinesi su giriş filtresi tıkandığı için bar buz stoğu bitti; F&B ekibi paketli buz satın aldı.

| Varlık | Etiket |
|---|---|
| Buz makinesi | EQUIPMENT |
| su giriş filtresi tıkandığı | ROOT_CAUSE |
| bar buz stoğu bitti | EVENT |
| F&B | DEPARTMENT |
| paketli buz satın aldı | ACTION |

İlişkiler:
- su giriş filtresi tıkandığı —CAUSES→ bar buz stoğu bitti
- bar buz stoğu bitti —ADDRESSED_BY→ paketli buz satın aldı
- bar buz stoğu bitti —OCCURS_IN→ F&B

## BAKIM-034  ·  multi_cause

> Aşırı yağış ve eski drenaj pompasının kapasite yetersizliği birlikte bodrum katının su basmasına yol açtı, depo stoklarının bir kısmı ıslandı.

| Varlık | Etiket |
|---|---|
| Aşırı yağış | ROOT_CAUSE |
| drenaj pompası | EQUIPMENT |
| kapasite yetersizliği | ROOT_CAUSE |
| bodrum katının su basması | EVENT |
| depo stoklarının bir kısmı ıslandı | EVENT |

İlişkiler:
- Aşırı yağış —CAUSES→ bodrum katının su basması
- kapasite yetersizliği —CAUSES→ bodrum katının su basması
- bodrum katının su basması —CAUSES→ depo stoklarının bir kısmı ıslandı

## BAKIM-039  ·  abbreviation

> KPI: AHU filtre değişimi gecikti (TS), buna bağlı HK'da oda havası hijyen puanı 82'ye geriledi. DÖF açıldı.

| Varlık | Etiket |
|---|---|
| AHU | EQUIPMENT |
| filtre değişimi gecikti | ROOT_CAUSE |
| hijyen puanı | KPI |
| 82'ye geriledi | EVENT |
| TS | DEPARTMENT |
| HK | DEPARTMENT |
| DÖF açıldı | ACTION |

İlişkiler:
- filtre değişimi gecikti —CAUSES→ 82'ye geriledi
- 82'ye geriledi —ADDRESSED_BY→ DÖF açıldı
- 82'ye geriledi —OCCURS_IN→ HK

## BAKIM-050  ·  chain

> Yağ tutucu temizliği geciktiği için mutfak gider hattı tıkandı, zemin taştı; kayma riski nedeniyle Güvenlik bölgeyi kordona aldı.

| Varlık | Etiket |
|---|---|
| Yağ tutucu temizliği geciktiği | ROOT_CAUSE |
| mutfak gider hattı tıkandı | EVENT |
| zemin taştı | EVENT |
| Güvenlik | DEPARTMENT |
| bölgeyi kordona aldı | ACTION |

İlişkiler:
- Yağ tutucu temizliği geciktiği —CAUSES→ mutfak gider hattı tıkandı
- mutfak gider hattı tıkandı —CAUSES→ zemin taştı
- zemin taştı —ADDRESSED_BY→ bölgeyi kordona aldı

## BAKIM-062  ·  negative

> Soğuk oda ve dondurucu günlük sıcaklık kayıtları alındı: +3 / -19. Mutfak şefi imzaladı, sapma yok.

| Varlık | Etiket |
|---|---|
| Soğuk oda | EQUIPMENT |
| dondurucu | EQUIPMENT |
| Mutfak | DEPARTMENT |

İlişkiler: *(yok)*

## BAKIM-066  ·  implicit

> TV başlık yayın sistemi güncelleme sonrası kanal listesini kaybetti. Odalarda kanallar gelmedi, Ön Büro telefonlarla boğuştu.

| Varlık | Etiket |
|---|---|
| TV başlık yayın sistemi | EQUIPMENT |
| güncelleme | ROOT_CAUSE |
| kanallar gelmedi | EVENT |
| Ön Büro | DEPARTMENT |
| kanal listesini kaybetti | EVENT |
| telefonlarla boğuştu | EVENT |

İlişkiler:
- güncelleme —CAUSES→ kanal listesini kaybetti
- kanal listesini kaybetti —CAUSES→ kanallar gelmedi
- kanallar gelmedi —CAUSES→ telefonlarla boğuştu
- telefonlarla boğuştu —OCCURS_IN→ Ön Büro

## DENETIM-004  ·  negative

> Spa resepsiyonunda kayıt defteri güncel tutulmuş, tüm randevular PMS ile uyumlu bulunmuştur. Uygunsuzluk tespit edilmemiştir.

| Varlık | Etiket |
|---|---|
| Spa | DEPARTMENT |
| PMS | EQUIPMENT |

İlişkiler: *(yok)*

## DENETIM-005  ·  negative

> Misafir İlişkileri biriminde şikayet kayıtlarının tamamı 24 saat içinde yanıtlanmış; misafir memnuniyet puanı 9,1 olarak ölçülmüştür.

| Varlık | Etiket |
|---|---|
| Misafir İlişkileri | DEPARTMENT |
| misafir memnuniyet puanı | KPI |

İlişkiler: *(yok)*

## DENETIM-008  ·  abbreviation|explicit

> F&B KPI raporunda kahvaltı bufesinde fire artışı görüldü; porsiyon standardı eğitimi eksikliği nedeniyle DÖF açıldı, eğitim verildi.

| Varlık | Etiket |
|---|---|
| F&B | DEPARTMENT |
| fire artışı | EVENT |
| porsiyon standardı eğitimi eksikliği | ROOT_CAUSE |
| eğitim verildi | ACTION |
| DÖF açıldı | ACTION |

İlişkiler:
- porsiyon standardı eğitimi eksikliği —CAUSES→ fire artışı
- porsiyon standardı eğitimi eksikliği —ADDRESSED_BY→ eğitim verildi
- fire artışı —OCCURS_IN→ F&B
- porsiyon standardı eğitimi eksikliği —ADDRESSED_BY→ DÖF açıldı

## DENETIM-019  ·  multi_cause

> Bakım planı güncellenmediği ve yedek filtre stoğu tutulmadığı için klima performansı düştü; bu da oda sıcaklığı şikayetlerine neden oldu. Teknik Servis bakım planını güncelledi.

| Varlık | Etiket |
|---|---|
| Bakım planı güncellenmediği | ROOT_CAUSE |
| yedek filtre stoğu tutulmadığı | ROOT_CAUSE |
| klima performansı düştü | EVENT |
| oda sıcaklığı şikayetlerine | EVENT |
| Teknik Servis | DEPARTMENT |
| bakım planını güncelledi | ACTION |

İlişkiler:
- Bakım planı güncellenmediği —CAUSES→ klima performansı düştü
- yedek filtre stoğu tutulmadığı —CAUSES→ klima performansı düştü
- klima performansı düştü —CAUSES→ oda sıcaklığı şikayetlerine
- Bakım planı güncellenmediği —ADDRESSED_BY→ bakım planını güncelledi
- klima performansı düştü —OCCURS_IN→ Teknik Servis

## DENETIM-021  ·  explicit

> Kat Hizmetleri'nde oda hazırlama gecikmeleri yaşandı; oda hazır olma süresi personel eksikliği yüzünden 45 dakikaya çıktı.

| Varlık | Etiket |
|---|---|
| Kat Hizmetleri | DEPARTMENT |
| oda hazırlama gecikmeleri | EVENT |
| oda hazır olma süresi | KPI |
| personel eksikliği | ROOT_CAUSE |

İlişkiler:
- personel eksikliği —CAUSES→ oda hazırlama gecikmeleri
- oda hazırlama gecikmeleri —OCCURS_IN→ Kat Hizmetleri

## DENETIM-027  ·  implicit

> Mini Club kayıt formlarında alerji bilgisi alanı boş bırakılmış. Bir çocuk fıstıklı ikram yedi ve revire götürüldü.

| Varlık | Etiket |
|---|---|
| Mini Club | DEPARTMENT |
| alerji bilgisi alanı boş bırakılmış | ROOT_CAUSE |
| fıstıklı ikram yedi | EVENT |
| revire götürüldü | EVENT |

İlişkiler:
- alerji bilgisi alanı boş bırakılmış —CAUSES→ fıstıklı ikram yedi
- fıstıklı ikram yedi —OCCURS_IN→ Mini Club
- fıstıklı ikram yedi —CAUSES→ revire götürüldü

## DENETIM-032  ·  chain

> Çocuk havuzu filtresi tıkandı, su akışı düştü, klor dağılımı bozuldu ve hijyen puanı sınırın altına indi.

| Varlık | Etiket |
|---|---|
| Çocuk havuzu filtresi | EQUIPMENT |
| su akışı düştü | EVENT |
| klor dağılımı bozuldu | EVENT |
| hijyen puanı | KPI |
| hijyen puanı sınırın altına indi | EVENT |

İlişkiler:
- Çocuk havuzu filtresi —CAUSES→ su akışı düştü
- su akışı düştü —CAUSES→ klor dağılımı bozuldu
- klor dağılımı bozuldu —CAUSES→ hijyen puanı sınırın altına indi

## DENETIM-036  ·  negative

> İç denetimde Mutfak depolarında FIFO uygulaması, etiketleme ve sıcaklık kayıtları incelenmiş olup herhangi bir bulguya rastlanmamıştır.

| Varlık | Etiket |
|---|---|
| Mutfak | DEPARTMENT |

İlişkiler: *(yok)*

## DENETIM-040  ·  chain

> Rezervasyon sistemindeki overbooking uyarısı kapalıydı; bu yüzden 6 oda fazla satıldı, sonuçta misafirler başka otele yönlendirildi ve memnuniyet puanı düştü.

| Varlık | Etiket |
|---|---|
| overbooking uyarısı kapalıydı | ROOT_CAUSE |
| 6 oda fazla satıldı | EVENT |
| misafirler başka otele yönlendirildi | EVENT |
| memnuniyet puanı | KPI |
| memnuniyet puanı düştü | EVENT |

İlişkiler:
- overbooking uyarısı kapalıydı —CAUSES→ 6 oda fazla satıldı
- 6 oda fazla satıldı —CAUSES→ misafirler başka otele yönlendirildi
- misafirler başka otele yönlendirildi —CAUSES→ memnuniyet puanı düştü

## DENETIM-041  ·  abbreviation|implicit

> HK DÖF'ünde kök neden: PMS'te oda durumu güncellenmiyor; FO ile HK arasında senkron eksik.

| Varlık | Etiket |
|---|---|
| HK | DEPARTMENT |
| PMS'te | EQUIPMENT |
| oda durumu güncellenmiyor | EVENT |
| senkron eksik | ROOT_CAUSE |
| FO | DEPARTMENT |

İlişkiler:
- PMS'te —CAUSES→ oda durumu güncellenmiyor
- senkron eksik —CAUSES→ oda durumu güncellenmiyor
- oda durumu güncellenmiyor —OCCURS_IN→ HK

## DENETIM-042  ·  abbreviation|multi_cause

> F&B KPI raporunda kahvaltıda bekleme şikayetleri arttı: PMS pax listesi hatası ve HK-F&B koordinasyon eksikliği.

| Varlık | Etiket |
|---|---|
| F&B | DEPARTMENT |
| kahvaltıda bekleme şikayetleri | EVENT |
| PMS pax listesi hatası | ROOT_CAUSE |
| HK-F&B koordinasyon eksikliği | ROOT_CAUSE |

İlişkiler:
- PMS pax listesi hatası —CAUSES→ kahvaltıda bekleme şikayetleri
- HK-F&B koordinasyon eksikliği —CAUSES→ kahvaltıda bekleme şikayetleri
- kahvaltıda bekleme şikayetleri —OCCURS_IN→ F&B

## DENETIM-049  ·  implicit

> Resepsiyon vardiya devrinde özel istek notlarını aktarmadı. Balayı çifti odasında süsleme bulamadı.

| Varlık | Etiket |
|---|---|
| özel istek notlarını aktarmadı | ROOT_CAUSE |
| süsleme bulamadı | EVENT |
| Resepsiyon | DEPARTMENT |

İlişkiler:
- özel istek notlarını aktarmadı —CAUSES→ süsleme bulamadı

## DENETIM-063  ·  explicit

> Asansör bakım sözleşmesinin süresi dolduğundan Teknik Servis periyodik kontrolleri yapamadı ve iki kat servis dışı kaldı.

| Varlık | Etiket |
|---|---|
| bakım sözleşmesinin süresi dolduğundan | ROOT_CAUSE |
| Teknik Servis | DEPARTMENT |
| iki kat servis dışı kaldı | EVENT |
| Asansör | EQUIPMENT |
| periyodik kontrolleri yapamadı | EVENT |

İlişkiler:
- bakım sözleşmesinin süresi dolduğundan —CAUSES→ periyodik kontrolleri yapamadı
- periyodik kontrolleri yapamadı —CAUSES→ iki kat servis dışı kaldı
- periyodik kontrolleri yapamadı —OCCURS_IN→ Teknik Servis

## DENETIM-068  ·  implicit

> Spa terapistlerinin sertifika yenilemeleri takip edilmiyor. Bir terapist süresi dolmuş belgeyle çalışırken yakalandı.

| Varlık | Etiket |
|---|---|
| sertifika yenilemeleri takip edilmiyor | ROOT_CAUSE |
| süresi dolmuş belgeyle çalışırken yakalandı | EVENT |
| Spa | DEPARTMENT |

İlişkiler:
- sertifika yenilemeleri takip edilmiyor —CAUSES→ süresi dolmuş belgeyle çalışırken yakalandı
- süresi dolmuş belgeyle çalışırken yakalandı —OCCURS_IN→ Spa

## DENETIM-070  ·  explicit

> Bar stoklarındaki fark, sayım formlarının doldurulmaması nedeniyle iki ay boyunca fark edilmedi.

| Varlık | Etiket |
|---|---|
| Bar stoklarındaki fark | EVENT |
| sayım formlarının doldurulmaması | ROOT_CAUSE |

İlişkiler:
- sayım formlarının doldurulmaması —CAUSES→ Bar stoklarındaki fark

## DOF-005  ·  negative

> Spa bölümü için yıllık hijyen denetimi tamamlandı. Hijyen puanı 94 olarak kayıtlara işlendi.

| Varlık | Etiket |
|---|---|
| Spa | DEPARTMENT |
| Hijyen puanı | KPI |

İlişkiler: *(yok)*

## DOF-012  ·  explicit

> Kat Hizmetleri'nde personel eksikliği nedeniyle oda hazır olma süresi 45 dakikaya çıktı. Vardiya planı revize edilerek ek personel görevlendirildi.

| Varlık | Etiket |
|---|---|
| Kat Hizmetleri | DEPARTMENT |
| personel eksikliği | ROOT_CAUSE |
| oda hazır olma süresi | KPI |
| oda hazır olma süresi 45 dakikaya çıktı | EVENT |
| ek personel görevlendirildi | ACTION |

İlişkiler:
- personel eksikliği —CAUSES→ oda hazır olma süresi 45 dakikaya çıktı
- oda hazır olma süresi 45 dakikaya çıktı —OCCURS_IN→ Kat Hizmetleri
- oda hazır olma süresi 45 dakikaya çıktı —ADDRESSED_BY→ ek personel görevlendirildi

## DOF-014  ·  implicit

> Misafir İlişkileri'ne bir haftada dört şikâyet geldi. Hepsi akşam yemeği bekleme süresiyle ilgiliydi. Restoranda servis personeli o günler yarı kadrodaydı.

| Varlık | Etiket |
|---|---|
| Misafir İlişkileri | DEPARTMENT |
| dört şikâyet | EVENT |
| yarı kadrodaydı | ROOT_CAUSE |

İlişkiler:
- yarı kadrodaydı —CAUSES→ dört şikâyet
- dört şikâyet —OCCURS_IN→ Misafir İlişkileri

## DOF-015  ·  implicit

> Teknik Servis asansör arızasına müdahale için 40 dakika geç ulaştı. Aynı saatte jeneratör testi yapılıyordu ve ekipte tek kişi vardı.

| Varlık | Etiket |
|---|---|
| Teknik Servis | DEPARTMENT |
| asansör | EQUIPMENT |
| 40 dakika geç ulaştı | EVENT |
| ekipte tek kişi vardı | ROOT_CAUSE |
| jeneratör testi yapılıyordu | ROOT_CAUSE |

İlişkiler:
- ekipte tek kişi vardı —CAUSES→ 40 dakika geç ulaştı
- 40 dakika geç ulaştı —OCCURS_IN→ Teknik Servis
- jeneratör testi yapılıyordu —CAUSES→ 40 dakika geç ulaştı

## DOF-016  ·  abbreviation|chain

> F&B'de HK'dan gelen geç bildirim → salon temizliği gecikti → kahvaltı açılışı 20 dk kaydı. DÖF kapatıldı.

| Varlık | Etiket |
|---|---|
| F&B | DEPARTMENT |
| HK | DEPARTMENT |
| geç bildirim | ROOT_CAUSE |
| salon temizliği gecikti | EVENT |
| kahvaltı açılışı 20 dk kaydı | EVENT |

İlişkiler:
- geç bildirim —CAUSES→ salon temizliği gecikti
- salon temizliği gecikti —CAUSES→ kahvaltı açılışı 20 dk kaydı
- kahvaltı açılışı 20 dk kaydı —OCCURS_IN→ F&B

## DOF-021  ·  explicit

> Havuz pompasının bakım gecikmesi yüzünden havuz suyu bulanıklaştı. Bakım planı güncellendi.

| Varlık | Etiket |
|---|---|
| Havuz pompası | EQUIPMENT |
| bakım gecikmesi | ROOT_CAUSE |
| havuz suyu bulanıklaştı | EVENT |
| Bakım planı güncellendi | ACTION |

İlişkiler:
- bakım gecikmesi —CAUSES→ havuz suyu bulanıklaştı
- havuz suyu bulanıklaştı —ADDRESSED_BY→ Bakım planı güncellendi

## DOF-029  ·  chain

> Kombi fırın bozulunca akşam menüsü kısaltıldı, bekleme süresi uzadı ve misafir memnuniyet puanı düştü.

| Varlık | Etiket |
|---|---|
| Kombi fırın | EQUIPMENT |
| akşam menüsü kısaltıldı | EVENT |
| bekleme süresi uzadı | EVENT |
| misafir memnuniyet puanı | KPI |
| misafir memnuniyet puanı düştü | EVENT |

İlişkiler:
- Kombi fırın —CAUSES→ akşam menüsü kısaltıldı
- Kombi fırın —CAUSES→ bekleme süresi uzadı
- bekleme süresi uzadı —CAUSES→ misafir memnuniyet puanı düştü

## DOF-036  ·  explicit

> Yetersiz stok takibi nedeniyle temizlik malzemesi tükendi. Satın Alma minimum stok seviyesi tanımladı.

| Varlık | Etiket |
|---|---|
| Yetersiz stok takibi | ROOT_CAUSE |
| temizlik malzemesi tükendi | EVENT |
| Satın Alma | DEPARTMENT |
| minimum stok seviyesi tanımladı | ACTION |

İlişkiler:
- Yetersiz stok takibi —CAUSES→ temizlik malzemesi tükendi
- Yetersiz stok takibi —ADDRESSED_BY→ minimum stok seviyesi tanımladı

## DOF-039  ·  implicit

> Gece vardiyasında iki misafir bagajlarının kaybolduğunu söyledi. Teslim kaydı yoktu. Dijital bagaj etiketi uygulamasına geçildi.

| Varlık | Etiket |
|---|---|
| bagajlarının kaybolduğunu | EVENT |
| Teslim kaydı yoktu | ROOT_CAUSE |
| Dijital bagaj etiketi uygulamasına geçildi | ACTION |

İlişkiler:
- Teslim kaydı yoktu —CAUSES→ bagajlarının kaybolduğunu
- Teslim kaydı yoktu —ADDRESSED_BY→ Dijital bagaj etiketi uygulamasına geçildi

## DOF-041  ·  negative

> Satın Alma bu ay 12 tedarikçiyle fiyat görüşmesi yaptı. Yeni sözleşme taslakları hukuk birimine gönderildi.

| Varlık | Etiket |
|---|---|
| Satın Alma | DEPARTMENT |

İlişkiler: *(yok)*

## DOF-045  ·  abbreviation|implicit

> PMS çöktü. Ön Büro rezervasyonları elle girdi; 14 hatalı kayıt oluştu. F&B yanlış kişi sayısıyla hazırlık yaptı.

| Varlık | Etiket |
|---|---|
| PMS | EQUIPMENT |
| Ön Büro | DEPARTMENT |
| 14 hatalı kayıt oluştu | EVENT |
| F&B | DEPARTMENT |
| yanlış kişi sayısıyla hazırlık yaptı | EVENT |

İlişkiler:
- PMS —CAUSES→ 14 hatalı kayıt oluştu
- 14 hatalı kayıt oluştu —CAUSES→ yanlış kişi sayısıyla hazırlık yaptı
- 14 hatalı kayıt oluştu —OCCURS_IN→ Ön Büro
- yanlış kişi sayısıyla hazırlık yaptı —OCCURS_IN→ F&B

## DOF-049  ·  abbreviation

> KPI raporunda F&B hijyen puanı 82'ye geriledi. HK ile ortak denetim yapıldı, DÖF kapsamında personel hijyen eğitimi planlandı.

| Varlık | Etiket |
|---|---|
| hijyen puanı | KPI |
| F&B | DEPARTMENT |
| HK | DEPARTMENT |
| hijyen puanı 82'ye geriledi | EVENT |
| personel hijyen eğitimi planlandı | ACTION |

İlişkiler:
- hijyen puanı 82'ye geriledi —OCCURS_IN→ F&B
- hijyen puanı 82'ye geriledi —ADDRESSED_BY→ personel hijyen eğitimi planlandı

## DOF-052  ·  negative

> Teknik Servis aylık asansör bakım kontrolünü zamanında tamamladı. Tüm cihazlar çalışır durumda teslim edildi.

| Varlık | Etiket |
|---|---|
| Teknik Servis | DEPARTMENT |
| asansör | EQUIPMENT |

İlişkiler: *(yok)*

## DOF-071  ·  multi_cause|chain

> Fırın bakımının yapılmaması ve gaz basıncının düşmesi nedeniyle pişirme süresi uzadı, kahvaltı geç açıldı. Bakım takvimi yeniden düzenlendi.

| Varlık | Etiket |
|---|---|
| Fırın bakımının yapılmaması | ROOT_CAUSE |
| gaz basıncının düşmesi | ROOT_CAUSE |
| pişirme süresi uzadı | EVENT |
| kahvaltı geç açıldı | EVENT |
| Bakım takvimi yeniden düzenlendi | ACTION |

İlişkiler:
- Fırın bakımının yapılmaması —CAUSES→ pişirme süresi uzadı
- gaz basıncının düşmesi —CAUSES→ pişirme süresi uzadı
- pişirme süresi uzadı —CAUSES→ kahvaltı geç açıldı
- Fırın bakımının yapılmaması —ADDRESSED_BY→ Bakım takvimi yeniden düzenlendi

## DOF-073  ·  chain

> Çalışan devir hızı arttı; boş kadrolar doldurulamadı ve kalan ekip fazla mesaiye kaldı, bu da kat kontrol hatalarını artırdı.

| Varlık | Etiket |
|---|---|
| Çalışan devir hızı arttı | EVENT |
| boş kadrolar doldurulamadı | EVENT |
| fazla mesaiye kaldı | EVENT |
| kat kontrol hatalarını artırdı | EVENT |

İlişkiler:
- Çalışan devir hızı arttı —CAUSES→ boş kadrolar doldurulamadı
- boş kadrolar doldurulamadı —CAUSES→ fazla mesaiye kaldı
- fazla mesaiye kaldı —CAUSES→ kat kontrol hatalarını artırdı

## SIKAYET-004  ·  negative

> Genel olarak memnun kalmadım, beklentimi karşılamadı.

| Varlık | Etiket |
|---|---|
| memnun kalmadım | EVENT |

İlişkiler: *(yok)*

## SIKAYET-005  ·  negative

> Merhaba, spa ve masaj fiyat listesini ve açık olduğu saatleri öğrenebilir miyim? Ayrıca gelecek hafta için randevu almak istiyorum.

| Varlık | Etiket |
|---|---|
| spa | DEPARTMENT |

İlişkiler: *(yok)*

## SIKAYET-010  ·  explicit

> Spa'da randevu sisteminde yaşanan hata sebebiyle masajımız iptal oldu, haber veren bile olmadı.

| Varlık | Etiket |
|---|---|
| Spa'da | DEPARTMENT |
| randevu sisteminde yaşanan hata | ROOT_CAUSE |
| masajımız iptal oldu | EVENT |

İlişkiler:
- randevu sisteminde yaşanan hata —CAUSES→ masajımız iptal oldu
- masajımız iptal oldu —OCCURS_IN→ Spa'da

## SIKAYET-013  ·  chain

> Su kaçağı tavanı ıslattı, nem yüzünden odadaki halı koktu, biz de odayı değiştirmek zorunda kaldık.

| Varlık | Etiket |
|---|---|
| Su kaçağı | EVENT |
| halı koktu | EVENT |
| odayı değiştirmek zorunda kaldık | EVENT |
| tavanı ıslattı | EVENT |

İlişkiler:
- halı koktu —CAUSES→ odayı değiştirmek zorunda kaldık
- Su kaçağı —CAUSES→ tavanı ıslattı
- tavanı ıslattı —CAUSES→ halı koktu

## SIKAYET-016  ·  informal|implicit

> yaw odada bi tane bile priz çalışmıyo, telefonu şarj edemedim. teknikciler gelcem dedi gelmedi

| Varlık | Etiket |
|---|---|
| priz | EQUIPMENT |
| şarj edemedim | EVENT |
| teknikciler | DEPARTMENT |
| gelmedi | EVENT |

İlişkiler:
- priz —CAUSES→ şarj edemedim
- gelmedi —OCCURS_IN→ teknikciler

## SIKAYET-027  ·  explicit

> Güvenlik görevlisinin kimlik kontrolü yapmaması yüzünden odamıza yetkisiz biri girmiş, valizim karışmıştı.

| Varlık | Etiket |
|---|---|
| Güvenlik görevlisinin | DEPARTMENT |
| kimlik kontrolü yapmaması | ROOT_CAUSE |
| odamıza yetkisiz biri girmiş | EVENT |
| valizim karışmıştı | EVENT |

İlişkiler:
- kimlik kontrolü yapmaması —CAUSES→ odamıza yetkisiz biri girmiş
- odamıza yetkisiz biri girmiş —OCCURS_IN→ Güvenlik görevlisinin
- odamıza yetkisiz biri girmiş —CAUSES→ valizim karışmıştı

## SIKAYET-034  ·  implicit

> Restoranda üç kişilik rezervasyonumuz vardı ama masa hazır değildi. Kapıdaki hanım defterine bile bakmadı.

| Varlık | Etiket |
|---|---|
| Restoranda | DEPARTMENT |
| defterine bile bakmadı | ROOT_CAUSE |
| masa hazır değildi | EVENT |

İlişkiler:
- defterine bile bakmadı —CAUSES→ masa hazır değildi
- masa hazır değildi —OCCURS_IN→ Restoranda

## SIKAYET-042  ·  informal|explicit

> arkadaş ya bu kadar da olmaz, sabahtan beri su sesi geliyo tavandan, ses yüzünden uyuyamadım resmen

| Varlık | Etiket |
|---|---|
| su sesi geliyo | EVENT |
| uyuyamadım | EVENT |

İlişkiler:
- su sesi geliyo —CAUSES→ uyuyamadım

## SIKAYET-047  ·  multi_cause

> Hem personel eğitimsizliği hem de sistemin yavaşlığı nedeniyle check-in yarım saat sürdü; kuyrukta bekleyen yaşlı eşim fenalaştı.

| Varlık | Etiket |
|---|---|
| personel eğitimsizliği | ROOT_CAUSE |
| sistemin yavaşlığı | ROOT_CAUSE |
| check-in yarım saat sürdü | EVENT |
| yaşlı eşim fenalaştı | EVENT |

İlişkiler:
- personel eğitimsizliği —CAUSES→ check-in yarım saat sürdü
- sistemin yavaşlığı —CAUSES→ check-in yarım saat sürdü
- check-in yarım saat sürdü —CAUSES→ yaşlı eşim fenalaştı

## SIKAYET-052  ·  abbreviation|explicit

> HK az personelle çalışıyormuş, o yüzden oda hazır olma süresi 4 saat olmuş. F&B de aynı durumda.

| Varlık | Etiket |
|---|---|
| HK | DEPARTMENT |
| az personelle çalışıyormuş | ROOT_CAUSE |
| oda hazır olma süresi | KPI |
| 4 saat olmuş | EVENT |
| F&B | DEPARTMENT |

İlişkiler:
- az personelle çalışıyormuş —CAUSES→ 4 saat olmuş
- 4 saat olmuş —OCCURS_IN→ HK

## SIKAYET-058  ·  chain

> Çatıdaki sızıntı fark edilmedi, tavan alçıpanı çöktü, üstelik güvenlik şeridi çekilmediği için lobide bir misafir yaralandı.

| Varlık | Etiket |
|---|---|
| Çatıdaki sızıntı fark edilmedi | ROOT_CAUSE |
| tavan alçıpanı çöktü | EVENT |
| güvenlik şeridi çekilmediği | ROOT_CAUSE |
| lobide bir misafir yaralandı | EVENT |

İlişkiler:
- Çatıdaki sızıntı fark edilmedi —CAUSES→ tavan alçıpanı çöktü
- tavan alçıpanı çöktü —CAUSES→ lobide bir misafir yaralandı
- güvenlik şeridi çekilmediği —CAUSES→ lobide bir misafir yaralandı

## SIKAYET-060  ·  negative

> Misafir İlişkileri'nden evcil hayvan politikasını öğrenmek istiyorum.

| Varlık | Etiket |
|---|---|
| Misafir İlişkileri'nden | DEPARTMENT |

İlişkiler: *(yok)*

## SIKAYET-061  ·  explicit

> Bulaşık makinesinin deterjan dozajı yanlış ayarlandığı için bardaklarda beyaz lekeler vardı, akşam yemeğinde su içemedik.

| Varlık | Etiket |
|---|---|
| Bulaşık makinesinin | EQUIPMENT |
| deterjan dozajı yanlış ayarlandığı | ROOT_CAUSE |
| bardaklarda beyaz lekeler vardı | EVENT |

İlişkiler:
- deterjan dozajı yanlış ayarlandığı —CAUSES→ bardaklarda beyaz lekeler vardı
- Bulaşık makinesinin —CAUSES→ bardaklarda beyaz lekeler vardı

## SIKAYET-067  ·  implicit

> Barda bardaklar kirliydi, barmen çok yorgun görünüyordu. Üç barmen yerine tek kişi çalışıyormuş.

| Varlık | Etiket |
|---|---|
| bardaklar kirliydi | EVENT |
| tek kişi çalışıyormuş | ROOT_CAUSE |
| barmen çok yorgun görünüyordu | EVENT |

İlişkiler:
- tek kişi çalışıyormuş —CAUSES→ bardaklar kirliydi
- tek kişi çalışıyormuş —CAUSES→ barmen çok yorgun görünüyordu

## SIKAYET-075  ·  implicit

> Koşu bandı üç haftadır arızalı yazıyor. Spor için geldik, tatilimiz boşa gitti.

| Varlık | Etiket |
|---|---|
| Koşu bandı | EQUIPMENT |
| arızalı | EVENT |
| tatilimiz boşa gitti | EVENT |

İlişkiler:
- Koşu bandı —CAUSES→ tatilimiz boşa gitti
- arızalı —CAUSES→ tatilimiz boşa gitti
