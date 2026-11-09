# Siber Güvenlik Domain Corpus ve Instruction Dataset

**Proje türü:** Bilgisayar Mühendisliği — Tasarım/Bitirme Projesi veri hazırlama çalışması  
**Alan:** Siber güvenlik  
**Durum (9 Kasım 2026):** v1.0 için **aday** veri setleri ve ön kalite kontrol. Tam doğrulama henüz tamamlanmamıştır.

## Projenin amacı

Siber güvenlik alanında teknik dokümanlardan elde edilen metinlerle bir **Domain Corpus** hazırlamak ve kaynak pasajlarıyla ilişkilendirilebilen soru-cevap örneklerinden bir **Instruction Dataset** oluşturmak. Veri setleri sonraki aşamalarda alan uyarlaması, instruction fine-tuning ve değerlendirme çalışmalarına temel oluşturmak üzere tasarlanmıştır. Bu repo aşamasında model eğitildiği veya bir RAG uygulamasının tamamlandığı iddia edilmemektedir.

## Veri setlerinin mevcut durumu

| Bileşen | Mevcut içerik | Durum |
|---|---:|---|
| Domain Corpus | 9.554 metin parçası (chunk), 731 kaynak belge | Otomatik ön denetim yapıldı; manuel kontrol sürüyor |
| Instruction Dataset | 3.075 soru-cevap adayı, 562 kaynak belge | Kural/model taraması ve sınırlı kaynak kontrolü yapıldı; tamamı insan tarafından doğrulanmadı |
| Corpus train/val/test | 7.643 / 1.059 / 852 chunk | Yeni kaynak-gruplu ayrım, teknik kontrol başarılı |
| Instruction train/val/test | 2.418 / 359 / 298 örnek | Yeni kaynak-gruplu ayrım, teknik kontrol başarılı |
Güncel veri ayrımı `data/final/guvenli_split_aday/` klasöründedir.

Yakın tekrar incelemesinde 63 aday metin çifti tespit edilmiştir.
Bunlardan farklı train/validation/test bölmelerinde bulunan 20 çift,
kaynak-gruplu yeniden bölümleme sonrasında 0'a indirilmiştir.

Toplam 9.554 Corpus parçası ve 3.075 soru-cevap korunmuştur.
Yeni bölümleme bağımsız teknik doğrulamadan geçmiştir.
Eski bölmeler yedek olarak saklanmaktadır.

Bu sonuç, tespit edilmemiş tüm veri benzerliklerinin
giderildiği anlamına gelmez.
Instruction ve Corpus splitleri 
**kaynak belge düzeyinde hizalanmıştır**; aynı kaynak belge iki farklı kümeye yerleştirilmemiştir. Bununla birlikte farklı adlarla kaydedilmiş benzer belgeler/örnekler için ek kontrol gereklidir.

## Dizin yapısı

```text
Tasarim1_SiberGuvenlik/
├── data/
│   ├── raw/                    # İlk indirilen veri
│   ├── extracted/              # PDF'den çıkarılmış metin
│   ├── cleaned_v2/             # Temizleme aşaması
│   └── final/
│       ├── domain_corpus_v1_aday.jsonl
│       ├── instruction_dataset_3075_aday.jsonl
│       └── instruction_v1/
│           ├── train.jsonl
│           ├── val.jsonl
│           └── test.jsonl
├── scripts/                     # Mevcut veri işleme betikleri
├── reports/
│   ├── corpus/                 # Domain Corpus kalite raporu
│   └── instruction/            # Soru-cevap kalite inceleme raporları
└── corpus_kontrol_paketi/
    ├── scripts/                 # Corpus ön denetim ve hazırlama betikleri
    ├── output/                  # Corpus adayları, envanter ve split çıktıları
    ├── reports/
    └── splits/
```

> **Not:** `data/final/` altında önceki denemelerden kalan `corpus.jsonl`, `corpus_v2.jsonl`, `train.jsonl`, `val.jsonl` ve `test.jsonl` gibi ek dosyalar bulunabilir. Bunlar `instruction_v1/` içindeki yeni soru-cevap splitleriyle karıştırılmamalıdır. Eski veriler değerlendirilmeden silinmemelidir.

## Alan kapsamı ve veri yapısı

Malware ve zararlı yazılım analizi, dijital adli bilişim, bulut güvenliği, DevSecOps, ağ ve sistem güvenliği, kimlik doğrulama, kriptografi, mobil/web güvenliği, olay müdahalesi ve sızma testi gibi teknik konular yer alır. Kaynaklar teknik PDF/doküman metinleri ve daha önce toplanmış siber güvenlik kayıtlarından oluşur; her kaynağın URL ve lisansı henüz bütünüyle doğrulanmış değildir.

- **Corpus (JSONL):** Metin (`text`), belge ilişkisi (`source_document`/`document_id`), kayıt kimliği ve kalite/split meta verileri içerir.
- **Instruction (JSONL):** `id`, `source_document`, `topic`, `source_text`, `output` ve inceleme durumu alanlarını içerir. Mevcut `output` alanındaki soru-cevap biçimi, ileride kullanılacak SFT şemasına göre ayrıca dönüştürülüp test edilmelidir.
- **Bölme ilkesi:** Aynı `source_document` üzerinden üretilen kayıtlar aynı splitte tutulur; corpus ve instruction ayrımları birbiriyle uyumludur.

## Ön kalite kontrol sonuçları

- Domain Corpus için **birebir aynı metin: 0**; **en az bir kalite uyarısı taşıyan chunk: 246**.
- TF-IDF taramasında benzerlik eşiği 0,83 veya üzeri olan **65 çift** aday olarak tespit edildi; bunlar kesin tekrar sayılmamış ve otomatik silinmemiştir.
- Instruction tarafında **28 yüksek öncelikli kayıt** kaynak pasajıyla incelendi: **4 korundu, 11 yeniden yazıldı, 13 çıkarıldı**. Ek bir 60'lık örneklem için değerlendirme raporu ayrıca mevcuttur; bu incelemeler tüm 3.075 örneğin onaylandığı anlamına gelmez.
- `verified: false` işaretli kayıtların doğrulanmış kabul edilmemesi gerekir.

Ayrıntılar: `reports/corpus/` ve `reports/instruction/`.

## Yeniden üretilebilirlik

Corpus ön hazırlama paketindeki iki betik, mevcut girdi ve QA split manifesti kullanılarak tekrar çalıştırılabilir:

```bash
pip install -r corpus_kontrol_paketi/requirements.txt
python corpus_kontrol_paketi/scripts/find_near_duplicates.py --input domain_corpus_taslak_v2.jsonl --output near_pairs.csv
python corpus_kontrol_paketi/scripts/prepare_corpus.py --input domain_corpus_taslak_v2.jsonl --qa-manifest corpus_kontrol_paketi/splits/split_manifest.csv --near-pairs near_pairs.csv --out prepared_corpus
```

`domain_corpus_taslak_v2.jsonl` yukarıdaki komutta **örnek girdi dosya adıdır**; dosyanın gerçek konumuna göre yol değiştirilmelidir. Bu iki betik yalnızca *corpus ön denetim/hazırlama* işlemlerini kapsar; ilk PDF indirmelerinden itibaren uçtan uca tekrarlanabilirlik henüz belgelenip sınanmamıştır.

## Bilinen eksikler ve sonraki doğrulamalar

1. Kaynak belge URL'leri, erişim tarihleri, lisansları ve yeniden dağıtım koşulları doğrulanmalı.
2. Gerçek model tokenizer'ı ile token sayımı ve dağılım raporu oluşturulmalı; kelime sayısı token sayısı değildir.
3. Corpus için rastgele 100–200, instruction için 150–200 örnek üzerinde belgeye dayalı manuel QA tamamlanmalı.
4. Şüpheli yakın tekrarlar, PDF çıkarım artıkları, eksik cevaplar ve konu/görev türü etiketleri gözden geçirilmeli.
5. Instruction kayıtlarının görev türleri sınıflandırılmalı; kullanılacak eğitim şemasına dönüştürülüp doğrulanmalı.
6. Veri aşamalarını kapsayan betik, ayar, bağımlılık ve istatistik raporları tek bir yeniden üretme akışına bağlanmalı.

## Telif, lisans ve paylaşım

**Kaynak dokümanların yeniden dağıtım izinleri teyit edilene kadar ham PDF'ler, tam corpus metinleri ve kaynak pasajlarını içeren tüm instruction kayıtları herkese açık GitHub deposuna yüklenmemelidir.** Depoda öncelikle kod, raporlar, şema belgeleri, kaynağı doğrulanmış küçük örnekler ve veri üretme yönergeleri paylaşılmalıdır.

## İlgili belgeler

Vize teslimi için `DATASET_CARD.md` (Domain Corpus), `INSTRUCTION_CARD.md` (Instruction Dataset), kaynak envanteri, teknik istatistikler ve manuel QA raporları ayrıca hazırlanıp güncellenecektir.
