"""180 soruluk model on incelemesindeki 12 kritik QA adayini SFT'den AYRI tutar.

VS Code proje kokunden:
    python scripts/14_kritik_12_ayir.py

- Orijinal 3075 QA / SFT veri setini ASLA degistirmez.
- Yalnizca ELE_ADAYI etiketli 12 kaydi yeni bir KARANTINA dosyasina alir.
- Kalan 3063 kaydi AYRI, gecici bir SFT aday setine yazar.
- Model kararlari insan onayi sayilmaz. Kalan 3063 kaydin dogrulugu onaylanmaz.
- Kaynak bazli train/val/test bolmeleri aynen korunur.
- Sadece Python standart kutuphanesi kullanilir.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / 'reports' / 'instruction' / 'QA_MODEL_ON_INCELEME_180.csv'
SFT = ROOT / 'data' / 'final' / 'sft_aday'
OUT = ROOT / 'data' / 'final' / 'sft_kritik_12_ayrilmis_aday'
REPORT = ROOT / 'reports' / 'instruction' / 'KRITIK_12_AYIRMA_KONTROL_RAPORU.md'
SPLITS = ('train', 'val', 'test')
EXPECTED = {'train': 2418, 'val': 359, 'test': 298}
CRITICAL = 'ELE_ADAYI'


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise ValueError(detail)


def load_review(path: Path) -> list[dict]:
    require(path.is_file(), f'Inceleme CSV bulunamadi: {path}')
    with path.open('r', encoding='utf-8-sig', newline='') as fh:
        reader = csv.reader(fh)
        header = next(reader, [])
        # Onceki dosyada ayni alti model kolonu iki kere yer almaktadir.
        # Onlari yok saymak yerine esit olduklarini denetliyoruz.
        core = ['sira', 'id', 'bolme', 'konu', 'kaynak_belge', 'soru',
                'cevap', 'kaynak_pasaji', 'insan_karari', 'inceleyen',
                'inceleme_tarihi', 'inceleme_notu']
        model = ['model_on_degerlendirme', 'model_oncelik', 'model_gerekce',
                 'model_onerilen_konu', 'model_kaynak_kelime_ortusmesi',
                 'model_kanit_penceresi']
        require(header == core + model + model,
                'CSV basliklari beklenenden farkli. QA_MODEL_ON_INCELEME_180.csv dosyasini kontrol et.')
        result: list[dict] = []
        for line_no, cells in enumerate(reader, 2):
            require(len(cells) == len(header), f'CSV {line_no}: kolon sayisi hatali')
            require(cells[12:18] == cells[18:24],
                    f'CSV {line_no}: iki model degerlendirme sutunu uyusmuyor')
            result.append(dict(zip(core + model, cells[:18])))
    require(len(result) == 180, f'Orneklem 180 olmali: {len(result)}')
    require(len({r['id'] for r in result}) == 180, 'Inceleme CSV dosyasinda tekrar eden ID var')
    require(all(r['bolme'] in SPLITS for r in result), 'Gecersiz bolme etiketi')
    return result


def read_jsonl(path: Path) -> list[dict]:
    require(path.is_file(), f'SFT veri dosyasi yok: {path}')
    with path.open('r', encoding='utf-8-sig') as fh:
        result = []
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            require(isinstance(row, dict), f'JSONL nesnesi gecersiz: {path}:{line_no}')
            result.append(row)
    return result


def safe_write(path: Path, text: str) -> str:
    if path.exists():
        require(path.is_file(), f'Cikti dosya degil: {path}')
        require(path.read_text(encoding='utf-8-sig') == text,
                f'Var olan farkli veya duzenlenmis dosya UZERINE YAZILMADI: {path}')
        return 'zaten mevcut, ayni icerik'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')
    return 'yeni olusturuldu'


def encode(rows: list[dict]) -> str:
    return ''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows)


def main() -> None:
    review = load_review(REVIEW)
    classes = Counter(r['model_on_degerlendirme'] for r in review)
    require(classes[CRITICAL] == 12,
            f'Beklenen 12 ELE_ADAYI yerine {classes[CRITICAL]} tespit edildi')
    review_by_id = {r['id']: r for r in review}
    per_split: dict[str, list[dict]] = {}
    quarantine: list[dict] = []
    all_ids: set[str] = set()
    found_review: set[str] = set()
    split_counts = Counter()

    # Veri okunup tamamen dogrulanmadan cikti uretme.
    for split in SPLITS:
        rows = read_jsonl(SFT / f'{split}.jsonl')
        require(len(rows) == EXPECTED[split],
                f'{split}: {EXPECTED[split]} bekleniyordu, {len(rows)} bulundu')
        kept: list[dict] = []
        for row in rows:
            rid = row.get('id')
            require(isinstance(rid, str) and rid and rid not in all_ids,
                    f'Bosluga veya tekrara dusen ID: {rid}')
            all_ids.add(rid)
            r = review_by_id.get(rid)
            if r is None:
                kept.append(row)
                continue
            found_review.add(rid)
            messages = row.get('messages')
            require(isinstance(messages, list) and len(messages) == 2,
                    f'SFT messages alani hatali: {rid}')
            require(
                r['bolme'] == split and r['konu'] == row.get('topic') and
                r['kaynak_belge'] == row.get('source_document') and
                messages[0].get('role') == 'user' and
                messages[1].get('role') == 'assistant' and
                messages[0].get('content') == r['soru'] and
                messages[1].get('content') == r['cevap'],
                f'Inceleme CSV ile SFT farkli: {rid}'
            )
            if r['model_on_degerlendirme'] == CRITICAL:
                # Orijinal SFT kaydini iceriyle sakla; inceleme notunu yaninda tut.
                quarantine.append({
                    'sira': int(r['sira']),
                    'split': split,
                    'model_on_degerlendirme': r['model_on_degerlendirme'],
                    'model_gerekce': r['model_gerekce'],
                    'insan_karari': r['insan_karari'],
                    'review_note': 'MODEL ON INCELEMESI - HENUZ INSAN ONAYI YOK',
                    'record': row,
                })
                split_counts[split] += 1
            else:
                kept.append(row)
        per_split[split] = kept

    require(len(all_ids) == 3075, f'SFT toplam 3075 degil: {len(all_ids)}')
    require(found_review == set(review_by_id), 'Incelenen 180 sorunun bazilari SFTde yok')
    require(len(quarantine) == 12, 'Karantina 12 kayit olmali')
    require(sum(len(rows) for rows in per_split.values()) == 3063,
            'Ayrilmis SFT aday toplam sayisi 3063 olmali')
    require(len({r['record']['id'] for r in quarantine}) == 12,
            'Karantinada tekrar ID mevcut')
    quarantine.sort(key=lambda r: r['sira'])

    report = [
        '# SFT kritik 12 kayit: ayirma ve izlenebilirlik raporu',
        '',
        '**Durum:** Otomatik ON ELEME / KARANTINA; uzman veya insan nihai karari DEGIL.',
        '',
        '180 soruluk incelemeden ELE_ADAYI etiketi alan 12 SFT kaydi, ',
        'yeni gecici SFT aday dosyalarindan AYRI tutuldu. Diger 168 orneklem',
        'kaydi dahil kalan butun sorular onaylanmis kabul EDILMEMELIDIR.',
        'Orijinal 3.075 QA ve SFT veri dosyalari degistirilmedi.',
        '',
        '| Bolme | Onceki SFT | Karantina | Gecici SFT adayi |',
        '|---|---:|---:|---:|',
    ]
    for split in SPLITS:
        report.append(
            f'| {split} | {EXPECTED[split]} | {split_counts[split]} | {len(per_split[split])} |'
        )
    report += [
        '| **Toplam** | **3075** | **12** | **3063** |',
        '',
        '## Kritik 12 kayit - gerekceler',
        '',
        '| Orneklem sirasi | ID | Modelin gerekcesi |',
        '|---:|---|---|',
    ]
    for r in quarantine:
        reason = r['model_gerekce'].replace('|', '\\|').replace('\n', ' ')
        report.append(f'| {r["sira"]} | `{r["record"]["id"]}` | {reason} |')
    report += [
        '',
        '## Diger bekleyen kontroller',
        '',
        f'- Toplam orneklem: 180; otomatik siniflar: {dict(classes)}.',
        '- 25 alan-disi adayi, 18 duzeltme adayi, 33 yanlis konu adayi ve diger',
        '  kayitlar bu adimda SILINMEDI veya DUZELTILMEDI. Sonraki denetime kaldi.',
        '- Kalan 3.063 SFT ornegi **insan dogrulamasi yapilmis temiz set degildir**.',
        '- Kaynak belgeler, ID ve train/val/test atamalari ayni kalmistir.',
        '- Ana SFT teslimini degistirmek icin tum kontrol kararlarini ve surumlemeyi tamamla.',
        '',
    ]

    outputs = []
    for split in SPLITS:
        path = OUT / f'{split}.jsonl'
        outputs.append((path, safe_write(path, encode(per_split[split]))))
    path = OUT / 'kritik_12_karantina.jsonl'
    outputs.append((path, safe_write(path, encode(quarantine))))
    outputs.append((REPORT, safe_write(REPORT, '\n'.join(report))))

    print('=== KRITIK 12 AYIRMA TAMAMLANDI ===')
    print('Orijinal SFT: 3075 (degismedi)')
    print('Kontrol edilen orneklem: 180')
    print('Karantinaya ayrilan kritik aday: 12', dict(split_counts))
    print('Gecici SFT adayi: 3063', {split: len(per_split[split]) for split in SPLITS})
    for output, status in outputs:
        print(f'{status}: {output.relative_to(ROOT)}')
    print('NOT: Bu islem insan onayi ve tum veri setinin kalite kontrolu DEGILDIR.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print('KRITIK 12 AYIRMA HATASI:', exc, file=sys.stderr)
        sys.exit(1)
