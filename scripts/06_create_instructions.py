import json
import os

# Çıktı dosyası
output_path = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\final\instruction_v1.0.jsonl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Örnek 5 tane (şimdilik elle)
examples = [
    {
        "messages": [
            {"role": "user", "content": "Zero Trust nedir?"},
            {"role": "assistant", "content": "Zero Trust, hiçbir kullanıcıya, cihaza veya ağa varsayılan olarak güvenilmemesi gerektiğini savunan bir güvenlik modelidir. Her erişim isteği doğrulanmalıdır."}
        ],
        "source_document": "DOC_000001",
        "task_type": "tanım"
    },
    {
        "messages": [
            {"role": "user", "content": "Ransomware nedir?"},
            {"role": "assistant", "content": "Ransomware, kurbanın dosyalarını şifreleyerek fidye talep eden bir zararlı yazılım türüdür."}
        ],
        "source_document": "DOC_000002",
        "task_type": "tanım"
    }
]

with open(output_path, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"{len(examples)} örnek yazıldı → {output_path}")