# Siber Güvenlik Veri Setleri — Güncel İstatistik Raporu

**İnceleme tarihi:** 9 Kasım 2026  
**Sürüm:** Kaynak-gruplu yeniden bölümleme sonrası **v1.0 adayı**  
**Durum:** Sayılar, ID bütünlüğü, kaynak eşleşmeleri ve tespit edilmiş 63 benzer çiftin bölmeleri bağımsız teknik kontrolden geçti. Tam manuel doğrulama, lisans denetimi ve tüm olası veri benzerliklerinin araştırılması tamamlanmadı.

## 1. Genel özet

| Ölçüt | Domain Corpus | Instruction QA |
|---|---:|---:|
| Kayıt | 9.554 metin parçası | 3.075 soru-cevap |
| Farklı kaynak belge adı | 731 | 562 |
| Bölümleme | Train/validation/test | Train/validation/test |
| Gerçek tokenizer tabanlı token sayımı | **5.866.093 token (Qwen3-4B-Base)** | Instruction için ayrı ölçüm yapılmadı |
| Tam bağımsız manuel kalite onayı | Tamamlanmadı | Tamamlanmadı |

**Kaynak havuzu:** `data/raw` altında **1.283 PDF** tarandı; bunların **731 farklı kaynak dosyası** mevcut Corpus ile ad bazında eşleştirildi. Bu sayı tüm PDF'lerin Corpus'a dahil edildiği anlamına gelmez. Ayrıntılar: `reports/corpus/PDF_KAYNAK_ESLESME_RAPORU.md`.

**Güncel ana dosyalar:**

- Corpus: `data/final/guvenli_split_aday/domain_corpus_v1_resplit_aday.jsonl`
- Instruction: `data/final/guvenli_split_aday/instruction_dataset_3075_resplit_aday.jsonl`
- Kaynak-bölme manifesti: `data/final/guvenli_split_aday/source_resplit_manifest.csv`

## 2. Domain Corpus istatistikleri

| İstatistik | Değer |
|---|---:|
| JSONL kaydı / chunk | 9.554 |
| Farklı `source_document` | 731 |
| Metin karakterleri toplamı | 27.440.087 |
| Boşlukla ayrılmış kelime toplamı | 3.988.017 |
| Medyan chunk uzunluğu | 2.910 karakter |
| Ortalama chunk uzunluğu | 2.872 karakter |
| En az bir otomatik kalite bayrağı içeren kayıt | 246 (%2,57) |
| Bayrağı olmayan kayıt | 9.308 (%97,43) |
| Otomatik ilk denetimde birebir tekrar | 0 |
| İlk denetim: cosine ≥ 0,83 yakın tekrar adayı | 65 çift |
| İlk denetim: cosine ≥ 0,92 yakın tekrar adayı | 16 çift |
| Sonraki karşılaştırma (`near_duplicate_pairs.csv`) | 63 aday çift |

**Not:** 65 ve 16 eşik bazlı sonuç ile 63 çiftlik sonraki tarama, farklı tarama/filtreleme sonuçlarıdır. Birbirinin aynısı sayılmamalıdır.

### 2.1 Güncel train/validation/test dağılımı

| Bölüm | Metin parçası | Farklı kaynak belge | Parça oranı |
|---|---:|---:|---:|
| Train | 7.643 | 587 | %80,00 |
| Validation (`val`) | 1.059 | 77 | %11,08 |
| Test | 852 | 67 | %8,92 |
| **Toplam** | **9.554** | **731** | **%100** |

**Klasör:** `data/final/guvenli_split_aday/corpus/`

### 2.2 Qwen tokenizer ile token istatistikleri

9.554 Corpus kaydının `text` alanı `Qwen/Qwen3-4B-Base` tokenizer ile, `add_special_tokens=False` parametresi kullanılarak ölçüldü. Bu sayılar bir model eğitimi veya model ağırlıklarının indirilmesi anlamına gelmez.

| Ölçüm | Sonuç |
|---|---:|
| Toplam token | **5.866.093** |
| Ortalama token / chunk | 614 |
| Medyan token / chunk | 573 |
| Minimum / maksimum token / chunk | 55 / 10.712 |
| Chunk token P95 | 948 |
| Tokenlanan kaynak belge | 731 |
| Train token | 4.731.185 |
| Validation token | 622.499 |
| Test token | 512.409 |

**Kanıt:** `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt` ve `scripts/15_vize_token_ve_once_sonra.py`.

### 2.3 Metin çıkarma ve temizleme karşılaştırmaları

12 kaynak belge için `data/extracted` ve `data/cleaned_v2` içindeki başlangıç metin kesitleri karşılaştırıldı. Bu örnekler belge bazında eşleşir, ancak satır/sözcük seviyesinde hizalanmış fark analizi değildir. Ham metinlerdeki bazı ön sayfa ve yazar/kurum bilgileri temizleme sırasında değişmiş veya çıkarılmış olabilir; bütün değişikliklerin doğru olduğu ayrıca insan tarafından doğrulanmadı.

**Kanıt:** `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt` (12 karşılaştırma).

### 2.4 Otomatik kalite işaretleri (ilk Corpus taraması)

| Bayrak | İşaretli chunk |
|---|---:|
| `toc_or_page_leader` | 158 |
| `low_alphabetic_ratio` | 130 |
| `bibliography_possible` | 14 |
| `near_duplicate_candidate` | 32 |
| `short_chunk` | 8 |
| `page_artifact_possible` | 7 |
| `unicode_replacement` | 2 |

*Bir kayıt birden fazla bayrak alabilir. Bayrak taşımaması manuel olarak doğrulandığı anlamına gelmez.*

## 3. Instruction QA istatistikleri

| İstatistik | Değer |
|---|---:|
| Soru-cevap kaydı | 3.075 |
| Tekil `id` | 3.075 |
| Farklı `source_document` | 562 |
| Farklı `topic` etiketi | 12 |
| `Question:` ve `Answer:` bölümleri mevcut kayıt | 3.075 |
| `verified: false` kayıt (orijinal aday) | 3.075 |
| SFT `messages` biçimine dönüştürülen kayıt | 3.075 |
| Ciddi hata adayı olarak ayrı tutulan kayıt | 12 |
| Geçici SFT kümesinde kalan kayıt | 3.063 |

### 3.1 Güncel train/validation/test dağılımı

| Bölüm | Soru-cevap kaydı | Farklı kaynak belge | Kayıt oranı |
|---|---:|---:|---:|
| Train | 2.418 | 449 | %78,63 |
| Validation (`val`) | 359 | 60 | %11,67 |
| Test | 298 | 53 | %9,69 |
| **Toplam** | **3.075** | **562** | **%100** |

**Klasör:** `data/final/guvenli_split_aday/instruction/`

### 3.2 Güncel geçici SFT biçimi

3.075 orijinal soru-cevap, `scripts/12_sft_formatina_donustur.py` ile `messages` tabanlı SFT JSONL biçimine dönüştürüldü. Ardından **12 ciddi hata adayı**, orijinal dosyalara dokunulmadan ayrı tutuldu.

| Bölüm | Geçici SFT adayı | Ayrı tutulan ciddi hata adayı |
|---|---:|---:|
| Train | 2.410 | 8 |
| Validation | 357 | 2 |
| Test | 296 | 2 |
| **Toplam** | **3.063** | **12** |

**Geçici SFT klasörü:** `data/final/sft_kritik_12_ayrilmis_aday/`. Bu verilerin tümünün insan tarafından onaylandığı iddia edilmez; asıl 3.075 kayıt korunmuştur.

**Dönüşüm raporları:** `reports/instruction/SFT_DONUSUM_KONTROL_RAPORU.md` ve `reports/instruction/KRITIK_12_AYIRMA_KONTROL_RAPORU.md`.

### 3.3 Güncel konu dağılımı — orijinal 3.075 kayıt üzerinden

| Konu | Train | Val | Test | Toplam | Pay |
|---|---:|---:|---:|---:|---:|
| Authentication | 506 | 73 | 45 | 624 | %20,29 |
| Network Security | 266 | 34 | 43 | 343 | %11,15 |
| System Security | 238 | 39 | 46 | 323 | %10,50 |
| Penetration Testing | 258 | 23 | 35 | 316 | %10,28 |
| Incident Response | 228 | 53 | 34 | 315 | %10,24 |
| Malware | 201 | 26 | 19 | 246 | %8,00 |
| Web Security | 173 | 20 | 19 | 212 | %6,89 |
| Cloud Security | 139 | 31 | 18 | 188 | %6,11 |
| Cryptography | 127 | 22 | 16 | 165 | %5,37 |
| Mobile Security | 116 | 14 | 9 | 139 | %4,52 |
| DevSecOps | 100 | 18 | 11 | 129 | %4,20 |
| Digital Forensics | 66 | 6 | 3 | 75 | %2,44 |
| **Toplam** | **2.418** | **359** | **298** | **3.075** | **%100** |

**Dikkat:** `topic` bir **konu etiketi**dir; açıklama, karşılaştırma, akıl yürütme vb. *görev türü dağılımı* henüz güvenilir şekilde etiketlenmedi.

## 4. Yeniden bölümleme ve veri sızıntısı kontrolleri

Önceki kaynak adı bazlı bölümlemede, farklı adlarla kaydedilmiş ancak birbirine benzeyen belgeler arasında **20 çapraz-bölme benzer metin çifti** tespit edildi. Tespit edilen toplam 63 yakın tekrar aday çifti için kaynaklar bağlantılı gruplar hâline getirilerek yeniden bölümlendi.

| Ölçüm | Sonuç |
|---|---:|
| Tespit edilmiş yakın tekrar aday çifti | 63 |
| Eski ayrımda farklı bölmelerde bulunan çift | 20 |
| Yeni ayrımda farklı bölmelerde bulunan çift | **0** |
| Bölümü değişen kaynak belge | 8 |
| Başka bölüme geçen Corpus parçası | 199 |
| Başka bölüme geçen Instruction sorusu | 64 |
| Kayıp kayıt | 0 |

**Bağımsız teknik kontrol başarılı:** Her iki veri setinin ID'leri korundu, içerikleri `split` dışında değişmedi, split dosyaları ana dosyalarla eşleşti, aynı kaynak belge tek bölmede kaldı ve Instruction kaynakları ilgili Corpus bölmeleriyle eşleşti.

**Sınır:** 63 aday çiftin tamamının tek bölmede bulunması, keşfedilmemiş benzerliklerin veya tüm değerlendirme sızıntılarının olmadığını **kanıtlamaz**. Ayrıca 562 Instruction kaynağı Corpus içinde bulunur; geri kalan 169 Corpus kaynağından bu Instruction setinde soru üretilmemiştir.

İlgili kanıtlar:

- `reports/corpus/near_duplicate_pairs.csv`
- `reports/corpus/near_duplicate_63_degerlendirme.csv`
- `reports/corpus/GUvenli_split_on_raporu.md`
- `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`

## 5. Kalite ön incelemesi ve manuel doğrulama durumu

- Corpus'ta 246 metin parçası otomatik kalite uyarısı aldı. Tamamının manuel incelendiği söylenemez.
- Corpus için 100–200 örneklik temsilî manuel kontrol henüz tamamlanmadı.
- Önceki çalışmalarda 60 örnek için inceleme yapıldı; ayrıca 28 öncelikli kayıt değerlendirildi (4 korundu, 11 düzeltildi, 13 çıkarıldı). Bu değerler önceki aşamanın bulgularıdır.
- Güncel adayın içinden **12 konu × 15 soru = 180 kayıt** (179 farklı kaynak belge) kalite kontrol örneklemine alındı. Bu 180 soru **model destekli ön incelemeden** geçti; insan tarafından tamamı onaylanmış değildir.
- Ön incelemede **12 ciddi hata/eleme adayı, 18 düzeltme adayı, 25 alan dışı, 33 konu etiketi adayı, 36 ek kontrol gerektiren ve 56 belirgin hata bulunmayan** kayıt belirlendi. Bunlar birbirini dışlayan ilk sınıflandırma gruplarıdır; nihai kalite kararları değildir.
- 12 ciddi aday geçici SFT kümesinden karantinaya ayrıldı; **18 düzeltme için öneri belgesi** oluşturuldu fakat bu öneriler ana veri setine uygulanmadı. 33 etiket önerisi ve diğer kalite kararları da nihai olarak uygulanmış değildir.
- İlgili dosyalar: `reports/instruction/QA_KALITE_ON_RAPORU_180.md`, `reports/instruction/QA_MODEL_ON_INCELEME_180.csv`, `reports/instruction/QA_18_DUZELTME_ONERILERI.csv`.
- Mevcut 3.075 Instruction kaydının `verified` alanı `false`; modelin `MODEL_PASS` etiketi bağımsız uzman doğrulaması değildir.
- Kaynak URL'leri, lisanslar, yeniden dağıtım izinleri ve dil yüzdeleri tam doğrulanmadı. **Corpus token sayımı tamamlandı**; Instruction için ayrı token sayımı henüz yapılmadı.
- Bu nedenle tam Corpus/Instruction JSONL dosyaları lisans doğrulanmadan herkese açık GitHub'a konulmamalıdır.

## 6. Ölçüm yöntemi

- JSONL kayıtları satır satır okundu; `source_document`, `topic` ve `split` değerleri üzerinden sayımlar yapıldı.
- Corpus karakter sayısı `len(text)`; kelime sayısı `text.split()` ile ölçüldü. Tokenlar ise ayrıca `Qwen/Qwen3-4B-Base` tokenizer ile `add_special_tokens=False` kullanılarak hesaplandı.
- Konu tablosundaki split sayıları **yeniden bölümleme sonrasındaki JSONL adayından** hesaplandı. Eski splitteki konu kırılımları kullanılmadı.
- Bağımsız teknik doğrulama `scripts/10_validate_resplit.py` ile yapıldı.
- Yakın tekrar sınırlaması `scripts/find_near_duplicates.py` tarafından oluşturulan 63 aday çift ve `scripts/09_resplit_near_duplicates.py` tarafından yapılan kaynak-gruplu yeniden bölümleme temelindedir.

## 7. Eski sürümlerle karıştırmayın

| Veri | Eski train/val/test | Güncel train/val/test |
|---|---|---|
| Corpus | 7.702 / 980 / 872 | **7.643 / 1.059 / 852** |
| Instruction | 2.448 / 326 / 301 | **2.418 / 359 / 298** |

- Önceki Corpus dosyası: `data/final/domain_corpus_v1_aday.jsonl`
- Önceki Instruction dosyası: `data/final/instruction_dataset_3075_aday.jsonl`
- Eski bölme yedekleri: `data/final/corpus_v1/` ve `data/final/instruction_v1/`
- Güncel aday: **`data/final/guvenli_split_aday/`**
- Eski veri kartındaki 1.210 doküman / 127.555.685 karakter / 19.194.321 token bilgileri önceki derleme aşamasına aittir; güncel 9.554 parçalık adayın metrikleri yerine kullanılmaz.

**İlgili belgeler:** `README.md`, `DATASET_CARD.md`, `INSTRUCTION_CARD.md`, `reports/corpus/VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt` ve `reports/corpus/` ile `reports/instruction/` altındaki kalite kanıtları.
