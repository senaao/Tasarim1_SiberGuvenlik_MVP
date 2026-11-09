# Instruction Card — Siber Güvenlik Soru–Cevap Veri Seti (v1.0 adayı)

**Son güncelleme:** 9 Kasım 2026  
**Alan:** Teknik siber güvenlik  
**Dil:** Soruların ve cevapların önemli bölümü İngilizce; kaynak pasajlarda Türkçe ve İngilizce metinler bulunabilir. Kesin dil oranı henüz ölçülmedi.  
**Durum:** **Aday / kısmi kalite kontrol.** Veri setindeki tüm soru–cevapların bağımsız olarak onaylandığı iddia edilmez.  
**Güncel bölümleme:** Yakın tekrar bağlantıları dikkate alınarak oluşturulmuş, teknik kontrolden geçmiş **yeni split adayı**. **SFT dönüşümü de yapıldı; 12 ciddi hata adayı karantinaya ayrıldı.**

## 1. Amaç ve kapsam

Teknik siber güvenlik belgelerinden çıkarılmış pasajlara dayanan, `source_document` ve `source_text` alanları üzerinden izlenebilir soru–cevap örneklerini derlemek. Gelecekte instruction fine-tuning (SFT) veya soru–cevap değerlendirme çalışmalarında kullanılabilir. Bu veri setinin hazırlanmış olması, bir modelin eğitildiği veya model başarısının ölçüldüğü anlamına gelmez.

## 2. Veri miktarı ve güncel bölümleme

- **Orijinal / tam aday:** 3.075 soru–cevap kaydı. **12 ciddi hata adayı karantinaya ayrıldıktan sonraki geçici SFT adayı:** 3.063 kayıt. Karantina bir kalite kararıdır, orijinal kayıtlarda silme yapılmamıştır.
- **Farklı `source_document`:** 562.
- **Dosya biçimi:** JSONL (her satır bir JSON nesnesi).
- **Güncel yöntem:** Önce `source_document` bazında yapılan bölümlemede tespit edilen yakın tekrar bağlantıları, bağlı kaynak grupları hâlinde bir arada tutuldu. Corpus ve Instruction bölümleri birlikte yeniden eşleştirildi.
- **Eski bölümleme tohumu:** `20261109`. Bu değer ilk bölmeye aittir; yeni yeniden bölümlemenin bağımsız bir rastgele tohumu olarak sunulmaz.

| Bölüm | Orijinal aday kayıt sayısı | Farklı kaynak belge | Pay |
|---|---:|---:|---:|
| Train | 2.418 | 449 | %78,63 |
| Validation (`val`) | 359 | 60 | %11,67 |
| Test | 298 | 53 | %9,69 |
| **Toplam** | **3.075** | **562** | **%100** |

**Orijinal 3.075 kayıtlık ve Corpus ile uyumlu yeni bölümleme:**

```text
data/final/guvenli_split_aday/
├── instruction_dataset_3075_resplit_aday.jsonl
├── source_resplit_manifest.csv
├── instruction/
│   ├── train.jsonl
│   ├── val.jsonl
│   └── test.jsonl
└── corpus/
    ├── domain_corpus_train.jsonl
    ├── domain_corpus_val.jsonl
    └── domain_corpus_test.jsonl
```

**SFT dönüşümü ve kalite ön elemesi (ayrı çıktı dosyaları):**

| Bölüm | `messages` biçimine çevrilen | Karantinaya ayrılan | Geçici SFT adayı |
|---|---:|---:|---:|
| Train | 2.418 | 8 | 2.410 |
| Validation | 359 | 2 | 357 |
| Test | 298 | 2 | 296 |
| **Toplam** | **3.075** | **12** | **3.063** |

- SFT dönüşüm dosyaları: `data/final/sft_aday/train.jsonl`, `val.jsonl`, `test.jsonl`.
- Karantina sonrası geçici SFT çıktıları: `data/final/sft_kritik_12_ayrilmis_aday/train.jsonl`, `val.jsonl`, `test.jsonl`.
- Ayrı tutulan 12 kayıt: `data/final/sft_kritik_12_ayrilmis_aday/kritik_12_karantina.jsonl`.
- Teknik raporlar: `reports/instruction/SFT_DONUSUM_KONTROL_RAPORU.md`, `reports/instruction/KRITIK_12_AYIRMA_KONTROL_RAPORU.md`.

SFT dosyalarının şema dönüşümü 3.075/3.075 kayıt için başarılıdır. Karantina sonrası kalan 3.063 kayıt **tamamı insan tarafından doğrulanmış** kabul edilmez. Bu tablodaki 3.063 sayısı orijinal Instruction veri setinin değil, **geçici SFT adayının** büyüklüğüdür.

Önceki `data/final/instruction_v1/` bölmeleri (2.448 / 326 / 301) **eski sürüm** olarak korunmaktadır; yeni sonuçları raporlarken bu eski dosyalar kullanılmamalıdır. `data/final/instruction_dataset_3075_aday.jsonl` de yeniden bölünmeden önceki tam aday dosyadır. Yeni tam aday dosyası yukarıda gösterilmiştir. Corpus için de aynı `guvenli_split_aday` klasöründeki eşlenmiş bölüm dosyaları kullanılmalıdır.

## 3. Konu dağılımı

Yeniden bölümlemede soru içerikleri korunmuştur; bu nedenle toplam konu dağılımı değişmemiştir.

| Konu etiketi (`topic`) | Kayıt |
|---|---:|
| Authentication | 624 |
| Network Security | 343 |
| System Security | 323 |
| Penetration Testing | 316 |
| Incident Response | 315 |
| Malware | 246 |
| Web Security | 212 |
| Cloud Security | 188 |
| Cryptography | 165 |
| Mobile Security | 139 |
| DevSecOps | 129 |
| Digital Forensics | 75 |
| **Toplam** | **3.075** |

Bu etiketler **konu** dağılımını gösterir; tanım, açıklama, karşılaştırma, analiz ve akıl yürütme gibi **görev türleri** için ayrı ve doğrulanmış bir dağılım henüz bulunmamaktadır.

## 4. JSONL kaydı ve alanlar

| Alan | Açıklama |
|---|---|
| `id` | Tekil soru–cevap kimliği |
| `source_document` | Kaynak belge adı |
| `topic` | Teknik siber güvenlik konu etiketi |
| `source_text` | Soru ve cevabın dayandığı kaynak pasaj |
| `output` | `Question: ...` ve `Answer: ...` biçimindeki metin |
| `generation_model` | Kaydedilmişse üretimde kullanılan model |
| `review_status`, `model_review` | Otomatik/model tabanlı inceleme bilgisi |
| `review_explanation` | Varsa inceleme gerekçesi |
| `verified` | Bağımsız onay alanı; mevcut 3.075 kaydın tamamında `false` |
| `split` | Yeni bölümleme dosyalarında ilgili train/val/test ataması |

Diğer inceleme/metaveri alanları kayda göre değişebilir. `source_document` ve `source_text` alanlarının bulunması, özgün PDF bağlantısının ve lisansının doğrulandığı anlamına gelmez.

**SFT biçimi notu:** Orijinal Instruction JSONL dosyaları `output` alanını korur. Ayrıca `scripts/12_sft_formatina_donustur.py` kullanılarak 3.075 soru–cevabın tamamı ayrıştırılmış ve `messages` sohbet biçiminde `data/final/sft_aday/` dizinine yazılmıştır. `scripts/14_kritik_12_ayir.py` ile şüpheli 12 kayıt ayrı tutularak `data/final/sft_kritik_12_ayrilmis_aday/` içinde 3.063 kayıtlık **geçici** eğitim adayı oluşturulmuştur. Format dönüşümü cevapların doğruluğunu garanti etmez.

## 5. Üretim ve kalite kontrol

1. Siber güvenlik pasajlarından soru–cevap örnekleri üretildi. Örneklerin önemli bir bölümünde `generation_model` alanında `Qwen2.5-3B-Instruct` bulunur; bazı kayıtlarda bu alan boş veya eksik olabilir.
2. Kural kontrolleri ve model temelli kaynak uyumu taraması uygulandı. Mevcut 3.075 aday kaydın tamamında `review_status: MODEL_PASS` vardır. **Bu, insan/uzman onayı değildir.**
3. Öncelikli 28 kayıt incelemesinde **4 kayıt korundu, 11 kayıt düzeltildi, 13 kayıt çıkarıldı**. Çıkarılan 13 kayıt 3.075 adayın içinde değildir.
4. Ayrıca 60 kayıtlık daha eski bir kalite örneklemi değerlendirildi.
5. Yeni kontrolde **12 konu × 15 soru = 180 soru** (train 120, validation 36, test 24; 179 farklı kaynak) için model destekli ön inceleme hazırlandı. Bu çalışmada **12 ciddi hata adayı** tespit edilip ana adaydan silinmeden ayrı dosyaya alındı. **18 soru için düzeltme önerisi** üretildi; bunlar henüz ana veri setine uygulanmadı. Diğer konu/kapsam ve kaynak uyumu bulguları da ön değerlendirme niteliğindedir.
6. Orijinal 3.075 kayıt için `verified: false` durumu korunmaktadır. İnceleme **insan tarafından yapılmış nihai onay** anlamına gelmez. Bölme değişikliği anlamsal kaliteyi yükseltmiş veya düşürmüş olarak yorumlanmamalıdır; yalnızca verilerin hangi bölümde tutulduğunu değiştirir.

İlgili dosyalar: `reports/instruction/MANUEL_KALITE_KONTROL_RAPORU.md`, `reports/instruction/QA_KALITE_INCELEME_ORNEKLEMI_180.csv`, `reports/instruction/QA_MODEL_ON_INCELEME_180.csv`, `reports/instruction/QA_KALITE_ON_RAPORU_180.md`, `reports/instruction/QA_18_DUZELTME_ONERILERI.csv`, `reports/instruction/KRITIK_12_AYIRMA_KONTROL_RAPORU.md`, `reports/instruction/qa_28_oncelikli_inceleme_raporu.md` ve `reports/instruction/qa_13_teknik_kapsam_disi.jsonl`.

## 6. Yakın tekrar, yeniden bölümleme ve teknik doğrulama

Corpus üzerinde gerçekleştirilen yakın tekrar taramasında **63 olası benzer metin çifti** tespit edildi. İlk bölmede bunların **20 çifti farklı train/val/test bölümlerindeydi**. Benzer belgeler aynı kaynak gruplarında toplanarak Corpus ve Instruction birlikte yeniden bölümlendi.

- **Yeni bölümde tespit edilen 63 çift arasındaki çapraz-bölme eşleşmesi: 0.**
- **Yeniden atanan kaynak belge: 8.**
- Bu kaynaklarla ilişkili **199 Corpus parçası ve 64 soru** farklı bölümlere geçti.
- Toplam **9.554 Corpus parçası** ve **3.075 soru** korundu; kayıt kimlikleri ve soru–cevap içerikleri değişmedi.
- `10_validate_resplit.py` ile yapılan bağımsız teknik kontrolde ID bütünlüğü, eski/yeni içerik eşitliği (`split` hariç), tam ve bölünmüş dosya tutarlılığı, kaynak bazlı eşleşme ve tespit edilmiş çapraz-bölme çiftleri kontrolü **başarılı** sonuç verdi.

**Önemli sınırlama:** “0” sonucu yalnızca **tespit edilmiş 63 benzer çift** için geçerlidir; bütün olası tekrarların veya veri sızıntılarının yokluğunu garanti etmez. Bazı aday çiftler gerçek kopya değil, iki belgede ortak kullanılan teknik pasajlar olabilir.

**Teknik kanıtlar:**

- `reports/corpus/near_duplicate_pairs.csv`
- `reports/corpus/near_duplicate_63_degerlendirme.csv`
- `reports/corpus/NEAR_DUPLICATE_INCELEME_RAPORU.md`
- `reports/corpus/GUvenli_split_on_raporu.md`
- `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`
- `data/final/guvenli_split_aday/source_resplit_manifest.csv`

**Not:** `08_validate_datasets.py` eski bölümlemenin sabit kayıt sayılarını bekler. Yeni bölümleme için `10_validate_resplit.py` kullanılmalıdır.

## 7. Bilinen sınırlılıklar ve sonraki kontroller

- **Anlamsal doğruluk:** Soruların ve yanıtların tamamı bağımsız olarak doğrulanmadı; kaynak pasajına dayanmayan veya eksik yanıtlar bulunabilir.
- **Görev türleri:** Çeşitlilik ve görev tipi dağılımı henüz güvenilir biçimde ölçülmedi.
- **Dil dağılımı:** Türkçe/İngilizce oranları kesinleştirilmedi.
- **Kaynak ve lisans:** Kaynak URL'leri, telif/lisans bilgileri ve yeniden dağıtım izinleri kaynak bazında tamamlanmadı.
- **Yakın tekrar:** Farklı eşikler, anlamsal benzerlik ve farklı isimli kaynak kopyaları için ek denetim gerekebilir.
- **Veri üretimi:** Bazı üretim metaverisi alanları eksik; işlem hattının uçtan uca yeniden üretilebilirliği ayrıca sınanmalıdır.
- **SFT kalite kararı:** `messages` formatına dönüşüm tamamlandı; 3.063 kayıtlık geçici aday için insan doğrulaması ve önerilen düzeltmelerin değerlendirilmesi henüz tamamlanmadı.

## 8. Paylaşım ve etik kullanım

`source_text` alanları üçüncü taraf dokümanlardan alınmış pasajlar içerebilir. **Kaynakların telif/lisans ve yeniden paylaşım koşulları doğrulanmadan tam JSONL veri setleri herkese açık GitHub deposuna eklenmemelidir.** Kod, dokümantasyon, istatistikler ve paylaşım izni doğrulanmış küçük örnekler öncelikli olarak yayımlanmalıdır.

Siber güvenlik içerikleri yanlış veya kötü amaçlı kullanıma açık teknik açıklamalar içerebilir. Veri seti profesyonel güvenlik kararları için doğrulanmış bir referans olarak sunulmamalıdır.

## 9. İlgili proje belgeleri

- `README.md` — proje tanımı ve dizin yapısı.
- `DATASET_CARD.md` — Domain Corpus veri kartı.
- `reports/VERI_SETI_ISTATISTIK_RAPORU_GUNCEL.md` — güncel genel istatistikler.
- `reports/instruction/` — soru–cevap kalite incelemeleri.
- `reports/corpus/` — yakın tekrar ve yeniden bölme doğrulama raporları.
- `data/final/guvenli_split_aday/` — teknik kontrolden geçmiş **3.075 kayıtlık orijinal aday bölmeler**.
- `data/final/sft_kritik_12_ayrilmis_aday/` — **3.063 kayıtlık geçici SFT adayı** ve 12 kayıtlık karantina.

**Sürüm notu:** `v1.0 adayı` tam manuel olarak onaylanmış veya lisans denetimi bitmiş nihai sürüm anlamına gelmez.
