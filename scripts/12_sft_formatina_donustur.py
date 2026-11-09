"""Siber guvenlik Instruction verisini SFT `messages` bicimine donustur.

Kullanim (VS Code proje ana klasoru):
    python scripts/12_sft_formatina_donustur.py

* `data/final/guvenli_split_aday` altindaki dogrulanmis aday bolmeleri okur.
* Kaynak bazli bolme, ID, bolme sayilari ve tam dosya tutarliligini tekrar denetler.
* Soru/cevap metnini degistirmeden SFT mesajlarina donusturur.
* `verified` alanini False olarak korur. MODEL_PASS insan onayi DEGILDIR.
* Eski dosyalari silmez, tasimaz veya degistirmez.
* Var olan farkli ciktilarin uzerine yazmaz. Ayni cikti varsa tekrar calismasi guvenlidir.
* Yalnizca Python standart kutuphanesini kullanir.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'data' / 'final' / 'guvenli_split_aday'
DEST = ROOT / 'data' / 'final' / 'sft_aday'
REPORT = ROOT / 'reports' / 'instruction' / 'SFT_DONUSUM_KONTROL_RAPORU.md'
SPLITS = ('train', 'val', 'test')
CORPUS_COUNTS = {'train': 7643, 'val': 1059, 'test': 852}
QA_COUNTS = {'train': 2418, 'val': 359, 'test': 298}

# Bazı uretilmis kayitlarda ek `{QUESTION}` / `{ANSWER}` satirlari var.
# Gercek `Question:` ve `Answer:` etiketlerinden soru-cevap parcasi alinir.
QA_PATTERN = re.compile(
    r'(?is)(?:^|\n)\s*Question\s*:\s*(.*?)\s*(?:\{ANSWER\}\s*)?'
    r'(?:^|\n)\s*Answer\s*:\s*(.*?)\s*\Z'
)


def demand(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def read_jsonl(path: Path) -> list[dict]:
    demand(path.is_file(), f'Dosya bulunamadi: {path}')
    result: list[dict] = []
    with path.open('r', encoding='utf-8-sig') as file:
        for line_no, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f'Gecersiz JSONL: {path}, satir {line_no}: {error}') from error
            demand(isinstance(row, dict), f'JSON nesnesi bekleniyordu: {path}:{line_no}')
            result.append(row)
    return result


def to_qa(output: str, rid: str) -> tuple[str, str]:
    demand(isinstance(output, str), f'{rid}: output metin degil')
    match = QA_PATTERN.search(output)
    demand(match is not None, f'{rid}: Question/Answer ayrilamadi, donusum durduruldu')
    question, answer = match.group(1).strip(), match.group(2).strip()
    demand(bool(question and answer), f'{rid}: bos soru ya da yanit')
    return question, answer


def write_if_new_or_same(path: Path, contents: str) -> str:
    if path.exists():
        demand(path.is_file(), f'Cikti yolunda dosya yerine klasor var: {path}')
        demand(path.read_text(encoding='utf-8-sig') == contents,
               f'Bu isimle farkli bir dosya zaten var; uzerine yazilmadi: {path}')
        return 'zaten vardi, ayni icerik'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding='utf-8', newline='\n')
    return 'olusturuldu'


def as_jsonl(rows: list[dict]) -> str:
    return ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows)


def main() -> None:
    corpus_ids: set[str] = set()
    qa_ids: set[str] = set()
    corpus_src_splits: dict[str, str] = {}
    qa_src_splits: dict[str, str] = {}
    qa_full_by_id: dict[str, dict] = {}

    full_path = SOURCE / 'instruction_dataset_3075_resplit_aday.jsonl'
    for row in read_jsonl(full_path):
        rid = row.get('id')
        demand(isinstance(rid, str) and bool(rid), 'Tam QA dosyasinda bos ID')
        demand(rid not in qa_full_by_id, f'Tam QA dosyasinda tekrar eden ID: {rid}')
        qa_full_by_id[rid] = row
    demand(len(qa_full_by_id) == 3075,
           f'Tam QA kayit sayisi beklenen 3075 degil: {len(qa_full_by_id)}')

    # Butun kontroller tamamlanana kadar hicbir yeni dosya olusturma.
    converted: dict[str, list[dict]] = {}
    topics: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    verified_counts: Counter[str] = Counter()

    for split in SPLITS:
        cr_path = SOURCE / 'corpus' / f'domain_corpus_{split}.jsonl'
        cr_rows = read_jsonl(cr_path)
        demand(len(cr_rows) == CORPUS_COUNTS[split],
               f'Corpus/{split}: {len(cr_rows)} kayit, beklenen {CORPUS_COUNTS[split]}')
        for row in cr_rows:
            rid, src = row.get('id'), row.get('source_document')
            demand(isinstance(rid, str) and rid and rid not in corpus_ids,
                   f'Corpus: gecersiz veya tekrar ID: {rid}')
            demand(isinstance(src, str) and src, f'Corpus kaynak bos: {rid}')
            demand(row.get('split') == split, f'Corpus split alani uyusmuyor: {rid}')
            demand(src not in corpus_src_splits or corpus_src_splits[src] == split,
                   f'Corpus kaynagi farkli bolmelerde: {src}')
            corpus_ids.add(rid)
            corpus_src_splits[src] = split

    demand(len(corpus_ids) == 9554, 'Corpus toplam 9554 degil')

    for split in SPLITS:
        rows = read_jsonl(SOURCE / 'instruction' / f'{split}.jsonl')
        demand(len(rows) == QA_COUNTS[split],
               f'Instruction/{split}: {len(rows)} kayit, beklenen {QA_COUNTS[split]}')
        output_rows: list[dict] = []
        for row in rows:
            rid, src = row.get('id'), row.get('source_document')
            demand(isinstance(rid, str) and rid and rid not in qa_ids,
                   f'Instruction: gecersiz veya tekrar ID: {rid}')
            demand(isinstance(src, str) and src, f'Instruction kaynak bos: {rid}')
            demand(row.get('split') == split, f'Instruction split uyusmuyor: {rid}')
            demand(rid in qa_full_by_id and row == qa_full_by_id[rid],
                   f'QA split ve tam dosya farkli: {rid}')
            demand(corpus_src_splits.get(src) == split,
                   f'Corpus/Instruction kaynak bolmesi eslesmiyor: {rid} -> {src}')
            demand(src not in qa_src_splits or qa_src_splits[src] == split,
                   f'QA kaynagi birden cok bolmede: {src}')
            question, answer = to_qa(row.get('output'), rid)
            topic = row.get('topic')
            demand(isinstance(topic, str) and topic.strip(), f'Konu etiketi bos: {rid}')
            verified = row.get('verified')
            demand(isinstance(verified, bool), f'verified bool degil: {rid}')

            # Ilk asamada yalnizca SFT yapisi: 2 rol, karsilikli metin.
            # Topic bir KONU etiketidir; 'gorev turu' olarak yeniden isimlendirilmez.
            output_rows.append({
                'id': rid,
                'source_document': src,
                'topic': topic,
                'verified': verified,
                'review_status': row.get('review_status'),
                'messages': [
                    {'role': 'user', 'content': question},
                    {'role': 'assistant', 'content': answer},
                ],
            })
            qa_ids.add(rid)
            qa_src_splits[src] = split
            topics[topic] += 1
            statuses[str(row.get('review_status'))] += 1
            verified_counts[str(verified)] += 1
        converted[split] = output_rows

    demand(qa_ids == set(qa_full_by_id),
           'Tam 3075 QA kaydi ile train/val/test ID kumesi uyusmuyor')
    demand(len(corpus_src_splits) == 731, f'Corpus kaynak sayisi beklenenden farkli: {len(corpus_src_splits)}')
    demand(len(qa_src_splits) == 562, f'QA kaynak sayisi beklenenden farkli: {len(qa_src_splits)}')

    lines = [
        '# SFT adayi: donusum ve bagimsiz kontrol raporu',
        '',
        'Bu rapor teknik bicim donusumunu denetler; insan tarafindan yanit dogrulamasini KAPSAMAZ.',
        '',
        '| Bolme | Corpus parcasi | Soru-cevap / SFT kaydi |',
        '|---|---:|---:|',
    ]
    for sp in SPLITS:
        lines.append(f'| {sp} | {CORPUS_COUNTS[sp]:,} | {len(converted[sp]):,} |')
    lines.extend([
        f'| **Toplam** | **{sum(CORPUS_COUNTS.values()):,}** | **{len(qa_ids):,}** |',
        '',
        f'- Corpus kaynak belgesi: **{len(corpus_src_splits)}**.',
        f'- Soru-cevap kaynagi: **{len(qa_src_splits)}**.',
        '- Tum QA IDleri ve source_document alanlari korundu.',
        '- Kaynak bazli bolmeler corpus ile eslesiyor; test/validation arasi ayni kaynak bulunmadi.',
        '- Yalnizca `Question:` ve `Answer:` isaretleri cikarildi; soru/yanit kelimeleri yeniden yazilmadi.',
        '- SFT bicimi: `messages`: `user` ve `assistant`. Basit egitim araclari icin ek metadata alanlari secilebilir.',
        '- Konu (`topic`) etiketi korunmustur. Ayrica **gorev turu etiketi uretilmemistir**.',
        '- Tum orijinal kayitlar ve eski bolmeler oldugu gibi kalmistir.',
        '',
        '## Degerlendirme sinirlari',
        '',
        f'- Insan dogrulamasi (`verified=True`): **{verified_counts.get("True", 0)} / {len(qa_ids)}**.',
        f'- `MODEL_PASS`: **{statuses.get("MODEL_PASS", 0)} / {len(qa_ids)}**; bu, uzman denetimi anlamina gelmez.',
        '- Yanlis/eksik teknik yanitlar, kaynak lisansi ve daha fazla anlamsal tekrar olasiligi bu donusumle giderilmez.',
        '- Bu ciktilar **SFT yapisina donusturulmus ADAYLAR** olarak sunulmalidir.',
        '',
        '## Konu dagilimi',
        '',
        '| Konu | Ornek |',
        '|---|---:|',
    ])
    lines.extend(f'| {topic} | {n} |' for topic, n in topics.most_common())
    report = '\n'.join(lines) + '\n'

    results = []
    for sp in SPLITS:
        dst = DEST / f'{sp}.jsonl'
        results.append((dst, write_if_new_or_same(dst, as_jsonl(converted[sp]))))
    results.append((REPORT, write_if_new_or_same(REPORT, report)))

    print('=== SFT ADAYI HAZIR ===')
    print('Kaynak belgesi: Corpus 731 | Instruction 562')
    print('Corpus:', CORPUS_COUNTS)
    print('Instruction/SFT:', {sp: len(converted[sp]) for sp in SPLITS})
    print('Soru/cevap ayristirma: 3075/3075')
    print(f'Insan onayli verified=True: {verified_counts.get("True", 0)}/{len(qa_ids)}')
    for dst, result in results:
        print(f'{result}: {dst.relative_to(ROOT)}')
    print('ESKI VERILER DEGISTIRILMEDI. Bu adim kalite denetiminin yerine gecmez.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('SFT DONUSUM HATASI:', exc, file=sys.stderr)
        sys.exit(1)
