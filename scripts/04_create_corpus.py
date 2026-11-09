import os
import json

input_folder = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\cleaned_v2"
output_file = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\final\corpus_v2.jsonl"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

def count_tokens(text):
    return len(text.split())

with open(output_file, "w", encoding="utf-8") as out:
    for i, file in enumerate(sorted(os.listdir(input_folder)), 1):
        if not file.endswith(".txt"):
            continue
        path = os.path.join(input_folder, file)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()
        if len(text) < 300:
            continue
        doc = {
            "document_id": f"DOC_{i:06d}",
            "title": os.path.splitext(file)[0],
            "source": "cleaned_v2",
            "char_count": len(text),
            "token_count": count_tokens(text),
            "text": text
        }
        out.write(json.dumps(doc, ensure_ascii=False) + "\n")

print("corpus_v2.jsonl oluşturuldu.")