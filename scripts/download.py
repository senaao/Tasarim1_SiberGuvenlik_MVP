import os
import requests
from urllib.parse import urlparse

os.makedirs("pdfs", exist_ok=True)

# BOM temizle
with open("links.txt", encoding="utf-8-sig") as f:
    urls = [l.strip() for l in f if l.strip()]

print(f"Toplam link: {len(urls)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

for i, url in enumerate(urls, 1):
    try:
        name = os.path.basename(urlparse(url).path) or f"dosya_{i}.pdf"
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        path = os.path.join("pdfs", name)
        if os.path.exists(path):
            print(f"[{i}] Zaten var: {name}")
            continue
        print(f"[{i}/{len(urls)}] İndiriliyor: {name}")
        r = requests.get(url, timeout=90, headers=headers, allow_redirects=True)
        if r.status_code == 200 and "pdf" in r.headers.get("content-type", "").lower():
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"  Tamam ({len(r.content)//1024} KB)")
        else:
            print(f"  Hata kodu: {r.status_code} | Content-Type: {r.headers.get('content-type')}")
    except Exception as e:
        print(f"  Hata: {e}")