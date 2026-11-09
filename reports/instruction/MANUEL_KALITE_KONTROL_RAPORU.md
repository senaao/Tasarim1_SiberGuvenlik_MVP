# Instruction Dataset — Kayıt Bazlı Kalite Kontrol Raporu

**Tarih:** 9 Kasım 2026  
**Proje:** Siber güvenlik domain corpus ve instruction QA veri seti  
**Aşama:** v1.0 adayı, örneklem incelemesi yapılmış; **nihai bağımsız insan/uzman onayı tamamlanmamış**  
**İlgili veri seti:** `data/final/instruction_dataset_3075_aday.jsonl` (3.075 kayıt)

## 1. Yöntem ve kapsam

- İncelemeler, soru, cevap ve beraberindeki `source_text` pasajının kayıt bazında karşılaştırılmasına dayanır. Esas PDF ile birebir karşılaştırma veya bağımsız dış kaynak doğrulaması yapılmamıştır.
- **60 örneklik, 12 konuya eşit dağıtılmış** kaynak-temelli inceleme önceki **3.155 adaylı** aşamadan yapılmıştır. Bu örneklem rastgele tüm veri setini temsil etmez ve sonuçları hata oranı olarak genellenemez.
- **28 öncelikli kayıt** ayrı bir turda tek tek incelenmiş; korunma, yeniden yazma veya kapsam dışına çıkarma kararları verilmiştir.
- İki listedeki kayıt kimlikleri çakışmaz: **88 farklı soru** için kayıt bazında bir değerlendirme izi vardır. Bu incelemeler, son aşamada bir alan uzmanının elle onay vermesiyle eşdeğer tutulmamalıdır.
- Ayrı olarak yürütülen model/Qwen kontrolleri insan doğrulaması sayılmaz. Final adayında `verified` alanı **3.075 kaydın tamamında `false`** durumundadır.

## 2. Ölçülen sonuçlar

| İnceleme turu | İncelenen | Aynen korunan | Düzeltme önerilen / uygulanan | Çıkarılan |
|---|---:|---:|---:|---:|
| 60 örnek (eski aday aşaması) | 60 | 27 | 20 öneri; yeni adaydan çıkarıldı | 13 |
| 28 öncelikli kayıt | 28 | 4 | 11 kaynakla yeniden yazıldı | 13 |
| **Toplam** | **88** | **31** | **31** | **26** |

**Güncel 3.075 kayıtta izlenen durum:** Önceki incelemelerde uygun bulunan **27** kayıt + öncelikli turda korunan **4** ve yeniden yazılan **11** kayıt = **42 kayıt** güncel adayın içindedir. Diğer **46 kayıt** (60 turundan 20 düzeltme önerisi ve 13 çıkarma; 28 turundan 13 çıkarma) bu adayın içinde değildir. Bunlar kayıt kimlikleri üzerinden karşılaştırılarak teyit edilmiştir.

**Önemli yorum:** 42 kayıt için de `verified: false` olarak kalmıştır. Bunlar "inceleme izi olan" kayıtlardır, "insan tarafından kesin onaylanmış" kayıtlar değildir. Mevcut 3.075 kaydın **3.033’ü** bu iki kayıt-bazlı kontrol turu kapsamında tek tek ele alınmamıştır.

## 3. 60 örneklem turunda konu bazlı sonuçlar

| Konu | Uygun | Düzelt | Çıkar |
|---|---:|---:|---:|
| Authentication | 3 | 2 | 0 |
| Cloud Security | 3 | 1 | 1 |
| Cryptography | 3 | 0 | 2 |
| DevSecOps | 0 | 3 | 2 |
| Digital Forensics | 0 | 2 | 3 |
| Incident Response | 2 | 2 | 1 |
| Malware | 2 | 2 | 1 |
| Mobile Security | 1 | 2 | 2 |
| Network Security | 4 | 1 | 0 |
| Penetration Testing | 2 | 2 | 1 |
| System Security | 3 | 2 | 0 |
| Web Security | 4 | 1 | 0 |

Öne çıkan sorun tipleri: kaynağın desteklemediği cevap ayrıntıları, yarım kalan yanıtlar, soru-cevap uyumsuzluğu, yanlış konu etiketi, güncellik hatası, kaynakçada geçen başlıktan mekanizma uydurma ve aşırı basit sayı ezberine dayanan sorular.

## 4. 60 örneklemin kayıt bazlı denetim izi

Bu bölümde kararlar, eski 3.155 kayıtlı aşamaya ilişkin değerlendirme dosyasından aktarılmıştır. `DÜZELT` kayıtları güncel adayda bırakılmadı; dolayısıyla bir düzeltmenin uygulandığı ima edilmemelidir.

| ID | Konu | Karar | Güncel 3.075 içinde? | Gerekçe |
|---|---|---|---|---|
| `batch_new500_0127` | Authentication | UYGUN | Evet | PIP’nin PDP’ye erişim kararı için gerekli öznitelikleri sağladığı kaynakta açıkça belirtiliyor. |
| `draft_0150` | Authentication | UYGUN | Evet | eddsa-rdfc-2022 kriptografik paket adı kaynak örneğinde açık; doğru ama dar kapsamlı soru. |
| `batch1000_0495` | Authentication | UYGUN | Evet | SM-DR19 için üç kimlik doğrulama politikası kapsamı doğru aktarılmış. |
| `batch1000_0346` | Authentication | DUZELT | Hayır | Soru bir mekanizma istiyor; cevap yalnızca imzalı DNS kayıtlı sunucularla iletişim yapılandırmasını tekrar ediyor. DNSSEC bağlamı açıklaştırılmalı. |
| `batch1000_0265` | Authentication | DUZELT | Hayır | Beacon ile sinyal kalitesi değerlendirmesi kaynakta var; Authentication yerine Network Security konusu uygun. |
| `batch500_0266` | Cloud Security | CIKAR | Hayır | Benchmark commit numaraları kaynakta yer alsa da teknik güvenlik bilgisi değil, Cloud Security etiketi de uygun değil. |
| `extra_20261108_3142` | Cloud Security | UYGUN | Evet | Hipervizör güvenliği için mimari seçenekler ve yönetim yapılandırmaları kaynakta destekleniyor. |
| `batch500_0146` | Cloud Security | UYGUN | Evet | Varsayılan dış ağ erişimi ve konteyner çalışma zamanının güvenlik duvarını yönetmesi kaynakla uyumlu; ortam bağlamı korunmalı. |
| `extra_20261108_4600` | Cloud Security | DUZELT | Hayır | Protect bir CSF fonksiyonudur, kategori değildir. Cloud Security etiketi de yanıltıcı. |
| `extra_20261108_1453` | Cloud Security | UYGUN | Evet | Eski konteyner imajlarını temizleme ve değişmez sürüm adları kullanma, kaynaktaki iki önlemle örtüşüyor. |
| `kaggle1000_0811` | Cryptography | UYGUN | Evet | Dört varlık için altı ikili ilişki ve en az altı simetrik anahtar doğrudan destekleniyor. |
| `batch500_0207` | Cryptography | CIKAR | Hayır | Cevap yarıda kesilmiş; Q kümesini açıklarken cümle tamamlanmıyor. |
| `extra_20261108_1964` | Cryptography | UYGUN | Evet | Moderate/High düzeyde anahtar veya hassas metaveri çıkışında güvenilir kanal şartı doğrudan destekleniyor. |
| `kaggle1000_0267` | Cryptography | CIKAR | Hayır | Sağlanan kaynak parçasında deterministik cüzdanın DID üretim amacı anlatılmıyor; cevap kaynak dışı ayrıntı üretiyor. |
| `batch500_0015` | Cryptography | UYGUN | Evet | ρU kullanılarak 1/poly(λ) ölçeğinde ε-simülasyon güvencesi kaynakta yer alıyor; oldukça uzmanlık gerektiren soru. |
| `draft_0253` | DevSecOps | DUZELT | Hayır | 450 davranış etiketi sayısı doğru fakat DevSecOps sınıflandırması uyumsuz ve soru salt sayı ezberi. |
| `batch500_0160` | DevSecOps | DUZELT | Hayır | Üç donanım platformu doğru ancak çalışma post-kuantum kriptografi karşılaştırması; DevSecOps yerine Cryptography. |
| `batch_new500_0173` | DevSecOps | CIKAR | Hayır | Kaynak yalnızca ücret uygulandığını söylüyor; soru maliyet miktarını istiyor, yanıtın “fee applies” olması anlamsız. |
| `batch_new500_0365` | DevSecOps | DUZELT | Hayır | CSS yerleşim/yazı biçimi dengesizliği doğru; soru phishing tespiti olduğu için Web Security etiketi daha uygun. |
| `extra_20261108_5884` | DevSecOps | CIKAR | Hayır | Ipiguard yalnızca kaynakça başlığı olarak geçiyor; savunma mekanizmasına ilişkin yanıt bu pasajdan doğrulanamıyor. |
| `extra_20261108_4645` | Digital Forensics | DUZELT | Hayır | Kaynak olay zamanı ve hasarı kaydetme ve log korelasyonu anlatıyor; sorunun “hangi mekanizma” kısmı muğlak. |
| `draft_0203` | Digital Forensics | CIKAR | Hayır | Kaynak VASCO sisteminde toplam sekiz chaincode olduğunu belirtiyor; bunların tümünün hasta-akışı için olduğu kanıtlanmıyor. Digital Forensics ile de ilgisiz. |
| `kaggle1000_0807` | Digital Forensics | CIKAR | Hayır | Ulusal siber politika hedefleri ve düzenleme çerçevesi soruluyor; teknik Digital Forensics sorusu değil. |
| `batch500_0257` | Digital Forensics | DUZELT | Hayır | %96 doğruluk oranı kaynakta var; içerik dijital adli bilişimden çok sosyal mühendislik/phishing tespiti. |
| `extra_20261108_280` | Digital Forensics | CIKAR | Hayır | Soru dört garanti düzeyinin ne olduğunu istiyor; cevap yalnızca dört düzey bulunduğunu ve bölüm numarasını söylüyor. |
| `kaggle1000_0896` | Incident Response | CIKAR | Hayır | Yanıt soru cümlesini tekrar ediyor; teknik açıklama sağlamıyor ve Incident Response ile zayıf ilişkili. |
| `kaggle1000_0198` | Incident Response | DUZELT | Hayır | LNG tesisleri için fiziksel/teknik erişim güvenliği destekleniyor; Incident Response sınıflandırması uygun değil. |
| `batch1000_0037` | Incident Response | UYGUN | Evet | Host/IP, malware örnekleri ve açık türleri gibi olay göstergeleri kaynakta açıkça listeleniyor. |
| `kaggle1000_0338` | Incident Response | DUZELT | Hayır | Data Management yeteneği doğru; kaynak olay müdahalesinden çok hassas veri tespiti/koruması anlatıyor. |
| `extra_20261108_593` | Incident Response | UYGUN | Evet | Log saklama süresi, eski keşif etkinliği ve geç keşfedilen olaylara ilişkin açıklama kaynakla uyumlu. |
| `batch_new500_0290` | Malware | UYGUN | Evet | COVID-19 phishing eklerinde infostealer oranı kaynakta doğrudan %75 olarak veriliyor. |
| `kaggle1000_0648` | Malware | UYGUN | Evet | Phishing kitlerinin çalınan parolaları kit yazarına da gönderebildiği kaynakta açık. |
| `kaggle1000_0974` | Malware | CIKAR | Hayır | Kaynak 178 harf diyor; cevap 180 diyor. Ayrıca bunu “maksimum” olarak sorması sonucu çarpıtıyor. |
| `draft_0023` | Malware | DUZELT | Hayır | GraphViz neato ismi doğru fakat soru malware analizi bağlamını içermeyen genel bir araç ezberi. Malware grafiği ile ilişkilendirilmeli. |
| `kaggle1000_0497` | Malware | DUZELT | Hayır | Pretexting örneği doğru ancak Malware sınıflaması yerine kimlik avı/sosyal mühendislik bağlamı uygun. |
| `batch_new500_0177` | Mobile Security | DUZELT | Hayır | PE başlıkları ve sistem çağrıları malware veri kümesi özellikleridir; mobil güvenliğe özgü değil. |
| `kaggle1000_0682` | Mobile Security | CIKAR | Hayır | Kaynak Android 6 dönemine (~2015) ait; “today” ifadesi güncel gerçek olarak kullanılıyor. Teknik güvenlik bilgisi de değil. |
| `batch1000_0949` | Mobile Security | DUZELT | Hayır | Tam cihaz veya kapsayıcı tabanlı şifreleme kaynakta var; ancak bu iki yöntemi doğrudan SP 800-124 tavsiyesi olarak atfetmek tam desteklenmiyor. |
| `batch1000_0604` | Mobile Security | UYGUN | Evet | Eski Android bağlamında ro.secure=0 koşulu kaynakta açık; güncel Android sürümleri için genellenmemeli. |
| `batch_new500_0163` | Mobile Security | CIKAR | Hayır | Sorunun cevabı projeksiyon argümanına * FROM accounts-- SQL enjeksiyonu eklenmesidir; yanıt “accounts table” diyerek bilgiyi kaçırıyor. |
| `batch1000_0108` | Network Security | UYGUN | Evet | Endüstriyel ortamda UTP kablonun parazite duyarlı olduğu kaynaktan destekleniyor. |
| `batch1000_0824` | Network Security | DUZELT | Hayır | Eski 802.11 ailesindeki hızlar kaynakta var; 802.11 temel sürümü ve eklerinin ayrımı yapılmıyor, zamana duyarlı/genelleyici. |
| `batch500_0447` | Network Security | UYGUN | Evet | RL tabanlı savunma ajanında test-zamanı policy shaping yaklaşımı kaynakla örtüşüyor. |
| `batch500_0397` | Network Security | UYGUN | Evet | Girdi kontrolü, temsil, zamansallaştırma, transformer ve agregasyon sırası kaynakta birebir. |
| `kaggle1000_0051` | Network Security | UYGUN | Evet | IoT için uzun yama döngüsü ve sınırlı hesaplama kapasitesi kaynakta iki sorun olarak açık. |
| `batch500_0388` | Penetration Testing | DUZELT | Hayır | Kali adı doğru ancak soru yalnızca kitapta önerilen işletim sistemini soruyor; teknik gerekçe ve araçların rolü sorulmalı. |
| `batch1000_0988` | Penetration Testing | CIKAR | Hayır | 100 örnek sayısı kaynakta var fakat soru makalenin veri seçme ayrıntısını ezberletiyor; Penetration Testing bilgisi değil. |
| `batch1000_0903` | Penetration Testing | UYGUN | Evet | Basit HTML tarayıcıları ve siteyi örümcekleyerek dolaşan gelişmiş tarayıcılar kaynakta anlatılıyor. |
| `extra_20261108_1652` | Penetration Testing | UYGUN | Evet | Bridge ve Dynamic senaryolarındaki yaklaşık %64/%24 ödül iyileşmesi kaynakta doğrudan var. |
| `batch1000_0481` | Penetration Testing | DUZELT | Hayır | PhishOpt amaç fonksiyonu doğru; çalışma e-posta/phishing ajanlarına ilişkin, Penetration Testing etiketi tartışmalı. |
| `draft_0233` | System Security | UYGUN | Evet | Şema fuzzerının 1–7 alanlı mesaj ürettiği kaynakta net. |
| `kaggle1000_0235` | System Security | UYGUN | Evet | Sistem sahipleri, güvenlik sorumluları ve yöneticiler kaynağa göre belgeye ihtiyaç duyan roller. |
| `kaggle1000_0726` | System Security | UYGUN | Evet | 2009 tarihli raporda listelenen altı SCAP bileşeni tam aktarılmış; tarihsel bağlam korunmalı. |
| `batch500_0449` | System Security | DUZELT | Hayır | MCP04 için Medium doğru ancak yalnızca bir güven derecesi ezberleniyor; tehdit-kontrol sınırını açıklayan soruya dönüştürülmeli. |
| `batch1000_0875` | System Security | DUZELT | Hayır | 288/300 doğru ancak hangi değerlendirme metriği ve veri kümesinde olduğu belirsiz; çok bağlamsız ve düşük bilgi değeri. |
| `batch500_0132` | Web Security | DUZELT | Hayır | RAG veri deposu gizliliği için random projection doğru; Web Security yerine sistem/veri güvenliği daha uygun. |
| `kaggle1000_0273` | Web Security | UYGUN | Evet | MIDE çalışmasındaki %4,1, %12,7 ve %14,9 oranları doğru ve uygun paydalara dayanıyor. |
| `batch1000_0055` | Web Security | UYGUN | Evet | XSS için alert ile basit doğrulama örneği kaynakla uyumlu; yetkili test bağlamı korunmalı. |
| `extra_20261108_2285` | Web Security | UYGUN | Evet | Reflected ve stored XSS farkı kaynakta destekleniyor; ek açıklamalar genel teknik anlamla tutarlı. |
| `kaggle1000_0525` | Web Security | UYGUN | Evet | OWASP ASVS içinde parametreli sorgular/ORM ile veri tabanı enjeksiyonlarına karşı kontrol açıkça belirtilmiş. |

## 5. 28 öncelikli kaydın denetim izi

Bu turda **4 kayıt korundu, 11 kayıt kaynak metne dayanarak yeniden yazıldı, 13 kayıt teknik soru-cevap kapsamından çıkarıldı**. Yeniden yazılan 11 kaydın önceki cevabı geçmiş/sürüm kayıtlarında korunmuştur; nihai veri setinin bu değişiklikleri barındırdığı `id` eşleşmesiyle kontrol edilmiştir.

| ID | Karar | Güncel 3.075 içinde? | Gerekçe |
|---|---|---|---|
| `draft_0210` | `REWRITE_QA_FROM_SOURCE` | Evet | Özgün cevap altıncı maddede kesiliyor; Türkçe kaynağa dayalı daha dar listeyle yeniden yazıldı. |
| `batch500_0455` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Kaynak yalnızca kaynakça girdisi; teknik mekanizma içermiyor. |
| `batch_new500_0089` | `RETAIN_QA_AFTER_SOURCE_READ` | Evet | EPP/HPP ayrımı kaynakta açıkça tanımlanıyor. |
| `batch_new500_0130` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Sertifika tanımı sorusu; teknik siber güvenlik ölçümüne uygun değil. |
| `batch_new500_0175` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Firewall türleri ve teknik ayrıntılar kaynak pasajında yer almıyor. |
| `batch1000_0047` | `REWRITE_QA_FROM_SOURCE` | Evet | Özgün komut listesi yarıda kalmış; kaynakta görülen adımlar tamamlandı. |
| `batch1000_0082` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Standart numaraları listesi yarıda kesilmiş; teknik süreç sorusu değil. |
| `batch1000_0099` | `REWRITE_QA_FROM_SOURCE` | Evet | Kesilmiş cevap tamamlandı; kaynakta açıkça belirtilen yanıt/yokluk sınırlaması korundu. |
| `batch1000_0317` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | CS1 faaliyet alanları listesi yarıda kesilmiş ve teknik soru değil. |
| `batch1000_0463` | `REWRITE_QA_FROM_SOURCE` | Evet | Yarım kalan madde listesi kaynak bilgileriyle tek cevap olarak yeniden yazıldı. |
| `batch1000_0529` | `REWRITE_QA_FROM_SOURCE` | Evet | Özgün IP listesi yarıda kalmış; altı aralık kaynak pasajından tamamlandı. Bunların tümünün RFC1918 özel adres olmadığını unutmayın. |
| `batch1000_0755` | `RETAIN_QA_AFTER_SOURCE_READ` | Evet | DLP çözümlerinin API destekli olup davranış analizi içermesi kaynakta bulunuyor; Türkçeden İngilizceye çevrilmiş. |
| `batch1000_0762` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Genel tedarik ve yaşam döngüsü kriterleri; teknik savunma sorusu değil, cevap da yarım. |
| `batch1000_0804` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | KSA kod listesi yarıda kesilmiş; bulut güvenliği teknik sorusu değil. |
| `batch1000_0964` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Kaynak en az beş savunma mekanizmasını araştırma görevi veriyor; cevap listesi kaynaktan çıkmıyor. |
| `kaggle1000_0228` | `REWRITE_QA_FROM_SOURCE` | Evet | PDF kaynak çıkarımında yazar adları Kubernetes teriminin arasına karışmış; cevap bu bozukluğu temizleyerek yeniden yazıldı. |
| `kaggle1000_0406` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Privacy Act yükümlülüğü üzerine hukuk sorusu. |
| `kaggle1000_0538` | `RETAIN_QA_AFTER_SOURCE_READ` | Evet | Ağ, donanım ve yazılım seviyesinde güvenlik testleri kaynakta açıkça belirtilmiş; konu etiketi DevSecOps/System Security olabilir. |
| `kaggle1000_0557` | `RETAIN_QA_AFTER_SOURCE_READ` | Evet | Adware tanımı ve yan etkileri kaynakta açıkça bulunuyor. |
| `kaggle1000_0665` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Matematiksel çıkarım bağlama bağımlı, bozuk sembollü ve teknik IR sorusu olarak zayıf. |
| `kaggle1000_0854` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Kitabın hedef kitlesini soruyor; sızma testi mekanizması değil. |
| `extra_20261108_1833` | `REWRITE_QA_FROM_SOURCE` | Evet | Özgün liste yarıda kalmış; görüş NIST kararı olarak değil kaynakta yer alan kamu yorumu olarak sunuldu. |
| `extra_20261108_2331` | `REWRITE_QA_FROM_SOURCE` | Evet | Hatalı "network key" çevirisi "switch", "financial malware" ifadesi "ransomware" olarak Türkçe kaynakla düzeltildi. |
| `extra_20261108_2333` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | Cevap karışık politika/ürün listesi, yarıda kesilmiş; Incident Response etiketi uyumsuz. |
| `extra_20261108_672` | `EXCLUDE_FROM_TECHNICAL_QA` | Hayır | NIST yayın revizyonu meta-bilgisi; yanıt yarım ve teknik Q&A hedefiyle düşük uyumlu. |
| `extra_20261108_5801` | `REWRITE_QA_FROM_SOURCE` | Evet | Kaynakta açık olmayan ayrıntılı geçiş matrisi ve gelecekteki tehditlere kesin uyarlanma iddiası çıkarıldı. |
| `extra_20261108_1344` | `REWRITE_QA_FROM_SOURCE` | Evet | Kesilmiş saldırı adımları yerine kaynakta açıklanan mekanizma özetlendi. |
| `extra_20261108_5607` | `REWRITE_QA_FROM_SOURCE` | Evet | Kaynağın doğrudan desteklemediği erişim yetkisi aşımı iddiası çıkarıldı. |

## 6. Manuel onayın tamamlanması için işlem planı

1. **Kayıt örneklemesini genişlet:** En az 150–200 QA kaydını, her konu ve train/val/test bölümlerini temsil edecek şekilde bir kişi tarafından yeniden değerlendir. Öncelik: bugüne kadar tek tek incelenmemiş kayıtlar, Digital Forensics ve DevSecOps gibi düşük başarı gösteren konular.
2. **Kontrol ölçütlerini kayıtla:** (a) sorunun teknik ve anlaşılır olması; (b) yanıtın kaynakta desteklenmesi; (c) doğru/eksiksiz cevap; (d) uygun konu etiketi; (e) kopya ve aşırı yüzeysel soru olmaması; (f) zamana bağlı iddialarda yıl/sürüm belirtilmesi; (g) güvenli/etik bağlam.
3. **Kararı görünür kıl:** `UYGUN`, `DUZELT`, `CIKAR` kararına ek olarak gerekçe, kontrol eden, tarih, kaynak pasajı veya sayfa referansı ve varsa düzeltilmiş yanıtı kaydet. Bağımsız insan kontrolü yapılan kayıtlarda `verified` alanını ancak gerçekten onaylandığında `true` yap.
4. **Düzeltmeleri veri setine uygula:** İnceleme sonuçları değişirse train/val/test dosyalarını aynı belge-bazlı split mantığıyla yeniden üret ve sayıları yeniden raporla; mevcut 2.448/326/301 dağılımını otomatik olarak güncel kabul etme.
5. **Corpus kontrolünü ayrı tamamla:** 9.554 chunk içindeki 246 otomatik işaretli kaydı ve 65 yakın-benzerlik çiftini gözden geçir; corpus için 100–200 parçalık bağımsız örneklem kontrolü henüz tamamlanmamıştır.

## 7. Sınırlılıklar

- 60’lık örneklem her konudan beş kayıt seçildiğinden rastgele-temsili bir örneklem değildir. 27/60 uygun oranı genel veri setinin başarı oranı olarak sunulamaz.
- Kaynak pasajı bir PDF veya makaleden eksik/bozuk çıkarılmış olabilir. Dış kaynak doğrulaması, güncel teknik standart doğrulaması ve telif/lisans incelemesi bu denetimin kapsamında değildir.
- Güncel 3.075 QA kaydının tamamı kaynak metinle tek tek bağımsız doğrulanmamıştır; model inceleme etiketleri yalnızca ön-elemedir.
- Corpus ve QA için alan dışı tekrarlar, benzer belgeler arasındaki sızıntı, görev türü etiketleri ve gerçek tokenizer istatistikleri ayrı iş kalemleridir.

## 8. Dayanak dosyalar

- `reports/instruction/qa_28_oncelikli_inceleme_raporu.md` — 28 kayıt için karar ve gerekçeler.
- `reports/instruction/qa_28_elle_inceleme_kararlari.jsonl` — 28 kayıt için makine-okunur inceleme listesi.
- `reports/instruction/qa_13_teknik_kapsam_disi.jsonl` — öncelikli turdaki 13 kapsam dışı kayıt.
- `kalite_orneklem_60_degerlendirme.jsonl` ve `kalite_orneklem_60_rapor.md` — bu raporun hazırlanmasında kullanılan, mevcut projeye henüz kopyalandığı doğrulanmamış önceki inceleme kayıtları.
- `data/final/instruction_dataset_3075_aday.jsonl` — güncel QA adayı.
- `reports/VERI_SETI_ISTATISTIK_RAPORU.md` — corpus/QA sayısal ölçüm raporu.

**Sonuç:** Teknik QA üretimi ve iki ayrı turdaki kaynak-temelli ön denetim belgelenmiştir. Ancak **nihai manuel kalite güvencesi henüz tamamlanmamıştır**; bu nedenle dosyalar hâlen *aday* olarak etiketlenmelidir.
