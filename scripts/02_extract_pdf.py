import os
import json
from pypdf import PdfReader

def extract_pdfs():
    raw_dir = "data/raw"
    extracted_dir = "data/extracted"
    os.makedirs(extracted_dir, exist_ok=True)
    
    out_file = os.path.join(extracted_dir, "pdf_extracted.jsonl")
    
    pdf_files = [f for f in os.listdir(raw_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"ℹ '{raw_dir}' klasorunde islenecek PDF bulunamadi.")
        return

    extracted_count = 0
    with open(out_file, "w", encoding="utf-8") as out_f:
        for pdf_name in pdf_files:
            pdf_path = os.path.join(raw_dir, pdf_name)
            reader = PdfReader(pdf_path)
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    doc = {
                        "document_id": f"{pdf_name}_p{page_num}",
                        "source": pdf_name,
                        "page": page_num,
                        "text": text.strip()
                    }
                    out_f.write(json.dumps(doc, ensure_ascii=False) + "\n")
                    extracted_count += 1
                    
    print(f"✓ PDF Metin Cikarma Tamamlandi: {extracted_count} sayfa '{out_file}' dosyasina kaydedildi.")

if __name__ == "__main__":
    extract_pdfs()