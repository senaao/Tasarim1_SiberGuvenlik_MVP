"""Siber guvenlik Instruction Dataset icin 180 kayitlik inceleme orneklemi.

Kullanim (VS Code, proje ana klasorunde):
    python scripts/13_qa_kalite_orneklemi_hazirla.py

- 12 konudan 15'er soru secer (her konuda train 10 / val 3 / test 2).
- Mevcut QA ve SFT donusumu arasindaki kimlik, kaynak ve mesaj eslesmesini kontrol eder.
- Kaynak belgesi cesitliligine oncelik verir, secim deterministiktir.
- Soru, yanit ve orijinal kaynak pasajini *birlikte* CSV'ye koyar.
- Inceleme sonucunu ve insan onayini BOS birakir. Kontrol yapilmis gibi davranmaz.
- Eski veri setlerini DEGISTIRMEZ.
- Sadece Python standart kutuphanesini kullanir.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'data' / 'final' / 'guvenli_split_aday' / 'instruction'
SFT = ROOT / 'data' / 'final' / 'sft_aday'
OUT = ROOT / 'reports' / 'instruction' / 'QA_KALITE_INCELEME_ORNEKLEMI_180.csv'
SPLITS = ('train', 'val', 'test')
COUNTS = {'train': 2418, 'val': 359, 'test': 298}
TARGET_PER_TOPIC = {'train': 10, 'val': 3, 'test': 2}
QA_PATTERN = re.compile(
    r'(?is)(?:^|\n)\s*Question\s*:\s*(.*?)\s*(?:\{ANSWER\}\s*)?'
    r'(?:^|\n)\s*Answer\s*:\s*(.*?)\s*\Z'
)
COLUMNS = [
    'sira', 'id', 'bolme', 'konu', 'kaynak_belge',
    'soru', 'cevap', 'kaynak_pasaji',
    'insan_karari', 'inceleyen', 'inceleme_tarihi', 'inceleme_notu'
]


def need(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def load_jsonl(path: Path) -> list[dict]:
    need(path.is_file(), f'Dosya bulunamadi: {path}')
    rows = []
    with path.open('r', encoding='utf-8-sig') as stream:
        for n, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f'Gecersiz JSON satiri: {path}:{n}: {exc}') from exc
            need(isinstance(row, dict), f'JSON nesnesi degil: {path}:{n}')
            rows.append(row)
    return rows


def parse_qa(text: str, rid: str) -> tuple[str, str]:
    need(isinstance(text, str), f'Gecersiz output: {rid}')
    found = QA_PATTERN.search(text)
    need(found is not None, f'Soru-cevap ayrilamiyor: {rid}')
    question, answer = found.group(1).strip(), found.group(2).strip()
    need(bool(question and answer), f'Bos soru/cevap: {rid}')
    return question, answer


def ordered_candidates(rows: list[dict]) -> list[dict]:
    # Sabit hash sirasi: bilgisayar/oturum fark etmeden ayni kayitlari secer.
    return sorted(rows, key=lambda r: hashlib.sha256(
        ('siber-vize-kalite-orneklem-v1|' + r['id']).encode('utf-8')
    ).hexdigest())


def pick_diverse(rows: list[dict], n: int, used_sources: set[str]) -> list[dict]:
    selected = []
    used_ids = set()
    ordered = ordered_candidates(rows)
    for item in ordered:
        if len(selected) >= n:
            break
        if item['source_document'] not in used_sources:
            selected.append(item)
            used_ids.add(item['id'])
            used_sources.add(item['source_document'])
    for item in ordered:
        if len(selected) >= n:
            break
        if item['id'] not in used_ids:
            selected.append(item)
            used_sources.add(item['source_document'])
    need(len(selected) == n, 'Yeterli cesitlilikte ornek bulunamadi')
    return selected


def main() -> None:
    grouped = defaultdict(list)
    all_ids = set()
    all_topics = set()
    for split in SPLITS:
        originals = load_jsonl(SRC / f'{split}.jsonl')
        sft_rows = load_jsonl(SFT / f'{split}.jsonl')
        need(len(originals) == COUNTS[split],
             f'{split}: {len(originals)} orijinal QA beklenen {COUNTS[split]} degil')
        need(len(sft_rows) == COUNTS[split],
             f'{split}: {len(sft_rows)} SFT QA beklenen {COUNTS[split]} degil')
        sft_by_id = {item.get('id'): item for item in sft_rows}
        need(len(sft_by_id) == len(sft_rows), f'{split}: SFT ID tekrari var')
        for item in originals:
            rid = item.get('id')
            need(isinstance(rid, str) and rid and rid not in all_ids,
                 f'Tekrar veya bos ID: {rid}')
            need(item.get('split') == split, f'Bolme etiketi hatali: {rid}')
            topic = item.get('topic')
            source = item.get('source_document')
            need(isinstance(topic, str) and topic and isinstance(source, str) and source,
                 f'Konu veya kaynak eksik: {rid}')
            question, answer = parse_qa(item.get('output'), rid)
            sft = sft_by_id.get(rid)
            need(isinstance(sft, dict), f'SFT karsiligi eksik: {rid}')
            messages = sft.get('messages')
            need(isinstance(messages, list) and len(messages) == 2 and
                 messages[0].get('role') == 'user' and
                 messages[1].get('role') == 'assistant' and
                 messages[0].get('content') == question and
                 messages[1].get('content') == answer and
                 sft.get('source_document') == source and sft.get('topic') == topic,
                 f'Orijinal ile SFT eslesmiyor: {rid}')
            item['_question'], item['_answer'] = question, answer
            grouped[(topic, split)].append(item)
            all_ids.add(rid)
            all_topics.add(topic)
    need(len(all_ids) == 3075, f'Toplam QA 3075 degil: {len(all_ids)}')
    need(len(all_topics) == 12, f'Konu sayisi 12 degil: {len(all_topics)}')

    sampled = []
    used_sources = set()
    for topic in sorted(all_topics):
        for split in SPLITS:
            candidates = grouped[(topic, split)]
            number = TARGET_PER_TOPIC[split]
            need(len(candidates) >= number,
                 f'{topic}/{split}: {len(candidates)} soru, en az {number} gerekli')
            sampled.extend(pick_diverse(candidates, number, used_sources))
    need(len(sampled) == 180 and len({r['id'] for r in sampled}) == 180,
         'Orneklem 180 tekil kayit olmadi')

    out_rows = []
    for idx, item in enumerate(sampled, 1):
        excerpt = item.get('source_text')
        need(isinstance(excerpt, str) and excerpt.strip(),
             f'Kaynak metni bos: {item["id"]}')
        out_rows.append({
            'sira': idx,
            'id': item['id'],
            'bolme': item['split'],
            'konu': item['topic'],
            'kaynak_belge': item['source_document'],
            'soru': item['_question'],
            'cevap': item['_answer'],
            'kaynak_pasaji': excerpt,
            'insan_karari': '',
            'inceleyen': '',
            'inceleme_tarihi': '',
            'inceleme_notu': '',
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Aynisini tekrar calistirmak guvenli; elde doldurulmus inceleme dosyasini asla ezme.
    if OUT.exists():
        with OUT.open('r', encoding='utf-8-sig', newline='') as stream:
            existing = list(csv.DictReader(stream))
        expected = [{k: str(v) for k, v in r.items()} for r in out_rows]
        need(existing == expected,
             f'Var olan farkli/doldurulmus dosyanin uzerine yazilmadi: {OUT}')
        status = 'Ayni orneklem zaten olusturulmus'
    else:
        with OUT.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(out_rows)
        status = 'Yeni kalite orneklemi olusturuldu'

    print('=== QA KALITE KONTROL ORNEKLEMI HAZIR ===')
    print('Kontrol edilen QA/SFT kaydi: 3075/3075')
    print('Orneklem: 180 soru, 12 konu x 15 soru')
    print('Bolme dagilimi:', dict(Counter(r['bolme'] for r in out_rows)))
    print('Farkli kaynak:', len({r['kaynak_belge'] for r in out_rows}))
    print('Insan kalite kararlari: BOS (henüz degerlendirilmedi)')
    print(status + ':', OUT.relative_to(ROOT))
    print('Ana veri setleri degistirilmedi; orneklem kalite onayi anlamina gelmez.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print('QA ORNEKLEM HATASI:', error, file=sys.stderr)
        sys.exit(1)
