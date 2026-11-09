# Domain Corpus — Benzer Metin (Near-Duplicate) İnceleme Raporu

**Tarih:** 2026-11-09  
**İncelenen corpus:** `domain_corpus_v1_aday.jsonl` — 9.554 kayıt  
**Algılama çıktısı:** `near_duplicate_pairs.csv` — 63 olası benzer metin çifti  
**Yöntem:** 63 çiftin ID'leri, kaynak doküman adları, bölmeleri ve orijinal metinleri eşleştirildi; TF-IDF kosinüs skoru ile metin örtüşmesi karşılaştırıldı. Etiketler ön inceleme değerlendirmesidir; bütün çiftler için kesin semantik eşdeğerlik kararı verilmemiştir.

## Özet

- **63 potansiyel benzer metin çifti** tespit edilmiştir; otomatik olarak 63 mükerrer kayıt anlamına gelmez.
- **19 çift** aynı kaynak dokümanın farklı parçaları arasındadır; paragraf/şablon/tekrar içerebilir.
- **44 çift** farklı dosya adları arasındadır; bir kısmı aynı yayın, bir kısmı farklı yayınların paylaştığı standart metin olabilir.
- **20 çift farklı veri bölmelerine dağılmıştır** (train/val/test). Bu, kaynak bazlı split kontrolünü geçse bile **yakın-mükerrer veri sızıntısı riski** olduğunu gösterir.
- **8 çapraz-split çift** iki ayrı dosya adı altında saklanan OWASP ASVS 5.0 metninden gelir. Bunlar yüksek öncelikli temizleme/split düzeltme adaylarıdır.
- **Hiçbir kayıt bu incelemede silinmedi; tüm sayılar aynen korunuyor.**

## Ön İnceleme Sınıflandırması

| Ön inceleme kategorisi | Çift sayısı |
|---|---:|
| Tek kaynak içindeki örtüşen/tekrarlanan parça | 19 |
| Farklı yılların raporları: tekrar eden bölüm/şablon | 8 |
| Farklı NIST yayınlarında ortak/alıntı içerik | 9 |
| Farklı yayınlarda benzer ortak teknik pasaj | 5 |
| Olası aynı kitabın farklı adla/edisyonla kopyası | 9 |
| Farklı kaynaklarda benzer eğitim materyali | 4 |
| Çok güçlü belge kopyası göstergesi (OWASP ASVS 5.0) | 8 |
| Olası aynı NIST dokümanının farklı adları | 1 |

Bu kategoriler **silme kararları değildir**. Dokümanların farklı sürümleri, tekrar kullanılan standart tablolar ve kitaplardaki başlık/örnek tekrarları bulunabilir.

## Veri Sızıntısı Riski — 20 Çapraz-Split Eşleşme

Kaynak belge adına göre yapılan bölme kontrolü geçmiştir; fakat aynı dokümanın alternatif dosya adı altında farklı gruba düşmesi ve farklı dokümanların aynı pasajları kullanması mümkündür. En belirgin örnek, OWASP ASVS 5.0'ın `(1)` ekli ve eksiz dosya adlarıdır.

| # | Kimlikler | Bölmeler | TF-IDF skoru | Kaynak özeti |
|---|---|---|---:|---|
| 5 | `cyber_001198` / `cyber_002293` | train / val | 0.8688 | Ayrı teknik belgelerde ortak pasaj |
| 9 | `cyber_001663` / `cyber_001861` | test / train | 0.8823 | Ayrı teknik belgelerde ortak pasaj |
| 28 | `cyber_004061` / `cyber_007848` | test / train | 0.8916 | Ayrı teknik belgelerde ortak pasaj |
| 29 | `cyber_004494` / `cyber_005998` | test / train | 0.8949 | BTK / başka eğitim materyali |
| 30 | `cyber_004499` / `cyber_006003` | test / train | 0.8712 | BTK / başka eğitim materyali |
| 31 | `cyber_004500` / `cyber_006004` | test / train | 0.9240 | BTK / başka eğitim materyali |
| 32 | `cyber_004504` / `cyber_006007` | test / train | 0.8738 | BTK / başka eğitim materyali |
| 41 | `cyber_005187` / `cyber_008442` | train / test | 0.9464 | OWASP ASVS 5.0 dosya varyantları |
| 42 | `cyber_005190` / `cyber_008443` | train / test | 0.8542 | OWASP ASVS 5.0 dosya varyantları |
| 43 | `cyber_005193` / `cyber_008446` | train / test | 0.8938 | OWASP ASVS 5.0 dosya varyantları |
| 44 | `cyber_005194` / `cyber_008447` | train / test | 0.9050 | OWASP ASVS 5.0 dosya varyantları |
| 45 | `cyber_005195` / `cyber_008449` | train / test | 0.9499 | OWASP ASVS 5.0 dosya varyantları |
| 46 | `cyber_005214` / `cyber_008450` | train / test | 0.9915 | OWASP ASVS 5.0 dosya varyantları |
| 47 | `cyber_005220` / `cyber_008451` | train / test | 0.9978 | OWASP ASVS 5.0 dosya varyantları |
| 48 | `cyber_005241` / `cyber_008452` | train / test | 0.8768 | OWASP ASVS 5.0 dosya varyantları |
| 50 | `cyber_005290` / `cyber_007978` | train / val | 0.9690 | NIST SP 800-172 / SP 800-160v2 ortak pasaj |
| 51 | `cyber_005291` / `cyber_007979` | train / val | 0.9592 | NIST SP 800-172 / SP 800-160v2 ortak pasaj |
| 52 | `cyber_005292` / `cyber_007980` | train / val | 0.9716 | NIST SP 800-172 / SP 800-160v2 ortak pasaj |
| 53 | `cyber_005293` / `cyber_007981` | train / val | 0.9774 | NIST SP 800-172 / SP 800-160v2 ortak pasaj |
| 58 | `cyber_007368` / `cyber_009551` | val / test | 0.8686 | Ayrı teknik belgelerde ortak pasaj |

## Somut bulgular

- **OWASP ASVS (`cyber_005220` / `cyber_008451`)**: TF-IDF **0,9978**; metinler neredeyse aynı ve **train/test** arasında. Bu iki kaynağın aynı yayın olduğu dosya adlarından anlaşılmaktadır.
- **OWASP ASVS (`cyber_005214` / `cyber_008450`)**: TF-IDF **0,9915**; benzer şekilde **train/test** arasında.
- **ENISA Threat Landscape 2023/2022**: Ortak öneri ve kontrol bölümleri tekrar kullanılabiliyor. Farklı yıllara ait raporların tümünü mükerrer saymak doğru olmaz.
- **NIST SP 800-172 / NIST SP 800-160v2**: Birden çok yüksek benzerlikli çift **train/val** arasında; farklı belgelerde yinelenen içerik olup olmadığı metin seviyesinde doğrulanmalı.
- **Hacking/Penetration Testing kitabı**: Aynı kitabı andıran iki dosya adında 9 benzer çift var. Kaynak adı ve edisyon kontrolü olmadan kopyalardan biri silinmemeli.
- **Aynı kaynak içindeki 19 eşleşme**: Eşleşmelerin bazıları bölüm şablonları, sayfa tekrarları ve chunk sınırları nedeniyle oluşmuş olabilir; hepsini tekrar diye atmak gerekmez.

## Öncelikli sonraki işlem

1. Aynı yayın için **kanonik doküman kimliği** (dosya adı varyantları dahil) belirle; özellikle OWASP ASVS 5.0.
2. Gerçekten mükerrer olduğu doğrulanan doküman sürümlerini, hangi sürüm kalacak kararıyla değerlendir.
3. Kanonik kaynak gruplarına göre corpus ile instruction bölmelerini **birlikte yeniden oluştur ve doğrula**; bunların uyumlu kalması gerekir. Mevcut JSONL dosyalarını doğrudan silme/değiştirme.
4. Sayı ve kaynak eşleşmesi testine ilave olarak **çapraz-split near-duplicate kontrolü** çalıştır; yeni split sonrası bu 20 eşleşme değerlendirilmeden veri sızıntısı sorununun kapandığı söylenmemeli.
5. Sonuçları `DATASET_CARD.md`, `INSTRUCTION_CARD.md` ve teknik doğrulama raporuna güncelleme olarak işle.

## Sınırlamalar

Bu tarama **TF-IDF tabanlı ve eşik bağımlıdır**. 63 çift, tüm olası yakın-mükerrerlerin eksiksiz listesi değildir; diğer örtüşmeler kaçmış olabilir. “Benzer metin” ile “yanlışlıkla kopyalanan veri” aynı şey değildir. İnceleme dosyası `near_duplicate_63_degerlendirme.csv` içindeki etiketler ön karar olup metinlerin tüm bağlamsal içerik ve lisans şartlarının kesin doğrulaması değildir.
