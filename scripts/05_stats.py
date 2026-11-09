import json

corpus_path = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\final\corpus.jsonl"

total_docs = 0
total_chars = 0
total_tokens = 0

with open(corpus_path, "r", encoding="utf-8") as f:
    for line in f:
        doc = json.loads(line)
        total_docs += 1
        total_chars += doc.get("char_count", 0)
        total_tokens += doc.get("token_count", 0)

print("=== CORPUS İSTATİSTİKLERİ ===")
print(f"Toplam doküman     : {total_docs}")
print(f"Toplam karakter    : {total_chars:,}")
print(f"Toplam token       : {total_tokens:,}")
print(f"Ortalama token/dok : {total_tokens // total_docs if total_docs else 0}")