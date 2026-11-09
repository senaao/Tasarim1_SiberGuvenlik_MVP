# Kaynak-gruplu yeniden bolme: ADAY raporu

> Bu yeni aday dosyalar veri sizintisi riskini azaltmak icin uretilmistir. Eski dosyalara dokunulmamistir.

- Corpus: 9554 metin parcasi; Instruction: 3075 soru-cevap (kayit silinmedi).
- Kaynak belge: 731; baglantili kaynak grubu: 715.
- Tespit edilen benzer metin cifti: 63.
- Tespit edilen cross-split cift: once 20, yeni adayda 0.
- Yeni bolmeye gecen kaynak: 8; corpus parcasi: 199; instruction sorusu: 64.

## Eski -> Yeni kayit sayilari

| Veri | Bolme | Eski | Yeni |
|---|---|---:|---:|
| Corpus | train | 7702 | 7643 |
| Corpus | val | 980 | 1059 |
| Corpus | test | 872 | 852 |
| Instruction | train | 2448 | 2418 |
| Instruction | val | 326 | 359 |
| Instruction | test | 301 | 298 |

## Degisen kaynaklar

| Kaynak belge | Eski bolme | Yeni bolme | Corpus parcasi | Instruction sorusu |
|---|---|---|---:|---:|
| A Security Analysis of Verifiable Credential Verification Pi.txt | test | val | 4 | 2 |
| BTK Akademi_Siber Güvenliğe Giriş_Atıl Samancıoğlu.txt | test | train | 12 | 2 |
| Computer Security Division 2012 Annual Report.txt | test | train | 42 | 11 |
| Computer Security Division 2014 Annual Report.txt | train | test | 52 | 15 |
| Enhanced Security Requirements for Protecting Controlled Unclassified Information_ A Supplement to NIST Special Publication 800-171.txt | train | val | 32 | 12 |
| NIST.SP.800-162.txt | train | val | 41 | 18 |
| NIST.SP.800-172.txt | train | val | 2 | 1 |
| OWASP_Application_Security_Verification_Standard_5.0.0_en.txt | test | train | 14 | 3 |

## Yontem ve sinirlar

- Benzer metin raporundaki kaynaklar baglantili bilesenlerde birlestirildi; her bilesen tek bolmeye atandi.
- Mümkün oldugunca mevcut bolmeler korundu; buyuklukler yeni adayda farkli olabilir.
- 63 aday cift icin cross-split kalmadi; ancak bu, tum olasi metin sizintilarinin temizlendigi anlamina gelmez.
- Bazi ciftler gercek kopya degil, farkli yayinlarin ortak pasajlari olabilir. Konservatif olarak ayni splitte tutuldu.
- Icerik ve kayit IDleri degistirilmedi; sadece split alanlari ve bolme dosyalari yeniden yazildi.
- Kaynak lisanslari, anlamsal dogruluk ve ek near-duplicate esikleri ayri kontrol gerektirir.
- Eski 08_validate_datasets.py, ESKI ayrimin sabit sayilarini kontrol eder; yeni aday icin kullanilmamalidir.
- Yeni aday kontrolu icin bu script icinde sayilar, kaynak uyumu, tam ID kapsami ve tespit edilmis ciftlerin ayrimi dogrulandi.
