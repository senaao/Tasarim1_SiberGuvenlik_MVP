# SFT adayi: donusum ve bagimsiz kontrol raporu

Bu rapor teknik bicim donusumunu denetler; insan tarafindan yanit dogrulamasini KAPSAMAZ.

| Bolme | Corpus parcasi | Soru-cevap / SFT kaydi |
|---|---:|---:|
| train | 7,643 | 2,418 |
| val | 1,059 | 359 |
| test | 852 | 298 |
| **Toplam** | **9,554** | **3,075** |

- Corpus kaynak belgesi: **731**.
- Soru-cevap kaynagi: **562**.
- Tum QA IDleri ve source_document alanlari korundu.
- Kaynak bazli bolmeler corpus ile eslesiyor; test/validation arasi ayni kaynak bulunmadi.
- Yalnizca `Question:` ve `Answer:` isaretleri cikarildi; soru/yanit kelimeleri yeniden yazilmadi.
- SFT bicimi: `messages`: `user` ve `assistant`. Basit egitim araclari icin ek metadata alanlari secilebilir.
- Konu (`topic`) etiketi korunmustur. Ayrica **gorev turu etiketi uretilmemistir**.
- Tum orijinal kayitlar ve eski bolmeler oldugu gibi kalmistir.

## Degerlendirme sinirlari

- Insan dogrulamasi (`verified=True`): **0 / 3075**.
- `MODEL_PASS`: **3075 / 3075**; bu, uzman denetimi anlamina gelmez.
- Yanlis/eksik teknik yanitlar, kaynak lisansi ve daha fazla anlamsal tekrar olasiligi bu donusumle giderilmez.
- Bu ciktilar **SFT yapisina donusturulmus ADAYLAR** olarak sunulmalidir.

## Konu dagilimi

| Konu | Ornek |
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
