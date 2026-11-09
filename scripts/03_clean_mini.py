import json
import os
import re

def clean_text(text):
    # Fazla boşlukları ve satır başlarını temizleme
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_raw_data():
    os.makedirs("data/final", exist_ok=True)
    raw_path = "data/raw/nvd_500_raw.json"
    
    if not os.path.exists(raw_path):
        print("❌ Ham veri bulunamadı. Önce 01_download_mini.py çalıştırılmalı.")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    corpus = []
    vulnerabilities = data.get('vulnerabilities', [])
    
    for idx, item in enumerate(vulnerabilities):
        cve_id = item['cve']['id']
        descriptions = item['cve']['descriptions']
        
        # İngilizce açıklamayı seçme
        text_en = next((d['value'] for d in descriptions if d['lang'] == 'en'), "")
        cleaned = clean_text(text_en)
        
        # Filtreleme: 60 karakterden kısa anlamsız metinleri eleme
        if len(cleaned) > 60:
            words = cleaned.split()
            doc = {
                "document_id": f"DOC_{idx+1:04d}",
                "cve_id": cve_id,
                "source": "NVD_CVE_API",
                "language": "en",
                "char_count": len(cleaned),
                "estimated_tokens": int(len(words) * 1.3),
                "text": cleaned
            }
            corpus.append(doc)

    out_path = "data/final/domain_corpus_v0.1.jsonl"
    with open(out_path, "w", encoding="utf-8") as f:
        for entry in corpus:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✓ Temizleme tamamlandı. {len(corpus)} adet doküman {out_path} dosyasına yazıldı.")

if __name__ == "__main__":
    process_raw_data()