"""Independently validate the leakage-reduced candidate Corpus/Instruction split.

Run from the project root: python scripts/10_validate_resplit.py
Only writes a text report; never changes dataset JSONL files.
"""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'final'
NEW = DATA / 'guvenli_split_aday'
SPLITS = ('train', 'val', 'test')
EXPECTED = {'corpus': (9554, (7643, 1059, 852)),
            'instruction': (3075, (2418, 359, 298))}
REPORT = ROOT / 'reports' / 'corpus' / 'YENI_SPLIT_DOGRULAMA_RAPORU.txt'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_jsonl(path):
    require(path.is_file(), f'Dosya bulunamadi: {path}')
    rows = []
    with path.open('r', encoding='utf-8-sig') as f:
        for lineno, line in enumerate(f, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f'JSON hatasi: {path}:{lineno} - {error}') from error
                require(isinstance(row, dict), f'Nesne olmayan kayit: {path}:{lineno}')
                rows.append(row)
    return rows


def indexed(rows, name):
    by_id = {}
    for row in rows:
        rid = row.get('id')
        require(isinstance(rid, str) and rid, f'{name}: gecersiz ID')
        require(rid not in by_id, f'{name}: tekrar eden ID: {rid}')
        require(isinstance(row.get('source_document'), str) and row['source_document'],
                f'{name}: eksik kaynak: {rid}')
        by_id[rid] = row
    return by_id


def without_split(row):
    return {key: value for key, value in row.items() if key != 'split'}


def validate_dataset(label, original_path, candidate_path, part_folder, filename):
    original = indexed(read_jsonl(original_path), f'{label} eski')
    candidate = indexed(read_jsonl(candidate_path), f'{label} yeni')
    full_expected, part_expected = EXPECTED[label]
    require(len(original) == len(candidate) == full_expected,
            f'{label}: tam dosyada kayit sayisi yanlis')
    require(original.keys() == candidate.keys(), f'{label}: eski ve yeni ID kumeleri farkli')
    for rid, new_row in candidate.items():
        require(without_split(original[rid]) == without_split(new_row),
                f'{label}: icerik veya metadata degismis: {rid}')
        require(new_row.get('split') in SPLITS, f'{label}: split eksik/gecersiz: {rid}')

    seen_ids = set()
    sources = defaultdict(set)
    counts = {}
    for split, expected in zip(SPLITS, part_expected):
        path = part_folder / filename(split)
        part = indexed(read_jsonl(path), f'{label} {split}')
        require(len(part) == expected,
                f'{label}/{split}: {len(part)} kayit, beklenen {expected}')
        for rid, row in part.items():
            require(rid in candidate, f'{label}/{split}: tam dosyada olmayan ID: {rid}')
            require(rid not in seen_ids, f'{label}: iki bolmede bulunan ID: {rid}')
            require(row == candidate[rid], f'{label}/{split}: tam dosyayla farkli satir: {rid}')
            require(row['split'] == split, f'{label}/{split}: kaydin split alani farkli: {rid}')
            seen_ids.add(rid)
            sources[row['source_document']].add(split)
        counts[split] = len(part)
    require(seen_ids == candidate.keys(), f'{label}: bolme dosyalari bazi kayitlari kapsamiyor')
    require(all(len(splits) == 1 for splits in sources.values()),
            f'{label}: ayni kaynak birden cok bolmede')
    return original, candidate, sources, counts


def main():
    old_c, new_c, c_sources, c_counts = validate_dataset(
        'corpus', DATA / 'domain_corpus_v1_aday.jsonl',
        NEW / 'domain_corpus_v1_resplit_aday.jsonl', NEW / 'corpus',
        lambda s: f'domain_corpus_{s}.jsonl')
    old_q, new_q, q_sources, q_counts = validate_dataset(
        'instruction', DATA / 'instruction_dataset_3075_aday.jsonl',
        NEW / 'instruction_dataset_3075_resplit_aday.jsonl', NEW / 'instruction',
        lambda s: f'{s}.jsonl')

    for source, splits in q_sources.items():
        require(source in c_sources, f'Instruction kaynagi Corpus icinde yok: {source}')
        require(splits == c_sources[source], f'Corpus-Instruction bolme eslesmiyor: {source}')

    pair_file = ROOT / 'reports' / 'corpus' / 'near_duplicate_pairs.csv'
    require(pair_file.is_file(), f'Benzerlik CSV bulunamadi: {pair_file}')
    with pair_file.open('r', encoding='utf-8-sig', newline='') as f:
        pairs = list(csv.DictReader(f))
    require(len(pairs) == 63, f'Beklenen 63 aday cift, bulunan {len(pairs)}')
    cross = 0
    for pair in pairs:
        a, b = pair.get('id_1'), pair.get('id_2')
        require(a in new_c and b in new_c, f'CSV icindeki ID bulunamadi: {a}, {b}')
        require(pair.get('source_document_1') == new_c[a]['source_document'] and
                pair.get('source_document_2') == new_c[b]['source_document'],
                f'CSV kaynak eslesmesi yanlis: {a}, {b}')
        cross += new_c[a]['split'] != new_c[b]['split']
    require(cross == 0, f'Bolmeler arasi {cross} benzer cift kaldi')

    changed_c = [rid for rid in new_c if old_c[rid].get('split') != new_c[rid]['split']]
    old_source_split = {row['source_document']: row['split'] for row in old_c.values()}
    changed_q = [rid for rid in new_q
                 if old_source_split[old_q[rid]['source_document']] != new_q[rid]['split']]
    changed_sources = {new_c[rid]['source_document'] for rid in changed_c}
    require((len(changed_sources), len(changed_c), len(changed_q)) == (8, 199, 64),
            'Tasinan kaynak/kayit sayilari on raporla uyusmuyor')

    lines = [
        '=== YENI SPLIT BAGIMSIZ TEKNIK KONTROLU ===',
        f'Corpus: {len(new_c)} | train={c_counts["train"]}, val={c_counts["val"]}, test={c_counts["test"]}',
        f'Instruction: {len(new_q)} | train={q_counts["train"]}, val={q_counts["val"]}, test={q_counts["test"]}',
        'Tum IDler korundu: OK',
        'Eski ve yeni veri icerigi (split haric) ayni: OK',
        'Bolme dosyalari ve tam dosyalar eslesiyor: OK',
        'Kaynak bazli bolme ve Corpus-Instruction eslesmesi: OK',
        f'Tespit edilen {len(pairs)} benzer ciftten bolmeler arasi kalan: {cross}',
        f'Tasinan kaynak: {len(changed_sources)} | Corpus parcasi: {len(changed_c)} | Soru: {len(changed_q)}',
        'SONUC: BAGIMSIZ TEKNIK KONTROL GECTI',
        'Sinir: Anlamsal dogruluk, lisanslar ve tespit edilmeyen olasi benzerlikler kontrol edilmedi.',
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines))
    print('Rapor:', REPORT.relative_to(ROOT))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print('DOGRULAMA HATASI:', error, file=sys.stderr)
        sys.exit(1)
