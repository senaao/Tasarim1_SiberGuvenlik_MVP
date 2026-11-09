"""Audit and stage a source-document-grouped cybersecurity domain corpus.

Preserves original source text; avoids deleting suspected errors without manual review.
Inputs: JSONL with id/source_document/text; CSV instruction split manifest.
Dependencies: Python standard library. Near-duplicate candidate CSV is optional and
should be generated separately using TF-IDF or a MinHash pipeline.
"""
import argparse
import csv
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

REPLACEMENT = '\ufffd'
DOT_LEADERS = re.compile(r'\.{8,}')
BIBLIO = re.compile(r'(?i)\b(references|bibliography)\b')
CITE = re.compile(r'\[\s*\d+\s*\]')
PAGE = re.compile(r'(?i)\bcontinued on next page\b|(?i:page\s+\d+\s+of\s+\d+)')


def load_jsonl(p):
    result = []
    with p.open(encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as e:
                    raise ValueError(f'{p.name}: line {n}: {e}') from e
                result.append(obj)
    return result


def save_jsonl(p, items):
    with p.open('w', encoding='utf-8') as f:
        for obj in items:
            f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def make_split(doc_name):
    """Deterministically assign only corpus-only docs; QA docs use QA manifest."""
    v = int(hashlib.sha256(('corpus-2026:' + doc_name).encode()).hexdigest()[:8], 16) % 100
    return 'train' if v < 80 else ('val' if v < 90 else 'test')


def flags_for(text):
    issues = []
    if len(text.strip()) < 600:
        issues.append('short_chunk')
    if text.count(REPLACEMENT):
        issues.append('unicode_replacement')
    if len(DOT_LEADERS.findall(text)) >= 4:
        issues.append('toc_or_page_leader')
    alpha = sum(c.isalpha() for c in text)
    if alpha / max(len(text), 1) < .47:
        issues.append('low_alphabetic_ratio')
    if BIBLIO.search(text) and len(CITE.findall(text)) >= 5:
        issues.append('bibliography_possible')
    if PAGE.search(text):
        issues.append('page_artifact_possible')
    return issues


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--input', required=True, type=Path)
    a.add_argument('--qa-manifest', required=True, type=Path)
    a.add_argument('--near-pairs', required=False, type=Path)
    a.add_argument('--out', required=True, type=Path)
    args = a.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records = load_jsonl(args.input)
    qa_doc_split = {}
    with args.qa_manifest.open(encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            doc, split = row['source_document'], row['split']
            assert split in ('train', 'val', 'test')
            assert doc not in qa_doc_split or qa_doc_split[doc] == split
            qa_doc_split[doc] = split

    near_ids = set()
    pair_count = 0
    if args.near_pairs and args.near_pairs.exists():
        with args.near_pairs.open(encoding='utf-8', newline='') as f:
            for row in csv.reader(f):
                if len(row) >= 3 and row[2] != 'tfidf_cosine_similarity' and float(row[2]) >= .92:
                    near_ids.update([row[0],row[1]])
                    pair_count += 1

    if any(not {'id','source_document','text'}.issubset(k) for k in records):
        raise ValueError('JSONL records must have id, source_document and text')
    if len({k['id'] for k in records}) != len(records):
        raise ValueError('Not all chunk IDs are unique')
    doc_counts = Counter(k['source_document'] for k in records)
    assert set(qa_doc_split).issubset(set(doc_counts)), 'Instruction document outside corpus; inspect and resolve.'
    exactseen = {}
    duplicate_exact = 0
    converted = []
    flag_counts = Counter()
    split_counts = Counter()
    groupcounts = Counter()
    doc_flags = defaultdict(Counter)
    doc_flagged_chunks = Counter()
    review = []
    original_paths = defaultdict(set)
    for k in records:
        text = k['text']
        doc = k['source_document']
        d_id = 'DOC_' + hashlib.sha256(doc.encode('utf-8')).hexdigest()[:12]
        split = qa_doc_split.get(doc, make_split(doc))
        issues = flags_for(text)
        if k['id'] in near_ids:
            issues.append('near_duplicate_candidate')
        hx = hashlib.sha256(text.encode('utf8')).hexdigest()
        if hx in exactseen:
            issues.append('exact_duplicate')
            duplicate_exact += 1
        else:
            exactseen[hx] = k['id']
        obj = {
            'id': k['id'],
            'document_id': d_id,
            'source_document': doc,
            'source_path_original': k.get('source_path',''),
            'text': text,
            'char_count': len(text),
            'word_count': len(text.split()),
            'split': split,
            'quality_flags': issues,
            'manual_reviewed': False,
        }
        converted.append(obj)
        for reason in issues: flag_counts[reason]+=1;doc_flags[doc][reason]+=1
        if issues:
            doc_flagged_chunks[doc] += 1
            review.append(obj)
        split_counts[split]+=1
        original_paths[doc].add(k.get('source_path',''))
    for doc in doc_counts:
        groupcounts[qa_doc_split.get(doc, make_split(doc))] += 1
    save_jsonl(args.out/'domain_corpus_v1_aday.jsonl', converted)
    save_jsonl(args.out/'domain_corpus_inceleme_gerekenler.jsonl', review)
    for split in ('train','val','test'):
        save_jsonl(args.out/f'domain_corpus_{split}.jsonl',[k for k in converted if k['split']==split])
    with (args.out/'source_inventory.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f)
        w.writerow(['document_id','source_document','source_path_original','chunk_count','split','flagged_chunks','source_url','license_status','language','document_type'])
        for doc in sorted(doc_counts):
            w.writerow(['DOC_'+hashlib.sha256(doc.encode()).hexdigest()[:12],doc,'; '.join(sorted(original_paths[doc])),doc_counts[doc],qa_doc_split.get(doc,make_split(doc)),doc_flagged_chunks[doc],'','NOT_VERIFIED','','TXT'])
    with (args.out/'review_manifest.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['id','source_document','flags','review_decision','reviewer_note'])
        for k in review:
            w.writerow([k['id'],k['source_document'],'|'.join(k['quality_flags']),'PENDING',''])
    summary={
        'version': 'v1_candidate',
        'original_chunks':len(records),
        'source_documents':len(doc_counts),
        'total_characters':sum(len(k['text']) for k in records),
        'total_words_whitespace_count':sum(len(k['text'].split()) for k in records),
        'median_chars_per_chunk':statistics.median(len(k['text']) for k in records),
        'source_doc_manifest_matched':len(set(doc_counts)&set(qa_doc_split)),
        'source_doc_not_in_instruction':len(set(doc_counts)-set(qa_doc_split)),
        'qa_docs_missing_from_corpus':len(set(qa_doc_split)-set(doc_counts)),
        'split_chunks':dict(split_counts),
        'split_documents':dict(groupcounts),
        'flagged_chunks_union':len(review),
        'quality_flags':dict(flag_counts),
        'high_similarity_cosine_pairs_ge_0_92':pair_count,
        'exact_duplicate_texts':duplicate_exact,
        'manual_quality_samples_completed_for_this_corpus':0,
        'verified_license_records':0,
        'actual_token_count_measured':False,
    }
    (args.out/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
    return summary

if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
