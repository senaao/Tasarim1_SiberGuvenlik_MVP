# SFT kritik 12 kayit: ayirma ve izlenebilirlik raporu

**Durum:** Otomatik ON ELEME / KARANTINA; uzman veya insan nihai karari DEGIL.

180 soruluk incelemeden ELE_ADAYI etiketi alan 12 SFT kaydi, 
yeni gecici SFT aday dosyalarindan AYRI tutuldu. Diger 168 orneklem
kaydi dahil kalan butun sorular onaylanmis kabul EDILMEMELIDIR.
Orijinal 3.075 QA ve SFT veri dosyalari degistirilmedi.

| Bolme | Onceki SFT | Karantina | Gecici SFT adayi |
|---|---:|---:|---:|
| train | 2418 | 8 | 2410 |
| val | 359 | 2 | 357 |
| test | 298 | 2 | 296 |
| **Toplam** | **3075** | **12** | **3063** |

## Kritik 12 kayit - gerekceler

| Orneklem sirasi | ID | Modelin gerekcesi |
|---:|---|---|
| 8 | `draft_0298` | Matematiksel semboller/koşul PDF çıkarımında birleşmiş; i=1 ile kabul koşulunun ifadesi doğrulanamıyor. Ayrıca kriptografik kanıt devresi sorusu kimlik doğrulama alanıyla zayıf ilişkili. |
| 21 | `batch1000_0967` | Kaynakta bu güven düzeyi bir soru olarak geçiyor, kesin yanıt ve gerekçe verilmemiş; modelin ürettiği güven açıklaması pasajla kanıtlanmıyor. |
| 78 | `kaggle1000_0718` | AC-16 NIST kontrolü güvenlik/gizlilik öznitelikleriyle ilgilidir; "Separation of Duties" AC-5 ile ilişkilidir. PDF tablosu OCR sırasında karışmış. |
| 79 | `kaggle1000_0526` | Kaynak pasajındaki "outside PIAtlas" notları gerçek alt teknikler olarak kopyalanmış; üç alt tekniği tutarlı saymıyor. |
| 92 | `batch1000_0884` | Kaynakta "Önerilen süre: 15 dakika" öğretim bölümünün ders süresidir; kötü amaçlı yazılım temizliği için 15 dakikalık operasyonel öneri değildir. |
| 101 | `batch_new500_0432` | DMARC e-posta alanı doğrulamasıdır; unsigned ActiveX mobil kodunu kısıtlamaz. PDF metninde farklı iki satır/sütun birleşmiş olabilir. |
| 120 | `batch_new500_0481` | App ID/client secret tek başına CSRF savunması değildir; kaynak bağlamı OAuth API kimlik doğrulamaya ait. Soru ve cevap teknik açıdan karışmış. |
| 137 | `batch1000_0258` | Kaynak "narrated card let 0.54 attacks THROUGH" diyor (engellenmedi); yanıt tam tersine %54 engellendi diyor. |
| 149 | `kaggle1000_0374` | "36 hafta" bulgusu kaynak pasajında desteklenmiyor; kaynak yalnızca Spring 2024 ve haftalık bayrak yakalama grafiğini anıyor. Muhtemel tablo/grafik okuma hatası. |
| 166 | `batch1000_0472` | PDF metnindeki bozuk URL parçası (points/wpa3-...) yanıta girmiş; ayrıca Wi-Fi protokolleri Web Security kategorisinde yanlış. |
| 169 | `batch_new500_0386` | Soru tam HTML içeriğini istiyor; kaynakta satır ve içerik farklı, yanıt birleştirilmiş/hatalı. Ayrıca örnek HTML sayfası web güvenliği becerisi değil. |
| 176 | `batch500_0012` | Soru beş kategori istiyor; yanıt yalnızca üç öğe listeliyor. Kaynak pasajı da üç maddeden sonra kesilmiş. |

## Diger bekleyen kontroller

- Toplam orneklem: 180; otomatik siniflar: {'ILK_TARAMADA_BELIRGIN_HATA_YOK': 56, 'DUZELT': 18, 'YANLIS_KONU': 33, 'ELE_ADAYI': 12, 'KAYNAK_KONTROL': 3, 'KANIT_ZAYIF_ON_TARAMA': 9, 'KONU_KONTROL': 22, 'ALAN_DISI': 25, 'GUNCELLIK_KONTROL': 2}.
- 25 alan-disi adayi, 18 duzeltme adayi, 33 yanlis konu adayi ve diger
  kayitlar bu adimda SILINMEDI veya DUZELTILMEDI. Sonraki denetime kaldi.
- Kalan 3.063 SFT ornegi **insan dogrulamasi yapilmis temiz set degildir**.
- Kaynak belgeler, ID ve train/val/test atamalari ayni kalmistir.
- Ana SFT teslimini degistirmek icin tum kontrol kararlarini ve surumlemeyi tamamla.
