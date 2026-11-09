import os
import fitz  # PyMuPDF

# PDF'lerin olduğu klasör
pdf_folder = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\raw"

# Çıktı klasörü
output_folder = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\extracted"
os.makedirs(output_folder, exist_ok=True)

# Tüm PDF'leri tara
for root, dirs, files in os.walk(pdf_folder):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            txt_name = os.path.splitext(file)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_name)

            # Zaten varsa atla
            if os.path.exists(txt_path):
                print(f"Atlandı (zaten var): {txt_name}")
                continue

            try:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()

                # Boşsa kaydetme
                if len(text.strip()) < 100:
                    print(f"BOŞ/ÇOK KISA: {file}")
                    continue

                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)

                print(f"Tamam: {txt_name} ({len(text)} karakter)")

            except Exception as e:
                print(f"HATA: {file} → {e}")

print("\nExtraction bitti!")