# Cybersecurity Domain Corpus — v1 aday / teknik ön inceleme

İnceleme tarihi: 9 Kasım 2026. Girdi: `domain_corpus_taslak_v2.jsonl`.
Bu rapor gerçek veri üzerinde çalışan otomatik kontrolleri yansıtır; uzman onayı verilmiş **nihai v1.0 değildir**.

## Kaydedilen bulgular

| Ölçüt | Değer |
| --- | ---: |
| Geçerli JSONL satırı / metin parçası | 9.554 |
| Farklı `source_document` | 731 |
| Benzersiz `id` | 9.554 |
| Birebir aynı `text` (SHA-256 ile) | 0 |
| Toplam karakter | 27.440.087 |
| Boşluğa göre ayrılmış toplam kelime | 3.988.017 |
| Metin parçası medyan uzunluğu | 2.910 karakter |
| En az bir kalite uyarısı alan parça | 246 |
| Uyarı almayan parça | 9.308 |
| TF-IDF benzerliği >= 0,83 olan çift | 65 |
| TF-IDF benzerliği >= 0,92 olan çift | 16 |

> **Uyarı almamak doğru / temiz olduğu anlamına gelmez.** 0,83 üzeri benzerlik de kesin kopya değildir. Özellikle tekrar eden şablonlar veya standart maddeleri benzer olabilir. İncelemeden silme yapılmadı.

## Kalite bayrakları

| İşaret | Parça sayısı | Yorum |
| --- | ---: | --- |
| `toc_or_page_leader` | 158 | İçindekiler veya noktalı sayfa dizini şüphesi |
| `low_alphabetic_ratio` | 130 | Metinde harf oranı düşük; tablolar da tetikleyebilir |
| `bibliography_possible` | 14 | Yoğun kaynakça / atıf içeriği şüphesi |
| `near_duplicate_candidate` | 32 | Yüksek benzerlik çiftinde yer alıyor |
| `short_chunk` | 8 | 600 karakterden kısa |
| `page_artifact_possible` | 7 | PDF sayfa geçiş artığı olabilir |
| `unicode_replacement` | 2 | Bozuk `�` karakteri bulundu |

Bir parça birden çok nedenle işaretlenebilir. Bu nedenle sütunlar toplanmaz.
Örnek: `cyber_000017` (NIST 800-53) noktalı içindekiler dizini içeriyor; `cyber_008607` ve `cyber_008608` bozuk Unicode içeriyor.

## QA setine göre sızıntıyı önleyen bölme

Önceden oluşturulan 3.075 soruluk instruction setinin *doküman düzeyindeki* split manifesti esas alındı.
QA'daki **562 dokümanın tamamı** corpus içinde bulundu ve split'i korundu. Yalnızca corpus'ta olup QA manifestinde olmayan 169 doküman, sabit SHA-256 tabanlı 80/10/10 sınıflandırmasıyla ayrıldı.

| Corpus split | Doküman | Metin parçası |
| --- | ---: | ---: |
| Train | 588 | 7.702 |
| Validation | 73 | 980 |
| Test | 70 | 872 |
| Toplam | 731 | 9.554 |

Bölme doğrulaması: QA'daki 2.448 train, 326 validation ve 301 test sorusunun kaynak belgeleri corpus'taki aynı split'e denk geliyor; uyuşmazlık **0**.
Bu, aynı belge seviyesinde sızıntıyı önler; farklı belgelerde yinelenen pasajlar için ayrıca benzerlik değerlendirmesi gerekir.

## Sınırlılıklar ve tamamlanması gerekenler

1. **Telif/lisans ve URL:** Kaynak JSONL'de yalnızca `id`, `source_document`, `source_path`, `text` var. Gerçek indirme URL'si, erişim tarihi ve lisans yok. `source_inventory.csv` içinde bu sütunlar boş veya `NOT_VERIFIED` olarak bırakıldı; bunlar orijinal PDF/indirme kayıtlarından doğrulanmalıdır. Yayınların internette erişilebilir olması yeniden dağıtım lisansı olduğu anlamına gelmez.
2. **Tokenizer:** Qwen tokenizer'ının gerçek token sayıları burada ölçülmedi; kelime sayısı token sayısı diye raporlanmamalıdır. Modelin tokenizer'ı ile ayrıca hesaplanmalı.
3. **Dil ve alan etiketleri:** Girdi JSONL'de yoktur. Atanmamıştır; kaynaklara göre ayrıca kontrol edilmelidir.
4. **PDF extraction:** Orijinal ham PDF'ler burada olmadığından metnin PDF ile birebir uyumu veya temizleme öncesi–sonrası farkı doğrulanamaz. Bazı chunk'lar sayfa dizini / kaynakça içeriyor.
5. **Manuel kalite kontrol:** Bu corpus için 100–200 belgelik örnek incelemesi henüz tamamlanmadı. `review_manifest.csv` öncelikli kontrol için kullanılır; 246 işaretli parça da otomatik olarak silinmedi.
6. **Tekrarlanabilirlik:** `scripts/prepare_corpus.py` ve `scripts/find_near_duplicates.py` çalışma mantığını açıklar. Orijinal indirme, extraction, cleaning kodları bu yüklemede bulunmadığı için bu ZIP tek başına PDF'den başa kadar pipeline'ı yeniden çalıştıramaz.
7. **Metin bölme:** Orijinal chunk'ların semantik paragraf sınırlarına uygunluğu otomatik doğrulanmadı. Girdi metni korundu; chunk'lar yeniden kesilmedi.

## Üretilenler

- `domain_corpus_v1_aday.jsonl`: Metinleri korunmuş, belge kimliği, split, karakter/kelime sayısı ve kalite bayrakları eklenmiş **aday** corpus.
- `domain_corpus_train.jsonl`, `domain_corpus_val.jsonl`, `domain_corpus_test.jsonl`: QA ile doküman bazında uyumlu bölümler.
- `domain_corpus_inceleme_gerekenler.jsonl`: 246 uyarı işaretli parça.
- `review_manifest.csv`: İnceleme kararlarını kaydetmek için boş sütunları olan kontrol listesi.
- `source_inventory.csv`: Kaynak belgelere göre envanter; eksik lisans/URL açıkça belirtiliyor.
- `near_duplicates_review.csv`: 65 olası yakın kopya çifti; uzman kontrolü bekler.
- `audit_summary.json`: Sayısal ön kontrol sonuçları.

**Sonraki adım:** Önce işaretlenen parçaları ve 100–200 rastgele belge örneğini incele; ardından açıklamalı kararları uygula. Lisans, URL ve token istatistiklerini tamamlayınca corpus v1.0 olarak kesinleştirilebilir.
