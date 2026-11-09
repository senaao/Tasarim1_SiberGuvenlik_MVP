# PDF kaynak envanteri ve Domain Corpus eşleştirmesi — ön inceleme

**Tarih:** 9 Kasım 2026  
**Girdiler:** `pdf_kaynak_envanteri.csv` (yerel PDF taraması), `source_inventory.csv` (731 Corpus kaynak kaydı).  
**Durum:** Dosya adı eşleştirmesi tamamlandı; kaynak URL, lisans ve içerik doğrulaması tamamlanmadı.

## 1. Sayısal sonuç

| Ölçüt | Sonuç |
|---|---:|
| `data/raw` altında taranan PDF | **1.283** |
| PDF olarak açılabilen | **1.282** |
| PDF olarak açılamayan | **1** |
| Corpus kaynak envanterindeki belge adı | **731** |
| Corpus belgesiyle PDF dosya adı eşleşen | **731 / 731** |
| Corpus dışındaki PDF sayısı | **552** |
| Corpus içindeki toplam chunk | **9.554** |
| Corpus'a eşleşen PDF'lerde en az bir URL adayı görünen | **175 / 731** |
| Corpus PDF'lerinde doldurulmuş doğrulanmış özgün indirme URL'si | **0** |
| Corpus PDF'lerinde doğrulanmış lisans kaydı | **0** |

**Eşleştirme yöntemi:** PDF ve `source_document` dosya adlarından `.pdf`/`.txt` uzantısı çıkarılıp harf-rakam normalize edildi. Tüm 731 Corpus kaynak adı envanterde **tek bir** PDF adıyla eşleşti. Bu, yerel dosya izlenebilirliğini güçlendirir; PDF içeriğinin Corpus'a birebir aktarıldığını tek başına kanıtlamaz.

**Önemli sayı farkı:** 1.283 ham PDF, 731 farklı Corpus kaynağı ve 9.554 chunk farklı aşamaları ifade eder. **552 PDF'nin neden Corpus'a alınmadığının neden bazlı kaydı bu envanterde yoktur**; bunların tamamına 'başarısız/elenmiş' denmemelidir.

## 2. Hocanın kaynak tablosu için ilk kaynak grupları

Aşağıdaki sınıflar ilk otomatik PDF meta veri taramasındaki aday etiketlerdir. **Yayımlayıcı ve lisans açısından resmen doğrulanmış kaynaklar değildir.** `NIST (tahmini)` gibi etiketler yalnızca metinde atıf geçmesinden de kaynaklanabilir; bu nedenle ilgili PDF'leri resmî NIST yayını saymadık.

| İlk taramadaki aday grup | Tüm 1.283 PDF | Corpus'a eşleşen 731 PDF | Güven |
|---|---:|---:|---|
| NIST | 64 | 58 | Adı belirgin, doğrulama gerekli |
| OWASP | 3 | 3 | Adı belirgin, doğrulama gerekli |
| ENISA | 5 | 5 | Adı belirgin, doğrulama gerekli |
| NIST (tahmini) | 77 | 57 | Düşük güven |
| OWASP (tahmini) | 5 | 4 | Düşük güven |
| MITRE (tahmini) | 4 | 3 | Düşük güven |
| SANS (tahmini) | 1 | 1 | Düşük güven |
| Belirlenemedi | 1124 | 600 | Bilinmiyor |
| **Toplam** | **1.283** | **731** | |

**Sunumda dürüst anlatım:** "1.283 PDF toplandı; son Corpus'ta 731 belgeye ait 9.554 metin parçası yer alıyor. Yerel belge adları 731 PDF ile eşleştirildi. Kaynak kurumları ve lisansların tamamı henüz doğrulanmadı." 

`NIST + OWASP + ENISA` adı belirgin kayıtlar toplamı Corpus'ta **66** belgedir; kalan **665** kayıt için yayımlayıcı veya kurum ilişkisi ek kontrol gerektirir. **Kurum belirsizliği, teknik içerik bulunmadığı anlamına gelmez**; büyük kısmı araştırma makalesi veya başka doküman olabilir.

## 3. URL ve lisans durumları

- Kaynak PDF'lerin içinden tespit edilen **175** URL adayı, PDF'nin *özgün indirme URL'si* olmak zorunda değildir. Örneğin kaynakça atfı, DOI, GitHub, çalışma web sitesi veya yer tutucu bağlantı olabilir.
- Orijinal `data_sources.csv` dosyasındaki genel kurum/lisans beyanları, tekil 731 PDF'nin lisansı doğrulanmış anlamına gelmez.
- `source_inventory.csv` dosyasındaki tüm 731 kaynak için lisans durumu `NOT_VERIFIED` olarak kalır. Bunları doğrulanmış açık lisans gibi raporlamayın.
- Bilimsel makaleler, kitaplar ve teknik raporların telif hakları kurum adından otomatik çıkarılamaz. Özellikle rastgele sitelerden indirilen kitapların yeniden dağıtım izni ayrıca incelenmelidir.
- GitHub'da tam PDF'ler ve tam Corpus/Instruction metinleri lisans kontrolü yapılmadan yayımlanmamalıdır.

## 4. Teknik kalite sınırlamaları

- Tarama sonuçlarında **1 PDF açılamadı**: `Bringing data minimization to digital wallets at scale with.pdf`. Bu dosya 731 Corpus kaynağı arasında değildir.
- `read_status=OK`, PDF'nin açılabildiğini gösterir; bütün sayfaların sorunsuz çıkarıldığını veya metnin temiz olduğunu kanıtlamaz. PDF motorunun uyarı vermesi mümkündür.
- Corpus'a eşleşen PDF'lerin **43** tanesi için ilk sayfa metin örneği boş kalmıştır. Bunlar mutlaka bozuk değildir, fakat metin çıkarımı açısından incelenmelidir.
- Bazı PDF başlıkları teknik siber güvenlik yerine idari rapor, genel politika veya başka konular içeriyor olabilir. Bu nedenle belge düzeyinde teknik kapsam kontrolü de yapılmalıdır.
- **Şu ana kadar içerik bazlı PDF–Corpus karşılaştırması yapılmadı.** Eşleşmeler isim bazlıdır.

## 5. Bir sonraki iş akışı

1. Eşleşen 731 kaydın kurum/yayımlayıcı bilgilerini ve gerçek indirildikleri URL'yi indirme kayıtları, PDF kapak sayfaları ve gerekirse resmî kaynak sayfalarından doğrulamak.
2. Kapsam dışı/içerik kalitesi düşük belgeleri gerekçeyle işaretlemek; ham PDF sayısı ile Corpus sayısı arasındaki farkı silinme/filtrelenme olarak varsaymamak.
3. Güncellenmiş kaynak tablosunu sunuma aktarmak; URL ve lisans için `DOĞRULANMADI` bilgisini korumak.

**İlgili makine-okunur dosya:** `PDF_KAYNAK_ESLESME_1283.csv` (1.283 satır, Corpus'a giriş işareti, PDF başlık/sayfa sayısı, ilk kurum adayı ve teyit durumları). Bu rapordaki 731 sayısı dosya adı eşleştirmesine dayanır; daha ileri içerik doğrulaması henüz yapılmamıştır.
