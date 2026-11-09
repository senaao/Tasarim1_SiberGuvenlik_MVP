# 28 yüksek öncelikli soru: kaynak temelli inceleme

Bu turda **28** önce yüksek öncelikli olarak işaretlenmiş kayıt, sağlanan `source_text` parçaları ve soru-cevapları karşılaştırılarak gözden geçirildi. İşlem tüm veri seti için uzman onayı anlamına gelmez.

| Karar | Kayıt |
|---|---:|
| Aynen koru | 4 |
| Kaynaktan yeniden yaz | 11 |
| Teknik QA dışında bırak | 13 |
| Yeni aday toplamı | 3.075 |

**Kapsam sınırı:** 3.075 kaydın büyük kısmı yalnızca Qwen incelemesi ve kural temelli taramalardan geçti. 28 öncelikli kaydın tamamı tek tek incelendi; bunlardan 11 tanesi source_text içeriğiyle yeniden yazıldı. Belgelerin özgün PDF biçimleri doğrulanmadı. Kaynakta OCR/metin çıkarma hataları bulunabilir. `verified` alanları değiştirilmedi.

## Kararlar

| ID | Karar | Gerekçe |
|---|---|---|
| `draft_0210` | REWRITE_QA_FROM_SOURCE | Özgün cevap altıncı maddede kesiliyor; Türkçe kaynağa dayalı daha dar listeyle yeniden yazıldı. |
| `batch500_0455` | EXCLUDE_FROM_TECHNICAL_QA | Kaynak yalnızca kaynakça girdisi; teknik mekanizma içermiyor. |
| `batch_new500_0089` | RETAIN_QA_AFTER_SOURCE_READ | EPP/HPP ayrımı kaynakta açıkça tanımlanıyor. |
| `batch_new500_0130` | EXCLUDE_FROM_TECHNICAL_QA | Sertifika tanımı sorusu; teknik siber güvenlik ölçümüne uygun değil. |
| `batch_new500_0175` | EXCLUDE_FROM_TECHNICAL_QA | Firewall türleri ve teknik ayrıntılar kaynak pasajında yer almıyor. |
| `batch1000_0047` | REWRITE_QA_FROM_SOURCE | Özgün komut listesi yarıda kalmış; kaynakta görülen adımlar tamamlandı. |
| `batch1000_0082` | EXCLUDE_FROM_TECHNICAL_QA | Standart numaraları listesi yarıda kesilmiş; teknik süreç sorusu değil. |
| `batch1000_0099` | REWRITE_QA_FROM_SOURCE | Kesilmiş cevap tamamlandı; kaynakta açıkça belirtilen yanıt/yokluk sınırlaması korundu. |
| `batch1000_0317` | EXCLUDE_FROM_TECHNICAL_QA | CS1 faaliyet alanları listesi yarıda kesilmiş ve teknik soru değil. |
| `batch1000_0463` | REWRITE_QA_FROM_SOURCE | Yarım kalan madde listesi kaynak bilgileriyle tek cevap olarak yeniden yazıldı. |
| `batch1000_0529` | REWRITE_QA_FROM_SOURCE | Özgün IP listesi yarıda kalmış; altı aralık kaynak pasajından tamamlandı. Bunların tümünün RFC1918 özel adres olmadığını unutmayın. |
| `batch1000_0755` | RETAIN_QA_AFTER_SOURCE_READ | DLP çözümlerinin API destekli olup davranış analizi içermesi kaynakta bulunuyor; Türkçeden İngilizceye çevrilmiş. |
| `batch1000_0762` | EXCLUDE_FROM_TECHNICAL_QA | Genel tedarik ve yaşam döngüsü kriterleri; teknik savunma sorusu değil, cevap da yarım. |
| `batch1000_0804` | EXCLUDE_FROM_TECHNICAL_QA | KSA kod listesi yarıda kesilmiş; bulut güvenliği teknik sorusu değil. |
| `batch1000_0964` | EXCLUDE_FROM_TECHNICAL_QA | Kaynak en az beş savunma mekanizmasını araştırma görevi veriyor; cevap listesi kaynaktan çıkmıyor. |
| `kaggle1000_0228` | REWRITE_QA_FROM_SOURCE | PDF kaynak çıkarımında yazar adları Kubernetes teriminin arasına karışmış; cevap bu bozukluğu temizleyerek yeniden yazıldı. |
| `kaggle1000_0406` | EXCLUDE_FROM_TECHNICAL_QA | Privacy Act yükümlülüğü üzerine hukuk sorusu. |
| `kaggle1000_0538` | RETAIN_QA_AFTER_SOURCE_READ | Ağ, donanım ve yazılım seviyesinde güvenlik testleri kaynakta açıkça belirtilmiş; konu etiketi DevSecOps/System Security olabilir. |
| `kaggle1000_0557` | RETAIN_QA_AFTER_SOURCE_READ | Adware tanımı ve yan etkileri kaynakta açıkça bulunuyor. |
| `kaggle1000_0665` | EXCLUDE_FROM_TECHNICAL_QA | Matematiksel çıkarım bağlama bağımlı, bozuk sembollü ve teknik IR sorusu olarak zayıf. |
| `kaggle1000_0854` | EXCLUDE_FROM_TECHNICAL_QA | Kitabın hedef kitlesini soruyor; sızma testi mekanizması değil. |
| `extra_20261108_1833` | REWRITE_QA_FROM_SOURCE | Özgün liste yarıda kalmış; görüş NIST kararı olarak değil kaynakta yer alan kamu yorumu olarak sunuldu. |
| `extra_20261108_2331` | REWRITE_QA_FROM_SOURCE | Hatalı "network key" çevirisi "switch", "financial malware" ifadesi "ransomware" olarak Türkçe kaynakla düzeltildi. |
| `extra_20261108_2333` | EXCLUDE_FROM_TECHNICAL_QA | Cevap karışık politika/ürün listesi, yarıda kesilmiş; Incident Response etiketi uyumsuz. |
| `extra_20261108_672` | EXCLUDE_FROM_TECHNICAL_QA | NIST yayın revizyonu meta-bilgisi; yanıt yarım ve teknik Q&A hedefiyle düşük uyumlu. |
| `extra_20261108_5801` | REWRITE_QA_FROM_SOURCE | Kaynakta açık olmayan ayrıntılı geçiş matrisi ve gelecekteki tehditlere kesin uyarlanma iddiası çıkarıldı. |
| `extra_20261108_1344` | REWRITE_QA_FROM_SOURCE | Kesilmiş saldırı adımları yerine kaynakta açıklanan mekanizma özetlendi. |
| `extra_20261108_5607` | REWRITE_QA_FROM_SOURCE | Kaynağın doğrudan desteklemediği erişim yetkisi aşımı iddiası çıkarıldı. |

## Dosyalar

- `qa_3075_duzenlenmis_aday.jsonl`: 3.075 aday, 11 kayıtta `original_output` alanı korunarak `output` düzeltildi.
- `qa_13_teknik_kapsam_disi.jsonl`: 13 ayrılmış soru ve gerekçeleri.
- `qa_28_elle_inceleme_kararlari.jsonl`: karar tablosu.
- Kaynak girdi `qa_teknik_aday_v2.jsonl` değiştirilmedi.

## Sıradaki adım

- Kaynak belge düzeyinde sızıntısız train/validation/test ayırımı.
- Her splite yayılan bağımsız kaynak kontrolü örneklemesi ve konu etiketi gözden geçirme.
- README, Dataset Card ve kalite raporunda değerlendirmenin sınırlılıklarını açıklama.
