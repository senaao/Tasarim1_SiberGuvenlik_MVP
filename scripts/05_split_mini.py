import json
import os
import hashlib
import random

def process_dedup_and_split():
    input_path = "data/final/domain_corpus_v0.1.jsonl"
    if not os.path.exists(input_path):
        print("❌ Corpus dosyası bulunamadı.")
        return

    docs = []
    seen_hashes = set()
    exact_duplicates = 0

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            # SHA-256 hash alarak birebir aynı metinleri tespit etme
            text_hash = hashlib.sha256(doc['text'].encode('utf-8')).hexdigest()
            if text_hash in seen_hashes:
                exact_duplicates += 1
            else:
                seen_hashes.add(text_hash)
                docs.append(doc)

    print(f"✓ Mükerrer Analizi: {exact_duplicates} adet birebir aynı kayıt elendi.")
    print(f"✓ Benzersiz Doküman Sayısı: {len(docs)}")

    # Karıştırma (Tekrarlanabilirlik / Reproducibility için sabit Seed)
    random.seed(42)
    random.shuffle(docs)

    n_total = len(docs)
    n_train = int(n_total * 0.90)
    n_val = int(n_total * 0.05)

    train_set = docs[:n_train]
    val_set = docs[n_train:n_train + n_val]
    test_set = docs[n_train + n_val:]

    sets = {'train': train_set, 'val': val_set, 'test': test_set}
    for name, s_data in sets.items():
        path = f"data/final/{name}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            for item in s_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"  └─ {name}.jsonl: {len(s_data)} doküman kaydedildi.")

if __name__ == "__main__":
    process_dedup_and_split()