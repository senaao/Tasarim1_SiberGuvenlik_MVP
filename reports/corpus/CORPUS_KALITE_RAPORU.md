# Siber Güvenlik Domain Corpus — Kalite ve Teknik Kontrol Raporu

**Son güncelleme:** 9 Kasım 2026  
**Veri seti durumu:** `v1.0 adayı` — teknik kontrol yapılmıştır; nihai manuel kalite ve lisans doğrulaması tamamlanmamıştır.  
**İlk otomatik denetimin girdisi:** `domain_corpus_taslak_v2.jsonl`  
**Güncel bölümleme adayı:** `data/final/guvenli_split_aday/domain_corpus_v1_resplit_aday.jsonl`

Bu rapor, **ilk Corpus otomatik denetiminin sonuçlarını** ve sonradan gerçekleştirilen **yakın tekrar incelemesi / yeniden bölümleme** çalışmasını birbirinden ayırır. İlk denetim sonuçları geriye dönük değiştirilmemiştir. Otomatik kontrollerin başarılı olması, tüm metinlerin doğru, temiz veya uzman tarafından onaylanmış olduğu anlamına gelmez.

## 1. Corpus boyutu ve ilk otomatik denetim

| Ölçüt | İlk denetimde kaydedilen sonuç |
|---|---:|
| Geçerli JSONL satırı / metin parçası | 9.554 |
| Farklı `source_document` | 731 |
| Benzersiz `id` | 9.554 |
| Birebir aynı `text` (SHA-256) | 0 |
| Toplam karakter | 27.440.087 |
| Boşlukla ayrılmış toplam kelime | 3.988.017 |
| Metin parçası medyan uzunluğu | 2.910 karakter |
| En az bir otomatik kalite uyarısı alan parça | 246 |
| Uyarı almayan parça | 9.308 |
| İlk TF-IDF taramasında benzerlik ≥ 0,83 olan çift | 65 |
| İlk TF-IDF taramasında benzerlik ≥ 0,92 olan çift | 16 |

**Ölçümün kapsamı:** Bu değerler ilk kontrol paketinin ürettiği sayısal rapordan alınmıştır. Sonraki yeniden bölümlemede **metin içerikleri ve kayıt kimlikleri korunmuştur**; yalnızca bölme atamaları değişmiştir. `3.988.017` değeri kelime sayısıdır, tokenizer ile hesaplanmış token sayısı değildir.

## 2. Otomatik kalite uyarıları

| Kalite işareti | Parça sayısı | İşaretin anlamı |
|---|---:|---|
| `toc_or_page_leader` | 158 | İçindekiler veya noktalı sayfa dizini şüphesi |
| `low_alphabetic_ratio` | 130 | Düşük harf oranı; teknik tablo da bu uyarıyı tetikleyebilir |
| `bibliography_possible` | 14 | Yoğun kaynakça / atıf içeriği şüphesi |
| `near_duplicate_candidate` | 32 | İlk taramadaki yüksek benzerlik adaylarıyla ilişkili |
| `short_chunk` | 8 | 600 karakterden kısa metin |
| `page_artifact_possible` | 7 | PDF sayfa geçişi artığı şüphesi |
| `unicode_replacement` | 2 | `�` yerine koyma karakteri |

Bir metin parçası birden fazla bayrak taşıyabileceği için bu satırlar toplanarak 246 sayısı elde edilemez. Örnek olarak ilk denetimde `cyber_000017` için içindekiler dizini, `cyber_008607` ve `cyber_008608` için Unicode bozulması şüphesi raporlanmıştır.

**Sınır:** Bayrak bulunmaması metnin hatasız olduğu anlamına gelmez. İşaretli 246 parçanın tamamı manuel olarak incelenip kabul/ret kararı verilmemiştir; bu parçalar otomatik olarak silinmemiştir.

## 3. Bölümleme: ilk aday ile güncel adayın farkı

İlk Corpus hazırlığında 3.075 soruluk Instruction Dataset'in **562 farklı kaynak belgeye** dayanan belge düzeyindeki bölümleme manifesti kullanıldı. Corpus'ta olup Instruction manifestinde bulunmayan **169 kaynak belge** için ayrı sabit kurallı bölümleme uygulandı. Bu yöntem **aynı adı taşıyan** kaynak belgelerin farklı train/validation/test kümelerine ayrılmasını engeller; ancak aynı belgenin farklı dosya adlarıyla kopyalanması sorununu tek başına çözmez.

| Corpus bölümü | İlk aday — kaynak | İlk aday — parça | Güncel aday — kaynak | Güncel aday — parça |
|---|---:|---:|---:|---:|
| Train | 588 | 7.702 | 587 | 7.643 |
| Validation | 73 | 980 | 77 | 1.059 |
| Test | 70 | 872 | 67 | 852 |
| **Toplam** | **731** | **9.554** | **731** | **9.554** |

İlk bölümlemede Instruction kayıtları **2.448 / 326 / 301** (train/val/test) şeklindeydi. **Güncel bölümlemede** bu değerler **2.418 / 359 / 298** oldu. Her iki aşamada da toplam **3.075 soru** korunmuştur.

**Güncel ve kullanılacak bölme dosyaları:**

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

Önceki `data/final/corpus_v1/` ve `data/final/instruction_v1/` klasörleri **eski ayrımın yedekleri** olarak tutulmaktadır. Güncel aday ile bu eski bölme dosyaları aynı analizde karıştırılmamalıdır.

## 4. Yakın tekrar incelemesi ve yeniden bölümleme

İlk Corpus otomatik denetimi, TF-IDF eşiklerine göre **65 aday çift (≥ 0,83)** ve bunlardan **16 aday çift (≥ 0,92)** raporlamıştı. Sonrasında `scripts/find_near_duplicates.py` ile ayrı bir tarama yürütüldü ve **63 yakın tekrar adayı çifti** belirlendi. Farklı taramaların çıktıları aynı liste veya aynı ölçüm olarak değerlendirilmemelidir.

İkinci taramadaki 63 çiftin **20'si ilk train/validation/test ayrımında farklı kümelerdeydi**. Farklı adla saklanmış, ortak pasaj taşıyan belgeler bu riske katkıda bulunuyordu. Saptanan bağlantılı kaynak gruplarını aynı bölmeye atayan `scripts/09_resplit_near_duplicates.py` ile yeni aday bölümleme oluşturuldu.

| Yeniden bölümleme sonucu | Değer |
|---|---:|
| İncelenen ikinci tarama yakın tekrar adayı çifti | 63 |
| Önceki ayrımda farklı bölmelerdeki aday çift | 20 |
| Yeni ayrımda farklı bölmelerde kalan **tespit edilmiş** aday çift | **0** |
| Bölümü değişen kaynak belge | 8 |
| Farklı bölmeye geçen Corpus parçası | 199 |
| Farklı bölmeye geçen Instruction sorusu | 64 |
| Silinen Corpus/Instruction kaydı | 0 |

**Yorum:** Bu çalışma, **tespit edilen** 63 çift açısından olası değerlendirme sızıntısını azaltmıştır. Sıfır sonucu, veri setindeki **tüm** kopyaların veya bütün anlamsal benzerliklerin giderildiğini göstermez. Bazı aday çiftler gerçek kopya değil, farklı belgelerde ortaklaşan meşru teknik açıklamalar olabilir; bunlar silinmek yerine aynı bölmede tutulmuştur.

Dayanak belgeleri:

- `reports/corpus/near_duplicate_pairs.csv` — ikinci taramadaki 63 aday çift.
- `reports/corpus/near_duplicate_63_degerlendirme.csv` — çift bazlı değerlendirme.
- `reports/corpus/NEAR_DUPLICATE_INCELEME_RAPORU.md` — bulgular ve sınırlamalar.
- `reports/corpus/GUvenli_split_on_raporu.md` — kaynak taşıma ve yeniden bölümleme özeti.

## 5. Yeni adayın teknik doğrulaması

Yeni ayrım, `scripts/10_validate_resplit.py` ile ayrı bir teknik kontrolden geçirilmiştir. Kullanıcının yerel ortamında bildirilen kontrol çıktısına göre:

- **9.554** Corpus kaydı ve **3.075** Instruction kaydı korundu.
- Bütün kayıt kimlikleri korundu; `split` dışında veri içeriği değişmedi.
- Bölme JSONL dosyaları ilgili tam veri setleriyle uyumlu bulundu.
- Kaynak bazlı bölümleme ve Corpus–Instruction kaynak eşleşmesi kontrolü geçti.
- Tespit edilen 63 aday çiftin hiçbirinin farklı bölmelerde kalmadığı raporlandı.

**Sonuç:** Güncel bölümleme **teknik kontrolü geçti**. Bu sonuç, PDF'lerdeki asıl metinlerin doğruluğunu, açıklamaların teknik geçerliliğini veya lisans durumunu doğrulamaz.

Kontrol çıktısı: `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt`.

**Önemli:** `scripts/08_validate_datasets.py`, **eski** ayrımın sabit sayılarını kontrol eder. Güncel aday üzerinde bu betik yerine `scripts/10_validate_resplit.py` kullanılmalıdır.

## 6. Tamamlanmamış kontroller ve riskler

1. **Kaynak URL'leri ve lisanslar:** `reports/corpus/source_inventory.csv` envanteri mevcut olsa da özgün indirme URL'leri, erişim tarihleri, lisanslar ve yeniden dağıtım izinleri tüm kaynaklar için doğrulanmadı. İnternette erişilebilir olmak yeniden yayımlama izni anlamına gelmez.
2. **Manuel Corpus kalite kontrolü:** Önerilen 100–200 kayıt/parça düzeyinde temsilî inceleme tamamlanmadı. Otomatik bayrak taşıyan **246 parça** için de ayrı kabul/düzelt/çıkar kararları henüz tamamlanmış değildir.
3. **PDF karşılaştırması:** Ham PDF ile çıkarılmış metnin birebir eşleşmesi, OCR kayıpları ve temizleme öncesi–sonrası örnekleri sistematik olarak doğrulanmadı.
4. **Token sayımı:** Gerçek model tokenizer'ı ile güncel Corpus token sayısı ölçülmedi. Kelime sayısı ve eski aşamaların yaklaşık token değerleri, bu sürümün doğrulanmış token sayısı olarak kullanılamaz.
5. **Dil ve görev etiketleri:** Corpus dil dağılımı sistematik doğrulanmadı; Instruction tarafındaki konu etiketleri ayrıca görev türü etiketlemesinin yerini tutmaz.
6. **Kapsamlı tekrar ve sızıntı kontrolleri:** Kullanılan TF-IDF taramalarının dışında kalan anlamsal tekrarlar hâlâ bulunabilir.
7. **Uçtan uca yeniden üretilebilirlik:** Veri hazırlama betikleri mevcut olsa da PDF indirmeden son JSONL üretimine kadar bütün akışın başka bir ortamda aynı sonuçla tekrar çalıştığı gösterilmedi. İlk Corpus ön kontrol paketinin tek başına ham PDF'den veri seti ürettiği iddia edilmemektedir.
8. **Parça sınırları:** Orijinal metin parçalarının anlamlı paragraf/başlık sınırlarıyla uyumu sistematik doğrulanmadı; yeniden bölümleme metni yeniden parçalamadı.

Bu eksikler tamamlanmadan veri seti **kesinleşmiş, tam doğrulanmış Corpus v1.0** olarak tanıtılmamalıdır. Kaynak pasajları ve PDF'ler için paylaşım lisansları doğrulanmadan tam veri dosyaları herkese açık GitHub deposuna eklenmemelidir.

## 7. İlgili çıktılar

**İlk otomatik kontrol paketi:**

- `corpus_kontrol_paketi/output/domain_corpus_v1_aday.jsonl` — ilk işaretlenmiş Corpus adayı.
- `corpus_kontrol_paketi/output/domain_corpus_inceleme_gerekenler.jsonl` — 246 uyarılı parça.
- `corpus_kontrol_paketi/output/review_manifest.csv` — manuel karar kaydı için liste.
- `corpus_kontrol_paketi/output/source_inventory.csv` — kaynak envanteri.
- `corpus_kontrol_paketi/output/near_duplicates_review.csv` — ilk taramadaki 65 aday çift.
- `corpus_kontrol_paketi/output/audit_summary.json` — ilk denetim istatistikleri.

**Güncel teknik kontrol ve yeniden bölümleme:**

- `data/final/guvenli_split_aday/` — Corpus ve Instruction için kullanılacak güncel aday dosyalar.
- `reports/corpus/GUvenli_split_on_raporu.md` — değişen kaynakların listesi ve yeni bölme sayıları.
- `reports/corpus/YENI_SPLIT_DOGRULAMA_RAPORU.txt` — teknik doğrulama çıktısı.

**Genel değerlendirme:** Metin ve kaynak bağlantılarının temel teknik bütünlüğü kontrol edilmiş, tespit edilen çapraz-bölme benzerlikleri yeni adayda giderilmiştir. Ancak belgenin teknik içeriğine ilişkin bağımsız manuel doğrulama, kaynak lisansı ve tam yeniden üretilebilirlik konularında çalışma sürmektedir.
