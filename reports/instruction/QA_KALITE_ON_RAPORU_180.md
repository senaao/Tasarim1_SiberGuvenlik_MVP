# 180 Soru-Cevap Kalite Kontrolü — Model Destekli Ön İnceleme

**Kapsam:** Siber güvenlik SFT veri setinden 180 soru (12 konu × 15, train 120 / val 36 / test 24), 179 farklı kaynak belge. **İnceleme türü:** Model destekli, dosyadaki soru/cevap ve en fazla ~2.000 karakterlik kaynak pasajıyla yapılan ön inceleme. **Uzman/insan kalite kararı verilmemiştir.**

## Kısa sonuç

| Ön inceleme sınıfı | Kayıt | Ne demek? |
|---|---:|---|
| `ELE_ADAYI` | **12** | Belirgin anlam/teknik çelişki veya yetersiz cevap, yeniden yazılmadan çıkarılması önerilir. |
| `DUZELT` | **18** | Düzeltilebilecek soru/cevap veya OCR hatası. |
| `ALAN_DISI` | **25** | Kaynağı doğru olsa da istenen teknik siber güvenlik odağının dışında. |
| `YANLIS_KONU` | **33** | Soru güvenlikle ilgili ama 12 etiket arasında yanlış yerleştirilmiş. |
| `KAYNAK_KONTROL` | **3** | Kaynak pasajı iddiayı yeterince kanıtlamıyor ya da ekleme var. |
| `GUNCELLIK_KONTROL` | **2** | Tarih/sürüm/politika doğrulaması gerekiyor. |
| `KONU_KONTROL` | **22** | Konu ilişkisi veya öğretim değeri sınırda, insan kararı gerekiyor. |
| `KANIT_ZAYIF_ON_TARAMA` | **9** | Otomatik kelime örtüşmesi düşük; tam kaynak doğrulaması gerekli. |
| `ILK_TARAMADA_BELIRGIN_HATA_YOK` | **56** | İlk tarama görünür bir hata yakalamadı; doğrulanmış demek değildir. |

**Toplam: 180 kayıt.** Öncelik sayıları: kritik 12, yüksek 43, orta 69, düşük 56.

**Yorumlama uyarısı:** Bu sayılar bilimsel hata oranı/insan doğruluk oranı değildir. Kategori ve kaynak eşleşmeleri ön inceleme sınıflarıdır. `model_kaynak_kelime_ortusmesi` yalnızca kelime benzerliği ölçer; yanıtın gerçekliğini kanıtlamaz. Özellikle sayısal kısa cevaplarda skor yanıltıcı olabilir. Doğruluğu göründüğü hâlde güncelliği değişen politikalar/sürümler uzman tarafından kontrol edilmelidir.

## Birinci öncelik: belirgin yanlış veya güvenilmez örnekler

| Satır | Konu | Saptanan sorun |
|---:|---|---|
| 8 | Authentication | Matematiksel semboller/koşul PDF çıkarımında birleşmiş; i=1 ile kabul koşulunun ifadesi doğrulanamıyor. Ayrıca kriptografik kanıt devresi sorusu kimlik doğrulama alanıyla zayıf ilişkili. |
| 21 | Cloud Security | Kaynakta bu güven düzeyi bir soru olarak geçiyor, kesin yanıt ve gerekçe verilmemiş; modelin ürettiği güven açıklaması pasajla kanıtlanmıyor. |
| 78 | Incident Response | AC-16 NIST kontrolü güvenlik/gizlilik öznitelikleriyle ilgilidir; "Separation of Duties" AC-5 ile ilişkilidir. PDF tablosu OCR sırasında karışmış. |
| 79 | Incident Response | Kaynak pasajındaki "outside PIAtlas" notları gerçek alt teknikler olarak kopyalanmış; üç alt tekniği tutarlı saymıyor. |
| 92 | Malware | Kaynakta "Önerilen süre: 15 dakika" öğretim bölümünün ders süresidir; kötü amaçlı yazılım temizliği için 15 dakikalık operasyonel öneri değildir. |
| 101 | Malware | DMARC e-posta alanı doğrulamasıdır; unsigned ActiveX mobil kodunu kısıtlamaz. PDF metninde farklı iki satır/sütun birleşmiş olabilir. |
| 120 | Mobile Security | App ID/client secret tek başına CSRF savunması değildir; kaynak bağlamı OAuth API kimlik doğrulamaya ait. Soru ve cevap teknik açıdan karışmış. |
| 137 | Penetration Testing | Kaynak "narrated card let 0.54 attacks THROUGH" diyor (engellenmedi); yanıt tam tersine %54 engellendi diyor. |
| 149 | Penetration Testing | "36 hafta" bulgusu kaynak pasajında desteklenmiyor; kaynak yalnızca Spring 2024 ve haftalık bayrak yakalama grafiğini anıyor. Muhtemel tablo/grafik okuma hatası. |
| 166 | Web Security | PDF metnindeki bozuk URL parçası (points/wpa3-...) yanıta girmiş; ayrıca Wi-Fi protokolleri Web Security kategorisinde yanlış. |
| 169 | Web Security | Soru tam HTML içeriğini istiyor; kaynakta satır ve içerik farklı, yanıt birleştirilmiş/hatalı. Ayrıca örnek HTML sayfası web güvenliği becerisi değil. |
| 176 | Web Security | Soru beş kategori istiyor; yanıt yalnızca üç öğe listeliyor. Kaynak pasajı da üç maddeden sonra kesilmiş. |

## İkinci öncelik: düzeltilmesi gerekenler

| Satır | Düzeltilmesi gereken nokta |
|---:|---|
| 2 | Yanıt gerçek rol/personel belirtmiyor; ODP[01] yapılandırılacak bir parametre. Parametreli kontrol olarak yeniden sorulmalı. |
| 3 | Soru Kerberos şifreleme türünü soruyor; pasaj simetrik anahtarlı kriptografiyi açıklıyor, yanıtta tür doğrudan söylenmiyor. |
| 11 | Soru hangi yöntem olduğunu soruyor; cevap yalnızca belgelemede yöntemin belirtilmesi gerektiğini tekrar ediyor. Belirli yöntem verilmemiş. |
| 12 | Kaynak OCR bozuk ve "may be inventoried semi-annually" ifadesi görünüyor; cevap bunu normatif "should" olarak genelliyor. |
| 30 | Soru F1 puanını istiyor; cevap F1 değeri vermeyip enerji/verimlilik karşılaştırmasını anlatıyor. |
| 32 | glibc 2.25+ getrandom arayüzüyle ilişkili; Linux özel dosyası olarak sorulması API/dosya kavramlarını karıştırıyor. |
| 35 | Kaynak 48-bit paket numarasının nonce oluşturduğunu söylüyor; yanıt anahtarın KeyID+PN ile türetildiğini iddia ediyor. CCMP nonce ve anahtar ayrılmalı. |
| 48 | Kaynakta PDF ayrıştırma kaynaklı 95:4% yazımı var; cevap bu bozuk değeri koruyor. %95,4 olarak özgün dokümandan teyit gerekli. |
| 69 | Soru veri biçimini soruyor; yanıt belirli dosya biçimini vermiyor, RTC/trimleme koşullarından söz ediyor. |
| 86 | Kaynak bir ölçülmesi gereken süreyi listeliyor, sayısal aralık vermiyor. "Belirtilmedi" cevabı yerine ölçütü açıklayan soru yazılmalı. |
| 94 | Violin grafiği dosya boyutlarını gösterirken yanıt farklı tespit sayısı grafiğinin ransomware karşılaştırmasını dosya boyutuna yüklüyor. |
| 98 | /etc/passwd bir dosyadır, klasör değil. Kaynak da yanlış "folder" diyor; soruyu dosya okuma/directory traversal bulgusu olarak düzelt. |
| 107 | Yanıt SDK eşik değerini vermiyor; kaynak hedef SDK <31 için izin denetimi baypasından söz ediyor. |
| 116 | Kaynak 5,0–8,0 m gibi örnek yakınlık aralığı veriyor; kesin maksimum mesafe ilan etmiyor. |
| 124 | PDF OCR kaynağındaki yazım bozukluğu yanıtı etkilemiş (DNNSEC, DNSSecurity). Ayrıca son RFC maddesi cevapta kesilmiş. |
| 135 | "Benchmark dataset" cevabı çok genel; gerçek veri setinin niteliğini açıklamıyor. |
| 165 | Yanıt Root of Trust ailesinin secure boot/anahtar yönetimini RTM özel işlevi gibi anlatıyor; kaynak RTM için yalnızca ölçüm/bütünlük odağı belirtiyor. |
| 170 | Güvenli HTTP yöntemi seçimi önemli ancak tek başına CSRF önlemi değildir; kaynakta bağlamı tam kontrol edilmeli. |

## Doğru kaynak olsa bile konu filtresinden geçmeyen sorular

**Alan dışı örnekler (satır numaraları):** 19, 22, 25, 26, 39, 40, 41, 42, 45, 55, 59, 62, 72, 83, 84, 102, 106, 109, 110, 123, 144, 153, 154, 168, 172.

**Yanlış konu etiketi adayları:** 5 → System Security, 6 → Cryptography, 7 → Cryptography, 16 → System Security, 20 → Incident Response, 24 → System Security, 28 → System Security, 37 → Authentication, 43 → Authentication, 50 → Malware, 60 → System Security, 61 → System Security, 63 → Incident Response, 64 → System Security, 65 → Incident Response, 70 → System Security, 71 → Penetration Testing, 74 → System Security, 80 → Malware, 87 → Digital Forensics, 88 → Authentication, 89 → Incident Response, 91 → Web Security, 100 → Malware, 115 → System Security, 117 → Network Security, 118 → System Security, 128 → Incident Response, 131 → System Security, 140 → Incident Response, 160 → Web Security, 162 → Network Security, 173 → Web Security.

## Konu dağılımı (sadece ön inceleme)

| Konu | Kritik | Düzeltme | Alan dışı | Yanlış kategori | Diğer işaretli | Belirgin hata yok (ön tarama) |
|---|---:|---:|---:|---:|---:|---:|
| Authentication | 1 | 4 | 0 | 3 | 2 | 5 |
| Cloud Security | 1 | 1 | 4 | 4 | 3 | 2 |
| Cryptography | 0 | 2 | 5 | 2 | 1 | 5 |
| DevSecOps | 0 | 1 | 2 | 2 | 5 | 5 |
| Digital Forensics | 0 | 1 | 2 | 7 | 2 | 3 |
| Incident Response | 2 | 1 | 2 | 4 | 3 | 3 |
| Malware | 2 | 2 | 1 | 2 | 1 | 7 |
| Mobile Security | 1 | 2 | 3 | 3 | 1 | 5 |
| Network Security | 0 | 2 | 1 | 2 | 5 | 5 |
| Penetration Testing | 2 | 0 | 1 | 1 | 5 | 6 |
| System Security | 0 | 1 | 2 | 2 | 4 | 6 |
| Web Security | 3 | 1 | 2 | 1 | 4 | 4 |

## Yöntem ve sınırlılıklar

- CSV içindeki 180 soru/cevap, kaynak dosya adı ve `kaynak_pasaji` alanları değerlendirildi. Kaynak pasajları yaklaşık 2.000 karakterle kesilmiş; bazı soruların grafik, tablo, denklem veya daha önceki sayfalardaki kanıtları bu kesitte bulunmayabilir.
- Belirgin kavramsal çelişkiler, soru-cevap uyuşmazlıkları, PDF/OCR kaynaklı hatalar, kategori kayması ve teknik alan dışı örnekler ayrı işaretlendi.
- Modelin özellikle işaretlemediği kayıtlarda otomatik kaynak kelime örtüşmesiyle ilk ön tarama yapıldı. Bu satırlar **semantik olarak doğrulandı** anlamına gelmez; nihai değerlendirmeleri boş bırakıldı.
- Dosyadaki `insan_karari`, `inceleyen`, `inceleme_tarihi` ve `inceleme_notu` alanlarına **dokunulmadı**. `verified=True` olarak hiçbir kayıt işaretlenmedi.
- Bu inceleme yalnızca **180 örneklem** içindir; tüm 3.075 soru-cevabın aynı oranlarda hata içerdiği çıkarılamaz.

## Bir sonraki kontrollü işlem

**Önce kritik örnekleri ana instruction/SFT setinden otomatik kaldırma;** çünkü train/val/test eşleştirmesi bozulabilir. Önce işaretli örneklerin uzman kontrolünü ve düzeltilmiş yanıtlarını tamamla, sonra aynı kaynak temelli split kurallarıyla yeni, sürümlenmiş bir veri seti çıkar. Başta 3, 21, 30, 35, 78, 92, 101, 120, 137, 149, 176 gibi yüksek riskli satırlar incelenebilir.

**Saklanacak dosyalar:** `QA_KALITE_INCELEME_ORNEKLEMI_180.csv` (orijinal), `QA_MODEL_ON_INCELEME_180.csv` (model notları), `QA_KALITE_ON_RAPORU_180.md` (bu rapor).
