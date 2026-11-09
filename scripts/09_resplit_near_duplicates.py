"""Build a conservative, leakage-reduced *candidate* split of both datasets.

Run from any directory: python scripts/09_resplit_near_duplicates.py

- Reads the existing complete corpus, complete instruction set, current splits,
  and reports/corpus/near_duplicate_pairs.csv.
- Keeps every record and its text unchanged; changes only split assignment.
- Groups every pair of source documents linked by detected near-duplicate
  chunks (even if similarity may be legitimate), as a conservative precaution.
- Places connected source groups entirely in one train/val/test partition.
- Writes new candidate datasets to data/final/guvenli_split_aday/ and a report
  to reports/corpus/. Does not overwrite or delete existing data.
- A detected-pairs check is NOT proof of full semantic deduplication.

Requires only Python standard library. Intended for the existing Windows VS Code project.
"""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'final'
REPORTS = ROOT / 'reports' / 'corpus'
PAIRS = REPORTS / 'near_duplicate_pairs.csv'
OUTPUT = DATA / 'guvenli_split_aday'
REPORT = REPORTS / 'GUvenli_split_on_raporu.md'
SPLITS = ('train', 'val', 'test')


def load(path):
    if not path.is_file():
        raise RuntimeError(f'Dosya bulunamadi: {path}')
    rows = []
    with path.open(encoding='utf-8-sig') as handle:
        for i, line in enumerate(handle, 1):
            if line.strip():
                try:
                    row = json.loads(line)
                except ValueError as e:
                    raise RuntimeError(f'Hatali JSONL: {path.name}, satir {i}: {e}')
                if not isinstance(row, dict):
                    raise RuntimeError(f'JSON nesnesi bekleniyordu: {path.name}:{i}')
                rows.append(row)
    return rows


def write_jsonl(path, rows):
    with path.open('w', encoding='utf-8', newline='\n') as h:
        for row in rows:
            h.write(json.dumps(row, ensure_ascii=False) + '\n')


def map_ids(rows, name):
    result = {}
    for r in rows:
        rid = r.get('id')
        src = r.get('source_document')
        if not isinstance(rid, str) or not rid or not isinstance(src, str) or not src:
            raise RuntimeError(f'{name} icinde bos id veya source_document.')
        if rid in result:
            raise RuntimeError(f'{name} icinde cift ID: {rid}')
        result[rid] = r
    return result


def main():
    if OUTPUT.exists() or REPORT.exists():
        raise RuntimeError('Yeni aday klasoru veya rapor zaten mevcut. Mevcut ciktiyi silmeden once kontrol et: ' + str(OUTPUT))

    corpus = load(DATA / 'domain_corpus_v1_aday.jsonl')
    instruction = load(DATA / 'instruction_dataset_3075_aday.jsonl')
    c_byid = map_ids(corpus, 'Corpus')
    q_byid = map_ids(instruction, 'Instruction')
    if len(corpus) != 9554 or len(instruction) != 3075:
        raise RuntimeError(f'Beklenen kayitlar bulunamadi: corpus={len(corpus)}, instruction={len(instruction)}')

    old_csplit = {}
    source_to_split = {}
    for row in corpus:
        s, rid, split = row['source_document'], row['id'], row.get('split')
        if split not in SPLITS:
            raise RuntimeError(f'Corpus split hatali: {rid}, {split!r}')
        if s in source_to_split and source_to_split[s] != split:
            raise RuntimeError(f'Ayni corpus kaynagi birden cok splitte: {s}')
        source_to_split[s] = split
        old_csplit[rid] = split

    # Confirm that all currently stored splits match the complete datasets.
    for split in SPLITS:
        part = load(DATA / 'corpus_v1' / f'domain_corpus_{split}.jsonl')
        ids = [r['id'] for r in part]
        if len(set(ids)) != len(ids) or set(ids) != {r['id'] for r in corpus if r['split'] == split}:
            raise RuntimeError(f'Eski corpus {split} ayrimi full dosyayla uyusmuyor.')

    old_qsplit = {}
    qa_by_source = defaultdict(Counter)
    for split in SPLITS:
        part = load(DATA / 'instruction_v1' / f'{split}.jsonl')
        for r in part:
            rid = r.get('id')
            if rid not in q_byid or rid in old_qsplit:
                raise RuntimeError(f'Instruction split ID sorunu: {rid}')
            if r.get('source_document') != q_byid[rid].get('source_document'):
                raise RuntimeError(f'Instruction source uyusmazligi: {rid}')
            old_qsplit[rid] = split
            qa_by_source[r['source_document']][split] += 1
    if set(old_qsplit) != set(q_byid):
        raise RuntimeError('Instruction split toplam IDs, full dosya ile esit degil.')
    for s, split_counts in qa_by_source.items():
        if s not in source_to_split:
            raise RuntimeError(f'Instruction kaynagi corpusta yok: {s}')
        if set(split_counts) != {source_to_split[s]}:
            raise RuntimeError(f'Corpus-instruction split uyumsuz: {s}')

    # Use original corpus row IDs to verify that each CSV pairing is valid.
    with PAIRS.open(encoding='utf-8-sig', newline='') as h:
        pairs = list(csv.DictReader(h))
    if not pairs:
        raise RuntimeError('Near-duplicate cift CSV dosyasi bos.')

    parent = {s: s for s in source_to_split}
    def find(s):
        while parent[s] != s:
            parent[s] = parent[parent[s]]
            s = parent[s]
        return s
    def join(a, b):
        x, y = find(a), find(b)
        if x != y:
            parent[max(x, y)] = min(x, y)

    old_cross = 0
    for row in pairs:
        a, b = row.get('id_1'), row.get('id_2')
        if a not in c_byid or b not in c_byid:
            raise RuntimeError(f'CSV icindeki ID corpusta yok: {a}, {b}')
        r1, r2 = c_byid[a], c_byid[b]
        if r1['source_document'] != row.get('source_document_1') or r2['source_document'] != row.get('source_document_2'):
            raise RuntimeError(f'CSV kaynak adi uyusmazligi: {a}, {b}')
        if r1['split'] != r2['split']:
            old_cross += 1
        join(r1['source_document'], r2['source_document'])

    components = defaultdict(list)
    for s in sorted(source_to_split):
        components[find(s)].append(s)
    corpus_by_source = Counter(r['source_document'] for r in corpus)

    source_newsplit = {}
    changed_components = []
    for component in components.values():
        present = {source_to_split[s] for s in component}
        if len(present) == 1:
            chosen = next(iter(present))
        else:
            # Maximise retention of existing rows, weighted towards question
            # examples so instruction splits change as little as possible.
            score = {
                split: sum(corpus_by_source[s] * (source_to_split[s] == split)
                           + 3 * qa_by_source[s][split] for s in component)
                for split in SPLITS
            }
            chosen = max(SPLITS, key=lambda sp: (score[sp], -SPLITS.index(sp)))
            changed_components.append((component, chosen))
        for s in component:
            source_newsplit[s] = chosen

    new_cross = sum(source_newsplit[c_byid[p['id_1']]['source_document']] != source_newsplit[c_byid[p['id_2']]['source_document']] for p in pairs)
    if new_cross:
        raise RuntimeError(f'Bazi tespit edilmis ciftler halen farkli splitlerde: {new_cross}')

    c_full, q_full = [], []
    c_parts, q_parts = {s: [] for s in SPLITS}, {s: [] for s in SPLITS}
    changed_c, changed_q = 0, 0
    for row in corpus:
        new_split = source_newsplit[row['source_document']]
        updated = dict(row)
        updated['split'] = new_split
        c_full.append(updated)
        c_parts[new_split].append(updated)
        changed_c += (old_csplit[row['id']] != new_split)
    for row in instruction:
        new_split = source_newsplit[row['source_document']]
        updated = dict(row)
        updated['split'] = new_split
        q_full.append(updated)
        q_parts[new_split].append(updated)
        changed_q += (old_qsplit[row['id']] != new_split)

    assert sum(map(len, c_parts.values())) == len(corpus)
    assert sum(map(len, q_parts.values())) == len(instruction)
    for split in SPLITS:
        csrc = {r['source_document'] for r in c_parts[split]}
        qsrc = {r['source_document'] for r in q_parts[split]}
        if not qsrc.issubset(csrc):
            raise RuntimeError(f'Yeni {split} icin QA kaynagi corpusta yok.')

    # All input checks pass; write outputs to a new directory. NEVER alter originals.
    OUTPUT.mkdir(parents=True, exist_ok=False)
    (OUTPUT / 'corpus').mkdir()
    (OUTPUT / 'instruction').mkdir()
    write_jsonl(OUTPUT / 'domain_corpus_v1_resplit_aday.jsonl', c_full)
    write_jsonl(OUTPUT / 'instruction_dataset_3075_resplit_aday.jsonl', q_full)
    for split in SPLITS:
        write_jsonl(OUTPUT / 'corpus' / f'domain_corpus_{split}.jsonl', c_parts[split])
        write_jsonl(OUTPUT / 'instruction' / f'{split}.jsonl', q_parts[split])

    with (OUTPUT / 'source_resplit_manifest.csv').open('w', encoding='utf-8-sig', newline='') as h:
        writer = csv.writer(h)
        writer.writerow(['source_document', 'original_split', 'new_split', 'corpus_chunks', 'instruction_questions', 'changed'])
        for s in sorted(source_to_split):
            writer.writerow([s, source_to_split[s], source_newsplit[s], corpus_by_source[s],
                             sum(qa_by_source[s].values()), 'YES' if source_to_split[s] != source_newsplit[s] else 'NO'])

    changed_sources = [s for s in source_to_split if source_to_split[s] != source_newsplit[s]]
    lines = [
        '# Kaynak-gruplu yeniden bolme: ADAY raporu', '',
        '> Bu yeni aday dosyalar veri sizintisi riskini azaltmak icin uretilmistir. Eski dosyalara dokunulmamistir.', '',
        f'- Corpus: {len(corpus)} metin parcasi; Instruction: {len(instruction)} soru-cevap (kayit silinmedi).',
        f'- Kaynak belge: {len(source_to_split)}; baglantili kaynak grubu: {len(components)}.',
        f'- Tespit edilen benzer metin cifti: {len(pairs)}.',
        f'- Tespit edilen cross-split cift: once {old_cross}, yeni adayda {new_cross}.',
        f'- Yeni bolmeye gecen kaynak: {len(changed_sources)}; corpus parcasi: {changed_c}; instruction sorusu: {changed_q}.',
        '', '## Eski -> Yeni kayit sayilari', '',
        '| Veri | Bolme | Eski | Yeni |', '|---|---|---:|---:|',
    ]
    for typ, orig, new in (
        ('Corpus', old_csplit, c_parts),
        ('Instruction', old_qsplit, q_parts),
    ):
        for sp in SPLITS:
            lines.append(f'| {typ} | {sp} | {sum(v == sp for v in orig.values())} | {len(new[sp])} |')
    lines += [
        '', '## Degisen kaynaklar', '',
        '| Kaynak belge | Eski bolme | Yeni bolme | Corpus parcasi | Instruction sorusu |',
        '|---|---|---|---:|---:|',
    ]
    for s in sorted(changed_sources):
        safe_source = s.replace("|", "&#124;")
        lines.append(f'| {safe_source} | {source_to_split[s]} | {source_newsplit[s]} | {corpus_by_source[s]} | {sum(qa_by_source[s].values())} |')
    lines += [
        '', '## Yontem ve sinirlar', '',
        '- Benzer metin raporundaki kaynaklar baglantili bilesenlerde birlestirildi; her bilesen tek bolmeye atandi.',
        '- Mümkün oldugunca mevcut bolmeler korundu; buyuklukler yeni adayda farkli olabilir.',
        '- 63 aday cift icin cross-split kalmadi; ancak bu, tum olasi metin sizintilarinin temizlendigi anlamina gelmez.',
        '- Bazi ciftler gercek kopya degil, farkli yayinlarin ortak pasajlari olabilir. Konservatif olarak ayni splitte tutuldu.',
        '- Icerik ve kayit IDleri degistirilmedi; sadece split alanlari ve bolme dosyalari yeniden yazildi.',
        '- Kaynak lisanslari, anlamsal dogruluk ve ek near-duplicate esikleri ayri kontrol gerektirir.',
        '- Eski 08_validate_datasets.py, ESKI ayrimin sabit sayilarini kontrol eder; yeni aday icin kullanilmamalidir.',
        '- Yeni aday kontrolu icin bu script icinde sayilar, kaynak uyumu, tam ID kapsami ve tespit edilmis ciftlerin ayrimi dogrulandi.',
        '',
    ]
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('=== YENI SPLIT ADAYI HAZIR ===')
    print('Eski dosyalar DEGISTIRILMEDI.')
    print(f'Eski cross-split ciftleri: {old_cross} | Yeni: {new_cross}')
    print(f'Tasinan kaynak: {len(changed_sources)} | Corpus parcasi: {changed_c} | Soru: {changed_q}')
    print('CORPUS yeni:', {s: len(c_parts[s]) for s in SPLITS})
    print('INSTRUCTION yeni:', {s: len(q_parts[s]) for s in SPLITS})
    print('Dosyalar:', OUTPUT.relative_to(ROOT))
    print('Rapor:', REPORT.relative_to(ROOT))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, KeyError) as exc:
        print(f'HATA: {exc}', file=sys.stderr)
        sys.exit(1)
