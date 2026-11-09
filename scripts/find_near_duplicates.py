"""Find possible near-duplicates using TF-IDF cosine similarity.

This is a screening heuristic, NOT automatic proof of duplicate content.
Review candidates manually before dropping records.
Usage:
  python scripts/find_near_duplicates.py --input raw.jsonl --output near_pairs.csv
Requires: scikit-learn.
"""
import argparse
import csv
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--threshold', type=float, default=0.83)
    args = p.parse_args()
    items = [json.loads(s) for s in args.input.open(encoding='utf8') if s.strip()]
    vec = TfidfVectorizer(ngram_range=(1, 2),min_df=2,max_df=.97,
                          max_features=140000,sublinear_tf=True)
    x = vec.fit_transform(k['text'] for k in items)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    found = 0
    with args.output.open('w',encoding='utf8',newline='') as f:
        w = csv.writer(f)
        w.writerow(['id_1','id_2','tfidf_cosine_similarity','source_document_1','source_document_2'])
        for start in range(0, len(items), 96):
            sims = (x[start:start + 96] @ x.T).tocoo()
            for loc, col, sim in zip(sims.row, sims.col, sims.data):
                i = start + int(loc)
                j = int(col)
                if j > i and sim >= args.threshold:
                    found += 1
                    w.writerow([items[i]['id'],items[j]['id'],round(float(sim),4),
                                items[i]['source_document'],items[j]['source_document']])
    print('Potential duplicate pairs:', found)

if __name__=='__main__':
    main()
