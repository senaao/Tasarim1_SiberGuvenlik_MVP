# Siber Güvenlik Veri Seti — Kaynak Tablosu (Sunum İçin Ön Sürüm)

**Tarih:** 9 Kasım 2026  
**Girdi:** Kullanıcının `pdf_kaynak_envanteri.csv` taraması ve 731 Corpus belge adıyla yerel PDF eşleştirmesi.  
**Yöntem:** PDF ilk sayfa örneği, başlık meta verisi, dosya adı ve yerel eşleştirme. **Kaynakların tekil indirme adresi / lisansı dış kaynaklarla topluca doğrulanmadı.**

## Slayta konabilecek kaynak tablosu

| Kaynak grubu (ön sınıf) | Adet | Tür | Dil: ilk sayfa tahmini (EN / TR / belirsiz) | Belgeye özel URL | Lisans |
|---|---:|---|---|---|---|
| NIST (yayın adayı) | **108** | NIST SP/IR, güvenlik rehberi, teknik yayın | 87 / 0 / 21 | Doğrulanmadı | NOT_VERIFIED |
| OWASP (doküman adayı) | **5** | Uygulama güvenliği standardı ve rehberi | 1 / 0 / 4 | Doğrulanmadı | NOT_VERIFIED |
| ENISA (yayın adayı) | **5** | Tehdit analizi, sektör raporu | 1 / 0 / 4 | Doğrulanmadı | NOT_VERIFIED |
| OWASP konulu / yayımcı belirsiz | **1** | OWASP konulu belge; kurum doğrulanmadı | 0 / 0 / 1 | Doğrulanmadı | NOT_VERIFIED |
| MITRE bağlantılı araştırma | **1** | MITRE bağlantılı yazarlı araştırma | 1 / 0 / 0 | Doğrulanmadı | NOT_VERIFIED |
| SANS bağlantılı doküman | **1** | SANS bağlantılı teknik doküman | 1 / 0 / 0 | Doğrulanmadı | NOT_VERIFIED |
| NIST ile ilişkili diğer | **2** | NIST taslak/yorum derlemesi | 1 / 0 / 1 | Doğrulanmadı | NOT_VERIFIED |
| Diğer araştırma makalesi adayları | **353** | Akademik makale formatı; yayımcı belirsiz | 328 / 0 / 25 | Doğrulanmadı | NOT_VERIFIED |
| Diğer / belirlenemeyen | **255** | Tür/yayımcı henüz sınıflanmadı | 160 / 4 / 91 | Doğrulanmadı | NOT_VERIFIED |
| **TOPLAM** | **731** | | **580 / 4 / 147** | **Doğrulanmadı** | **NOT_VERIFIED** |

**Tablo başlığı önerisi:** *Corpus'taki 731 belge için ilk sayfa ve dosya adına dayalı kaynak grubu ön sınıflandırması.*

**Önemli:** 'Araştırma makalesi adayı' bir yayımlayıcı adı değildir; belge türüdür. 'MITRE ile ilişkili' yazar kurumu anlamına gelebilir; kurumun yayımladığı resmi rapor demek değildir. **Hiçbir satır tamamen teyit edilmiş yayıncı/lisans listesi olarak sunulmamalıdır.**

## Sayısal veri hattı — ayrı slaytta kullan

| Aşama | Sayı | Not |
|---|---:|---|
| `data/raw` altında bulunan PDF | **1.283** | Alt klasörler dahil |
| PDF olarak açılabilen | **1.282** | Açılması, tüm metnin doğru çıkarıldığı anlamına gelmez |
| PDF olarak açılamayan | **1** | Corpus'a eşleşen 731 kaynak içinde değil |
| PDF adı Corpus kaynak adıyla eşleşen | **731** | Yalnız dosya adı temelli; birebir içerik karşılaştırması yok |
| Corpus'a adıyla eşleşmeyen ham PDF | **552** | Neden dışarıda kaldıkları bu tabloyla bilinmiyor |
| Son Corpus metin parçası | **9.554** | Ayrı corpus istatistiği |

## Bu sürümde düzelen nokta

Önceki raporda **58 NIST ve 3 OWASP** adayı ilk otomatik tarama etiketinden sayılmıştı. Bu sürümde ilk sayfa kapak örneklerine ve yayın kodlarına da bakılarak gruplama genişletildi. **Bu yeni sayılar yayıncı tarafından tek tek doğrulanmış sayılar değildir.** Bir araştırma makalesinde NIST/OWASP'tan yalnızca söz edilmesi kurumsal yayın sayılmadı.

## Dil ön taraması (yalnızca ilk sayfaya göre)

| Etiket | Belge |
|---|---:|
| İngilizce olabilir (`EN_ON_TAHMIN`) | 580 |
| Türkçe olabilir (`TR_ON_TAHMIN`) | 4 |
| Belirlenemedi | 147 |

Bu değerler tüm PDF'nin dili teyit edilmiş değerler **değildir**. İlk sayfada az metin varsa veya çok dilli içerik varsa hata olabilir. Sunumda kesin dil dağılımı olarak kullanmak yerine dil analizinin ön sonuçları olarak sunun.

## İzlenebilirlik / doğrulama durumu

- İlk PDF envanteri: 1.283 satır; Corpus eşleştirme envanteri: 731 satır.
- 731 PDF adı Corpus'taki 731 `source_document` adıyla eşleşiyor; bu **içerik eşitliği** demek değil.
- Corpus'a eşleşen PDF'lerin **43** tanesinde ilk sayfa metin örneği boş; PDF'nin tamamının okunamaz olduğuna işaret etmeyebilir.
- Corpus'a eşleşen PDF'lerde **175** PDF-içi URL adayı vardı. Bu URL'lerin bir kısmı dipnot/kaynakça/DOI olabilir; **indirilen PDF'nin kaynak URL'si olarak doğrulanmış 0** kayıt var.
- **731/731** kaynak için lisans `NOT_VERIFIED` durumunda.
- `NIST_SP800_61r2_Olay_Mudahale.pdf` belgesinin kapak örneğinde **"Withdrawn" (yürürlükten kaldırılmış/geri çekilmiş)** uyarısı görülüyor. Dosya adı r2 ve ilk sayfa "SP 800-61 Revision 2" diyor; sürüm adında bir uyuşmazlık tespit edilmedi. Ancak güncellik ve içerik seçimi yeniden değerlendirilmelidir.
- Aynı başlığı çağrıştıran iki OWASP ASVS 5.0 dosyası var (`...5.0.0_en.pdf` ve `...5.0.0_en (1).pdf`). **Gerçek kopya oldukları kanıtlanmadı**; SHA256/içerik kontrolü yapılabilir.
- Resmî OWASP ASVS sitesi 4.0.3 ve 5.0.0 sürümlerini listeliyor; bu iki sürümün proje olarak gerçek olduğu doğrulanabiliyor. Yerel dosyaların aynı içerikte olduğu, lisansları ve indirme geçmişi ayrıca kontrol edilmedi.

## Sunumda okunabilecek kısa açıklama

> Siber güvenlik alanında 1.283 PDF topladık. Bunların 1.282'si açılabildi. Son Corpus'ta 731 kaynak belgeye ait 9.554 metin parçası bulunuyor. Dosya adı üzerinden 731 Corpus kaynağını yerel PDF envanteriyle eşleştirdik. İlk sayfa örnekleriyle NIST, OWASP ve ENISA gibi kaynak gruplarını ön sınıflandırdık. Belge bazında orijinal indirme URL'si, lisans ve içerik eşitliği doğrulaması ise tamamlanmadı.

**İlgili veri dosyası:** `KAYNAK_GRUPLARI_ON_SINIFLANDIRMA_731.csv` — her belge için grup, kanıt, dil ön tahmini, sayfa, Corpus chunk sayısı, URL/lisans statüsü ve inceleme uyarısı bulunur.
