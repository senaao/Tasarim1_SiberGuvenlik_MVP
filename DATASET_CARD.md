# DATASET_CARD — Siber Güvenlik Domain Corpus

**Sürüm:** `v1_aday` (yeniden bölümlendirilmiş teknik doğrulama adayı; nihai v1.0 değil)  
**Son teknik inceleme:** 9 Kasım 2026  
**Dil:** Kaynak belgelerin dili karışıktır; dil etiketleri sistematik olarak doğrulanmamıştır.  
**Alan:** Siber güvenlik  
**Format:** UTF-8 JSONL; her satır bir metin parçası (chunk)  
**Güncel temel dosya:** `data/final/guvenli_split_aday/domain_corpus_v1_resplit_aday.jsonl`  
**Önceki adayın yedeği:** `data/final/domain_corpus_v1_aday.jsonl`

## 1. Özet ve amaç

Bu veri seti siber güvenliğin teknik alanlarına ait PDF/dokümanlardan çıkarılmış ve parçalara ayrılmış metinleri içerir. Domain Corpus; ileride **continued pretraining (CPT)** yoluyla alan uyarlaması, bilgi erişimi ve model değerlendirme çalışmalarında kullanılmak üzere hazırlanmıştır. Bu aşamada **model eğitimi yapılmış olduğu iddia edilmez**.

## 2. Kapsam ve kaynaklar

İçerik; ağ ve sistem güvenliği, kimlik doğrulama, kriptografi, web/mobil güvenliği, zararlı yazılım analizi, dijital adli bilişim, bulut güvenliği, DevSecOps, olay müdahalesi ve benzeri teknik konuları kapsar.

- **731 farklı kaynak belge** (`source_document` alanına göre).
- **9.554 metin parçası**.
- Önceki veri kartında **NIST SP 800**, **CISA**, **ENISA**, **OWASP** ve diğer açık teknik kaynaklar kullanıldığı belirtilmiştir. Bunlar önceki aşamaya ait kaynak beyanıdır; mevcut 731 kaynak belgenin her biri için kurum, indirme URL'si ve lisans eşleştirmesi henüz doğrulanmamıştır.
- Kaynakların yerel belge adları ve önceki işlem yolları kayıtlarda bulunur; ancak her belge için doğrulanmış kaynak URL'si, erişim tarihi ve lisans bilgisi henüz yoktur.
- Kaynak envanteri: `reports/corpus/source_inventory.csv`. Buradaki eksik alanlar tamamlanmış kaynakça olarak sunulmamalıdır.

## 3. Veri yapısı

`domain_corpus_v1_resplit_aday.jsonl` dosyasında başlıca alanlar:

| Alan | Açıklama |
|---|---|
| `id` | Metin parçasının benzersiz kimliği |
| `document_id` | Kaynak belgeye bağlanan kimlik |
| `source_document` | Kaynak belgenin dosya adı |
| `source_path_original` | Ön işleme aşamasındaki eski yerel kaynak yolu; taşınabilir indirme adresi değildir |
| `text` | Temizlenmiş olarak devralınan metin parçası |
| `char_count` | Metnin karakter uzunluğu |
| `word_count` | Boşluğa göre yaklaşık kelime sayısı; token sayısı değildir |
| `split` | `train`, `val` veya `test` |
| `quality_flags` | Otomatik kontrollerin uyarıları; boş liste onay anlamına gelmez |
| `manual_reviewed` | Manuel inceleme tamamlanma durumu |

JSONL biçiminde her satır ayrı bir JSON nesnesidir. Kaynak metnin gerçek PDF'deki biçimi ve tüm parça sınırları manuel olarak doğrulanmamıştır.

## 4. Boyut ve güncel bölümleme

| Küme | Farklı kaynak belge | Metin parçası | Pay (parça) |
|---|---:|---:|---:|
| Train | 587 | 7.643 | %80,00 |
| Validation | 77 | 1.059 | %11,08 |
| Test | 67 | 852 | %8,92 |
| **Toplam** | **731** | **9.554** | **%100** |

- Toplam karakter sayısı: **27.440.087**.
- Boşlukla ayrılmış kelime sayısı: **3.988.017**.
- Parça başına medyan karakter: **2.910** (önceki ölçüm; metinler aynı kaldı).
**Token istatistikleri:** Qwen/Qwen3-4B-Base tokenizer kullanılarak 9.554 Corpus parçasında toplam 5.866.093 token ölçülmüştür. Parça başına ortalama 614, medyan 573 ve P95 değeri 948 tokendır. Train kümesi 4.731.185, validation 622.499 ve test 512.409 token içermektedir.

İlk bölümleme kaynak belge adlarına göre yapılmıştı. Ardından farklı adlarla saklanan benzer belgelerin bazı pasajlarının farklı train/val/test bölmelerinde kaldığı görüldü.

**Tespit edilen 63 yakın tekrar adayı çifti** üzerinden bağlantılı kaynak grupları birlikte tutularak yeni bölümleme üretildi.

Bu işlem sonucunda:

- **8 kaynak belgenin** bölümü değiştirildi.
- **199 Corpus parçası** farklı bölümlere taşındı.
- **64 Instruction sorusu** farklı bölümlere taşındı.
- Hiçbir kayıt silinmedi.
- Metin içerikleri değiştirilmedi.

Güncel Corpus bölmeleri ile 3.075 soruluk Instruction Dataset'in güncel bölmeleri beraber oluşturuldu ve bağımsız teknik kontrolde eşleşti.

**Tespit edilen 63 benzer çift arasında bölmeler arası kalan çift: 0.**

Bu sonuç yalnızca tespit edilmiş çiftleri kapsar; olası tüm veri sızıntılarının giderildiğini kanıtlamaz.

### Güncel kullanılacak dosyalar

```text
data/final/guvenli_split_aday/
├── domain_corpus_v1_resplit_aday.jsonl
├── instruction_dataset_3075_resplit_aday.jsonl
├── source_resplit_manifest.csv
├── corpus/
│   ├── domain_corpus_train.jsonl
│   ├── domain_corpus_val.jsonl
│   └── domain_corpus_test.jsonl
└── instruction/
    ├── train.jsonl
    ├── val.jsonl
    └── test.jsonl
```

**Eski bölmeler yedek olarak korunur:**

- `data/final/corpus_v1/` — 7.702 / 980 / 872
- `data/final/instruction_v1/` — 2.448 / 326 / 301

Önceki `domain_corpus_v1_aday.jsonl` dosyası da eski split alanlarını içerir. Güncel raporlama ve analizde eski bölme dosyaları yeni adayla karıştırılmamalıdır.

## 5. Önceki veri kartındaki sayılar ve sürüm farkı

**6 Kasım 2026 tarihli eski DATASET_CARD.md**, farklı bir derleme ve ön işleme aşamasını anlatıyordu.

Oradaki ölçümler kaybolmasın diye aşağıda korunmuştur. Ancak bu ölçümlerin 9 Kasım 2026 tarihli güncel Corpus sürümüyle aynı veri sürümünü veya aynı ölçüm yöntemini temsil ettiği doğrulanmamıştır.

| Eski kartta bildirilen metrik | Değer | Mevcut dosyayla ilişkisi |
|---|---:|---|
| İşlenen doküman sayısı | 1.210 | Önceki derleme aşamasına ait; güncel dosyada 731 farklı kaynak belge adı var |
| Toplam karakter | 127.555.685 | Eski derleme aşaması; güncel adayda 27.440.087 karakter var |
| Toplam token | 19.194.321 | Önceki karttaki sayı; tokenizer adı ve yöntem doğrulanmadığından güncel adayın token sayısı olarak kullanılamaz |
| Ortalama token/doküman | 15.863 | Önceki kartta bildirilen değer; güncel adayın parça başına token ölçümü değildir |
| Tekrar eleme | MD5 ile 21 tekrar çıkarıldığı bildirildi | Önceki işlem aşamasının beyanı; güncel adayda otomatik denetimde kalan birebir tekrar sayısı 0 |
| PDF metin çıkarımı | PyMuPDF | Önceki işlemde kullanıldığı belirtilmiş; kaynak PDF'ler karşılaştırılarak bağımsız doğrulama yapılmamış |

**Önemli ayrım:** İşlenen doküman, farklı kaynak belge ve metin parçası (chunk) aynı kavramlar değildir.

Eski 19.194.321 token değeri ile güncel 3.988.017 kelime sayısı da aynı ölçüm birimlerini temsil etmez.

## 6. Oluşturulma ve ön işleme

Projedeki mevcut veri akışı genel olarak şu adımları içerir:

1. Teknik belgelerin temin edilmesi ve PDF metinlerinin çıkarılması.
2. Metin temizleme ve parçalara ayırma (chunking).
3. JSONL kayıtlarını standartlaştırma ve belge kimliği oluşturma.
4. Birebir tekrar ve TF-IDF temelli yakın tekrar adaylarını tarama.
5. İçerik kalite işaretlerini üretme, kaynak bazlı split oluşturma ve tespit edilen yakın tekrar bağlantılarını aynı bölmede tutacak yeniden bölümleme.

`corpus_kontrol_paketi/scripts/` dizinindeki betikler ilk Corpus denetimi ve hazırlığı içindir.

Güncel aday bölümleme:

`scripts/09_resplit_near_duplicates.py`

Bağımsız teknik denetim:

`scripts/10_validate_resplit.py`

Projedeki önceki `scripts/` betiklerinin tüm ilk aşamaları uçtan uca aynı sonuçla ürettiği henüz teyit edilmemiştir.

Metin temizleme sürecini göstermek için 12 farklı kaynak belgenin extracted (ham çıkarılmış metin) ve cleaned_v2 (temizlenmiş metin) sürümleri karşılaştırılmıştır. Karşılaştırmalar reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt dosyasında belgelenmiştir.
## 7. Kalite kontrol ve bulgular

9 Kasım 2026 itibarıyla otomatik inceleme:

| Ölçüt | Sonuç |
|---|---:|
| Birebir aynı `text` kayıtları | 0 |
| En az bir uyarı alan parça | 246 |
| Uyarı almayan parça | 9.308 |
| TF-IDF cosine ≥ 0,83 aday çift | 65 |
| TF-IDF cosine ≥ 0,92 aday çift | 16 |

Bu tablodaki 65 ve 16 yakın tekrar çiftleri ilk Corpus ön kontrolünün farklı eşiklerde raporladığı adaylardır.

Daha sonra kullanılan `find_near_duplicates.py` betiğinin oluşturduğu `near_duplicate_pairs.csv` dosyasında **63 aday çift** vardır.

Farklı tarama ve filtreleme sonuçları birbiriyle aynı listeymiş gibi değerlendirilmemelidir.

Uyarılar şu konuları içerebilir:

- İçindekiler dizini
- Düşük harf oranı
- Kaynakça
- Olası yakın tekrar
- Kısa metin parçası
- Sayfa artığı
- Bozuk Unicode karakterleri

Bir kayıt birden fazla uyarı alabilir. Bu sayılar, uyarılı kayıtların yanlış olduğunu veya diğerlerinin eksiksiz doğru olduğunu göstermez.

Yakın tekrar adayları otomatik olarak silinmemiştir. Yeniden bölümleme yalnızca ilişkili kaynakları aynı bölmede tutmayı hedefler.

Corpus için hedeflenen **100–200 rastgele veya temsilî manuel kontrol henüz tamamlanmamıştır**.

İnceleme dosyaları:

- `corpus_kontrol_paketi/output/review_manifest.csv`
- `corpus_kontrol_paketi/output/domain_corpus_inceleme_gerekenler.jsonl`
- `reports/corpus/CORPUS_KALITE_RAPORU.md`

### Yeni bölümlemenin bağımsız teknik doğrulaması

Aşağıdaki kontroller başarıyla tamamlanmıştır:

- 9.554 Corpus kaydı korundu.
- Tüm kayıt ID'leri korundu.
- Bölme dosyaları tam dosyayla eşleşti.
- Corpus ve Instruction kaynak eşleşmeleri doğrulandı.
- Tespit edilmiş 63 benzer çiftten çapraz bölmede kalan çift sayısı 0 olarak ölçüldü.

**Sonuç: Bağımsız teknik kontrol başarılı.**

İlgili raporlar:

- `reports/corpus/NEAR_DUPLICATE_INCELEME_RAPORU.md`
- `reports/corpus/near_duplicate_63_degerlendirme.csv`
- `reports/corpus/GUvenli_split_on_raporu.md`
- `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`

## 8. Olası kullanım alanları

- Siber güvenlik metinlerinde terminoloji ve bağlam analizi.
- Alan uyarlama ve continued pretraining denemeleri için ön çalışma.
- Bilgi erişimi ve belge arama deneyleri.
- Kaynağa dayalı Instruction Dataset ile belge düzeyinde eşleştirme.
- Eğitim ve değerlendirme veri seti hazırlama çalışmaları.

**Kullanılmaması gereken durumlar:**

Kaynak doğruluğu, güncellik ve lisansları kontrol edilmeden üretim ortamında güvenlik kararları vermek; metinleri kesin doğru kaynak kabul etmek; gözden geçirilmemiş splitleri tamamen sızıntısız varsaymak; doğrulanmamış telif haklarıyla herkese açık tam veri dağıtmak.

## 9. Lisans, etik ve paylaşım

- Kullanılan kaynakların tekil lisans ve yeniden dağıtım izinleri henüz doğrulanmamıştır.
- Doğrulanmış lisans kaydı: **0**.
- Kamuya açık erişim, otomatik olarak yeniden dağıtma izni sağlamaz.
- Lisans taraması bitene kadar ham PDF'ler ve kaynak metinlerin tamamı herkese açık GitHub deposuna konulmamalıdır.
- Güvenlik zafiyeti ve saldırı teknikleriyle ilgili metinler eğitim ve araştırma bağlamında ele alınmalıdır.
- Bazı kaynaklarda tarihi veya bağlamdan kopmuş teknik bilgiler bulunabilir.

## 10. Bilinen sınırlılıklar ve tamamlanması gerekenler

- Kaynak URL, erişim tarihi, lisans ve yayın bilgilerini doğrulamak.
- Corpus için manuel kalite örneklemesini tamamlamak ve kararları kayıt altına almak.
- İşaretlenmiş 246 parçayı değerlendirmek.
- İlk taramadaki 65 yakın tekrar adayı ile sonraki taramadaki 63 aday çiftin yöntem farklarını dikkate almak.
- Dil ve alt konu etiketleriyle kaynak kapsama dağılımını doğrulamak.
- Ham PDF'den son JSONL dosyasına kadar tekrarlanabilir veri hazırlama sürecini belgelendirmek.
- Nihai değerlendirmeden sonra sürümü `v1.0` olarak ilan etmek.
- `README.md` ve genel istatistik raporundaki eski train/val/test sayılarını güncellemek.

## 11. İlgili dosyalar

- **Güncel ana veri:** `data/final/guvenli_split_aday/domain_corpus_v1_resplit_aday.jsonl`
- **Güncel Corpus bölmeleri:** `data/final/guvenli_split_aday/corpus/`
- **Eski veri yedeği:** `data/final/domain_corpus_v1_aday.jsonl`
- **İnceleme paketi:** `corpus_kontrol_paketi/`
- **Corpus kalite raporu:** `reports/corpus/CORPUS_KALITE_RAPORU.md`
- **Güncel bölümleme raporu:** `reports/corpus/GUvenli_split_on_raporu.md`
- **Bağımsız doğrulama raporu:** `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`
- **Instruction Dataset veri kartı:** `INSTRUCTION_CARD.md`
- **Proje genel özeti:** `README.md`

**Sürüm notu:** Bu kart 9 Kasım 2026 tarihli otomatik kontrol raporlarına dayanır. Güncel bölümleme ve kayıt sayıları bağımsız teknik doğrulamayla uyumludur. Ancak manuel kalite denetimi, kaynak lisansları ve tüm olası veri benzerlikleri henüz tam olarak doğrulanmamıştır.