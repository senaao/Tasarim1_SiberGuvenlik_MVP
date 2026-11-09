import os
import re

input_folder = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\extracted"
output_folder = r"C:\Users\snmrl\Tasarim1_SiberGuvenlik_MVP\data\cleaned_v2"
os.makedirs(output_folder, exist_ok=True)

def clean_text(text):
    # Satır satır temizle
    lines = text.splitlines()
    cleaned_lines = []
    
    bad_patterns = [
        r"this page intentionally left blank",
        r"table of contents",
        r"all rights reserved",
        r"copyright",
        r"page \d+",
        r"doi\.org",
        r"https?://",
        r"www\.",
        r"@\w+\.\w+",
        r"figure \d+",
        r"table \d+",
        r"^\s*\d+\s*$",  # sadece sayı olan satırlar
        r"u\.s\. department of commerce",
        r"national institute of standards",
    ]
    
    for line in lines:
        line = line.strip()
        if len(line) < 20:
            continue
        lower = line.lower()
        if any(re.search(p, lower) for p in bad_patterns):
            continue
        # Çok fazla büyük harf varsa at
        if sum(1 for c in line if c.isupper()) > len(line) * 0.4:
            continue
        cleaned_lines.append(line)
    
    text = "\n".join(cleaned_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

count = 0
for file in os.listdir(input_folder):
    if not file.endswith(".txt"):
        continue
    path = os.path.join(input_folder, file)
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        cleaned = clean_text(text)
        if len(cleaned) < 400:
            continue
        out_path = os.path.join(output_folder, file)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)
        count += 1
    except:
        continue

print(f"Temizlenen dosya sayısı: {count}")