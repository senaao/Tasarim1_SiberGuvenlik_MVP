import json
import os

def print_stats():
    final_dir = "data/final"
    files = ['train.jsonl', 'val.jsonl', 'test.jsonl', 'pdf_corpus_v0.1.jsonl', 'instruction_v1.0.jsonl']
    
    print("\n" + "="*55)
    print("   SDÜ BİLGİSAYAR MÜHENDİSLİĞİ - TASARIM I MVP VERİ RAPORU")
    print("="*55)
    
    total_docs = 0
    total_chars = 0
    
    for f_name in files:
        path = os.path.join(final_dir, f_name)
        if os.path.exists(path):
            count = 0
            chars = 0
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    count += 1
                    data = json.loads(line)
                    if 'char_count' in data:
                        chars += data['char_count']
            
            print(f"  ► {f_name:<26}: {count:>4} kayıt")
            if 'instruction' not in f_name:
                total_docs += count
                total_chars += chars
    
    avg_chars = int(total_chars / max(1, total_docs))
    est_tokens = int(total_chars / 4)
    
    print("-" * 55)
    print(f"  • Toplam Domain Corpus Dokümanı : {total_docs} adet")
    print(f"  • Ortalama Doküman Uzunluğu    : {avg_chars} karakter")
    print(f"  • Tahmini Toplam Hacim         : ~{est_tokens:,} Token")
    print("="*55 + "\n")

if __name__ == "__main__":
    print_stats()