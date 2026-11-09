# Siber Güvenlik Domain Corpus ve Instruction Dataset

**Proje:** Tasarım 1 — Siber Güvenlik Veri Hazırlama Çalışması  
**Son güncelleme:** 9 Kasım 2026  
**Durum:** Teknik kontrolleri yapılmış v1.0 adayları; nihai içerik ve lisans doğrulaması tamamlanmadı.

## 1. Projenin Amacı

Bu çalışmada teknik siber güvenlik belgelerinden bir **Domain Corpus** (metin parçaları) ve kaynak pasajlarıyla ilişkilendirilmiş bir **Instruction Dataset** (soru-cevap kayıtları) hazırlanmıştır.

Hedef, sonraki aşamalarda bilgi erişimi, alan uyarlaması ve instruction fine-tuning gibi deneylere veri temeli oluşturmaktır.

**Bu aşamada bir dil modelinin eğitildiği, RAG uygulamasının tamamlandığı veya model performansının ölçüldüğü iddia edilmemektedir.**

## 2. Veri Setlerinin Güncel Durumu

| Veri seti | Toplam kayıt | Farklı kaynak belge | Train | Validation | Test |
|---|---:|---:|---:|---:|---:|
| Domain Corpus | 9.554 metin parçası | 731 | 7.643 | 1.059 | 852 |
| Instruction Dataset (orijinal aday) | 3.075 soru-cevap | 562 | 2.418 | 359 | 298 |
| SFT geçici kalite adayı | 3.063 soru-cevap | — | 2.410 | 357 | 296 |

**SFT kalite notu:** Orijinal 3.075 soru-cevap kaydı korunmuştur. Model destekli kalite ön incelemesinde ciddi hata adayı olarak işaretlenen 12 kayıt (train 8, validation 2, test 2) ayrı bir karantina dosyasına alınmış, 3.063 kayıtlık **geçici** SFT adayı oluşturulmuştur. Kalan kayıtların tümünün insan tarafından onaylandığı iddia edilmez.

**Corpus token sayımı:** `Qwen/Qwen3-4B-Base` tokenizer (`add_special_tokens=False`) ile 9.554 chunk üzerinde toplam **5.866.093 token** ölçülmüştür (ortalama 614, medyan 573, P95 948 token/chunk). Train / validation / test token sayıları: **4.731.185 / 622.499 / 512.409**. Ayrıntılar: `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt`.

Güncel veri bölmeleri `data/final/guvenli_split_aday/` klasöründedir.

Önceki bölmeler karşılaştırma ve geri dönüş amacıyla yerelde saklanmaktadır.

Yeni ayrımın kayıt sayıları, benzersiz kimlikleri, kaynak eşleşmeleri ve dosya bütünlüğü bağımsız teknik kontrolden geçmiştir.

Bu kontroller, içeriklerin tamamının bir insan veya alan uzmanı tarafından doğrulandığı anlamına gelmez. Instruction kayıtlarındaki `verified: false` durumu bu sınırlamayı yansıtır.

## 3. Kapsam ve Veri Biçimi

Veri setleri aşağıdaki teknik siber güvenlik konularını kapsamaktadır:

- Ağ ve sistem güvenliği
- Kimlik doğrulama
- Web ve mobil güvenlik
- Bulut güvenliği
- DevSecOps
- Zararlı yazılım analizi
- Kriptografi
- Dijital adli bilişim
- Olay müdahalesi
- Sızma testi

**Domain Corpus:** JSONL biçiminde `text`, kayıt kimliği, kaynak belge ve bölüm bilgileri içerir.

**Instruction Dataset:** JSONL biçiminde `id`, `source_document`, `topic`, `source_text`, `output` ve değerlendirme metaverilerini içerir.

Orijinal Instruction dosyasında soru ve cevap `output` alanında birlikte tutulur. Tüm **3.075 kayıt**, `scripts/12_sft_formatina_donustur.py` ile `messages` şemasına dönüştürülmüş ve `data/final/sft_aday/` altında train/val/test dosyaları oluşturulmuştur. Kalite ön incelemesinden sonra 12 kritik adayın ayrıldığı geçici küme `data/final/sft_kritik_12_ayrilmis_aday/` altındadır. Bu dönüşüm, yanıtların insan tarafından doğrulandığı anlamına gelmez.

`topic` alanı konu etiketidir. Açıklama, karşılaştırma veya akıl yürütme gibi görev türlerinin doğrulanmış dağılımı henüz çıkarılmamıştır.

Yerel `data/raw/` altında **1.283 PDF** envantere alınmıştır; bunlardan **731 farklı kaynak belge** mevcut Domain Corpus ile eşleşmektedir. Kaynak türleri arasında NIST, OWASP, ENISA yayın adayları, akademik makaleler, akademik slaytlar ve teknik kitaplar yer alır. Bu sınıflamalar ön incelemeye dayalıdır; her kaynak için özgün URL, lisans ve yeniden dağıtım izni doğrulanmış değildir. Envanter ve kaynak grubu adayları `reports/corpus/` altındadır.

## 4. Proje Klasör Yapısı

Aşağıdaki yapı yerel çalışma bilgisayarındaki temel dosyaları göstermektedir.

```text
Tasarim1_SiberGuvenlik_MVP/
├── README.md
├── DATASET_CARD.md
├── INSTRUCTION_CARD.md
├── requirements.txt
├── .gitignore
│
├── scripts/
│   ├── find_near_duplicates.py
│   ├── prepare_corpus.py
│   ├── 08_validate_datasets.py
│   ├── 09_resplit_near_duplicates.py
│   ├── 10_validate_resplit.py
│   ├── 11_pdf_kaynak_envanteri.py
│   ├── 12_sft_formatina_donustur.py
│   ├── 13_qa_kalite_orneklemi_hazirla.py
│   ├── 14_kritik_12_ayir.py
│   └── 15_vize_token_ve_once_sonra.py
│
├── reports/
│   ├── VERI_SETI_ISTATISTIK_RAPORU_GUNCEL.md
│   ├── corpus/
│   │   ├── CORPUS_KALITE_RAPORU.md
│   │   ├── NEAR_DUPLICATE_INCELEME_RAPORU.md
│   │   ├── GUvenli_split_on_raporu.md
│   │   ├── YENI_SPLIT_DOGRULAMA_RAPORU.txt
│   │   ├── pdf_kaynak_envanteri.csv
│   │   ├── KAYNAK_GRUPLARI_ON_SINIFLANDIRMA_731.csv
│   │   └── VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt
│   └── instruction/
│       ├── MANUEL_KALITE_KONTROL_RAPORU.md
│       ├── SFT_DONUSUM_KONTROL_RAPORU.md
│       ├── QA_KALITE_INCELEME_ORNEKLEMI_180.csv
│       ├── QA_MODEL_ON_INCELEME_180.csv
│       └── KRITIK_12_AYIRMA_KONTROL_RAPORU.md
│
├── data/
│   ├── raw/
│   ├── extracted/
│   ├── cleaned_v2/
│   └── final/
│       ├── domain_corpus_v1_aday.jsonl
│       ├── instruction_dataset_3075_aday.jsonl
│       ├── corpus_v1/
│       ├── instruction_v1/
│       └── guvenli_split_aday/
│           ├── domain_corpus_v1_resplit_aday.jsonl
│           ├── instruction_dataset_3075_resplit_aday.jsonl
│           ├── source_resplit_manifest.csv
│           ├── corpus/
│           └── instruction/
│       ├── sft_aday/
│       │   ├── train.jsonl
│       │   ├── val.jsonl
│       │   └── test.jsonl
│       └── sft_kritik_12_ayrilmis_aday/
│           ├── train.jsonl
│           ├── val.jsonl
│           ├── test.jsonl
│           └── kritik_12_karantina.jsonl
│
└── corpus_kontrol_paketi/
```

Bu ağaç temel dosyaları özetler. `scripts` ve `reports` altında başka dosyalar da bulunmaktadır.

**Önemli:** `data/` ve `corpus_kontrol_paketi/` klasörleri `.gitignore` ile GitHub dışında tutulmaktadır. GitHub deposunu klonlamak veri setlerini otomatik olarak indirmez.

## 5. Gerçekleştirilen Teknik Kontroller

### 5.1. JSONL ve Kimlik Kontrolü

Domain Corpus ve Instruction Dataset için:

- Toplam kayıt sayıları kontrol edildi.
- Train, validation ve test dosyaları doğrulandı.
- Benzersiz kayıt kimliklerinin korunduğu kontrol edildi.
- Corpus ve Instruction kaynak eşleşmeleri doğrulandı.

### 5.2. Veri Tekrarlarının İncelenmesi

Corpus ön kontrolünde:

- Birebir aynı metin kaydı bulunmadı.
- 246 metin parçası en az bir otomatik kalite uyarısı aldı.

TF-IDF tabanlı yakın tekrar incelemeleri gerçekleştirildi.

İlk taramada belirli eşiklerde 65 ve 16 aday çift raporlandı. Sonraki taramada ise 63 benzer metin çifti adayı belirlendi.

Bu sonuçlar farklı taramalara aittir ve aynı liste olarak değerlendirilmemelidir.

### 5.3. Veri Sızıntısı Riskinin Azaltılması

Sonraki taramada belirlenen 63 benzer metin çiftinin 20'si önceki train/validation/test bölmeleri arasında bulunuyordu.

Bu nedenle bağlantılı kaynak belgeleri aynı bölümde tutan yeni bir ayrım oluşturuldu.

Bu işlemde:

- 8 kaynak belgenin bölümü değiştirildi.
- 199 Domain Corpus parçası yeniden bölümlendirildi.
- 64 Instruction sorusu yeniden bölümlendirildi.
- Toplam 9.554 Corpus kaydı korundu.
- Toplam 3.075 soru-cevap kaydı korundu.
- Metin içerikleri değiştirilmedi.

**Tespit edilen 63 çift arasında bölmeler arası kalan benzerlik sayısı 0'a düşürüldü.**

Bu sonuç bütün olası veri sızıntılarının veya anlamsal tekrarların giderildiği anlamına gelmemektedir.

### 5.4. Bağımsız Teknik Doğrulama

Güncel veri ayrımı `scripts/10_validate_resplit.py` kullanılarak kontrol edilmiştir.

Kontrolde:

- Kayıt sayıları
- Benzersiz kimlikler
- Veri içeriklerinin korunması
- Bölme dosyalarının ana dosyalarla uyumu
- Kaynak bazlı bölümleme
- Corpus–Instruction eşleşmesi
- Tespit edilmiş benzer metin çiftlerinin bölmeler arası durumu

incelenmiştir.

**Sonuç: Bağımsız teknik kontrol başarılı.**

İlgili rapor:

`reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`

## 6. Instruction Dataset Kalite Değerlendirmesi

Instruction Dataset kayıtları kural tabanlı ve model destekli ön kontrollerden geçirilmiştir.

Buna ek olarak:

- Önceki aday aşamasında 60 soruluk kaynak-pasaj inceleme izi oluşturulmuştur.
- Ayrı bir turda 28 öncelikli kayıt incelenmiştir.
- Öncelikli 28 kaydın 4'ü korunmuştur.
- 11 kayıt kaynak pasajına göre yeniden yazılmıştır.
- 13 kayıt kapsam dışında bırakılmıştır.
- Sonraki aşamada 12 konuya dağıtılmış **180 soru-cevaplık** (train 120, validation 36, test 24; 179 farklı kaynak) kalite kontrol örneklemi oluşturulmuş ve **model destekli ön inceleme** yapılmıştır.
- Bu ön incelemede **12 ciddi hata adayı** karantinaya ayrılmıştır; **18 kayıt** için düzeltme önerileri hazırlanmıştır. Öneriler ana veri setine otomatik uygulanmamıştır.

Bu kontroller bağımsız uzman onayı anlamına gelmez. 180 örnek için insan değerlendirmesi tamamlanmış değildir.

Mevcut 3.075 sorunun tamamı kaynak metinler üzerinden tek tek bağımsız olarak doğrulanmamıştır.

Kalite kontrol sonuçları ve sınırlılıklar şu dosyada açıklanmaktadır:

`reports/instruction/MANUEL_KALITE_KONTROL_RAPORU.md`

Ek kanıtlar: `reports/instruction/QA_KALITE_ON_RAPORU_180.md`, `reports/instruction/QA_MODEL_ON_INCELEME_180.csv`, `reports/instruction/KRITIK_12_AYIRMA_KONTROL_RAPORU.md` ve `reports/instruction/QA_18_DUZELTME_ONERILERI.csv`.

### 6.1. Metin temizleme karşılaştırmaları

`data/extracted/` ve `data/cleaned_v2/` altındaki aynı kaynak adına ait dosyalardan **12 gerçek önce/sonra başlangıç kesiti** karşılaştırılmıştır. Bunlar satır satır hizalanmış diff değil, karşılaştırmalı örneklerdir. Rapor: `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt`.

## 7. Kurulum ve Çalıştırma

Proje Python ile geliştirilmiştir.

Gerekli kütüphaneler proje ana klasöründe şu komutla kurulabilir:

```powershell
python -m pip install -r requirements.txt
```

Yerel veri dosyaları mevcutsa güncel veri ayrımının teknik kontrolü şu komutla yapılabilir:

```powershell
python scripts/10_validate_resplit.py
```

Kontrol raporu:

`reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`

**Dikkat edilmesi gerekenler:**

- `08_validate_datasets.py` önceki bölümlemenin sayılarını kontrol eder.
- `09_resplit_near_duplicates.py` yeni aday bölümleme oluşturmak için kullanılmıştır.
- `10_validate_resplit.py` güncel aday bölümlemenin teknik kontrolü içindir.
- `12_sft_formatina_donustur.py` SFT `messages` dönüşümünü; `13_qa_kalite_orneklemi_hazirla.py` inceleme örneklemini; `14_kritik_12_ayir.py` kritik kayıtların geçici ayrımını üretir.
- `15_vize_token_ve_once_sonra.py` Qwen tokenizer ile Corpus token sayımı ve karşılaştırma raporu üretir; model ağırlıklarını indirmeyi gerektirmez.
- Mevcut çıktıların üzerine yanlışlıkla yazmamak için bölümleme kodları çalıştırılmadan önce dosya yolları ve hedef klasörler kontrol edilmelidir.

İlk PDF indirmesinden nihai JSONL dosyalarına kadar bütün işlem hattının başka bir bilgisayarda aynı sonuçları ürettiği henüz gösterilmemiştir.

GitHub deposunda veri dosyaları bulunmadığı için doğrulama kodları yalnızca depoyu klonlayarak çalıştırılamaz.

## 8. Henüz Tamamlanmamış Çalışmalar

Aşağıdaki işlemler tamamlanmış olarak değerlendirilmemektedir:

1. Kaynak URL'lerinin, erişim tarihlerinin, lisansların ve yeniden dağıtım izinlerinin doğrulanması.
2. Corpus ve Instruction Dataset için daha kapsamlı, kaynak temelli bağımsız manuel kalite kontrolü.
3. Otomatik işaretli 246 Corpus parçasının değerlendirilmesi.
4. Ek benzerlik kontrollerinin yapılması.
5. Dil ve görev türü dağılımlarının güvenilir biçimde ölçülmesi.
6. Veri hazırlama sürecinin uçtan uca yeniden üretilebilirliğinin sınanması.
7. Düzeltme adaylarının kaynaklarla ayrıca doğrulanması ve gerekirse nihai SFT adayına uygulanması.

## 9. Lisans, Etik ve Paylaşım

Kaynak belgelerin yeniden dağıtım izinleri henüz bütünüyle doğrulanmamıştır.

Bu nedenle ham PDF'ler, tam Domain Corpus ve kaynak pasajlarını içeren Instruction Dataset kayıtları herkese açık GitHub deposunda paylaşılmamalıdır.

GitHub deposunda öncelikle:

- Veri hazırlama ve kontrol kodları
- Veri kartları
- İstatistik raporları
- Kalite kontrol raporları
- Teknik doğrulama belgeleri

bulundurulmaktadır.

## 10. İlgili Belgeler

- `DATASET_CARD.md` — Domain Corpus'un yapısı, istatistikleri ve sınırlılıkları.
- `INSTRUCTION_CARD.md` — Instruction Dataset'in üretimi, bölümlenmesi ve kalite durumu.
- `reports/VERI_SETI_ISTATISTIK_RAPORU_GUNCEL.md` — Güncellenmiş Corpus, Instruction ve SFT istatistikleri.
- `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt` — Token sayımı ve 12 gerçek metin karşılaştırması.
- `reports/instruction/SFT_DONUSUM_KONTROL_RAPORU.md` — SFT `messages` dönüşümünün teknik kontrolü.
- `reports/corpus/` — Corpus kalite kontrolü ve yeniden bölümleme raporları.
- `reports/instruction/` — Instruction kalite inceleme raporları.

**Sürüm notu:** Bu çalışma, 9 Kasım 2026 itibarıyla teknik kontrolleri geçmiş bir veri seti adayıdır. Nihai kalite onayı, tüm lisansların doğrulandığı veya eğitilmiş bir modelin başarılı olduğu iddia edilmemektedir.