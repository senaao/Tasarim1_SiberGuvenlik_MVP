"""PDF klasorundeki belgeler icin yerel kaynak envanteri hazirlar.

Calistirma (projenin ana klasorunden):
    python scripts/11_pdf_kaynak_envanteri.py

Acildiginda PDF'lerin bulundugu ana klasoru secin. Alt klasorler de taranir.
PDF'ler okunur, kopyalanmaz, degistirilmez veya yuklenmez.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF kurulu degil. Terminal: python -m pip install pymupdf")
    sys.exit(1)


KURUM_DESENLERI = (
    ("NIST", r"\bNIST\b|National Institute of Standards and Technology"),
    ("OWASP", r"\bOWASP\b"),
    ("CISA", r"\bCISA\b|Cybersecurity and Infrastructure Security Agency"),
    ("ENISA", r"\bENISA\b|European Union Agency for Cybersecurity"),
    ("MITRE", r"\bMITRE\b|ATT&CK"),
    ("CIS", r"\bCIS Controls\b|Center for Internet Security"),
    ("Kubernetes", r"\bKubernetes\b"),
    ("SANS", r"\bSANS Institute\b"),
    ("NVD", r"National Vulnerability Database|\bNVD\b"),
)
URL_DESEN = re.compile(r"https?://[^\s<>\[\]\"']+", re.I)


def kurum_adayi(dosya_adi: str, baslik: str, yazar: str, ilk_metin: str) -> str:
    # Once dosya adindan ve PDF metadatasindan karar ver; ilk sayfa
    # baska kurumlara atif yapabilecegi icin oradan kesin sonuc cikarma.
    guclu_kanit = " ".join((dosya_adi, baslik, yazar))
    for kurum, desen in KURUM_DESENLERI:
        if re.search(desen, guclu_kanit, flags=re.I):
            return kurum
    ilk_bolum = ilk_metin[:700]
    for kurum, desen in KURUM_DESENLERI:
        if re.search(desen, ilk_bolum, flags=re.I):
            return kurum + " (tahmini)"
    return "BELIRLENEMEDI"


def temiz_metin(metin: str, sinir: int = 400) -> str:
    return re.sub(r"\s+", " ", metin).strip()[:sinir]


def aday_url(metin: str) -> str:
    # PDF metninde URL bulunmasi o dosyanin indirildigi adres oldugunu kanitlamaz.
    for url in URL_DESEN.findall(metin[:6000]):
        url = url.rstrip(".,;:)")
        if len(url) < 250:
            return url
    return ""


def klasor_sec() -> Path:
    try:
        import tkinter as tk
        from tkinter import filedialog
        pencere = tk.Tk()
        pencere.withdraw()
        pencere.attributes("-topmost", True)
        konum = filedialog.askdirectory(title="PDF'lerin oldugu ANA klasoru secin (alt klasorler de taranir)")
        pencere.destroy()
    except Exception as hata:
        raise RuntimeError(
            "Klasor secim penceresi acilamadi. "
            "Ornek: python scripts/11_pdf_kaynak_envanteri.py --folder \"C:\\PDFler\""
        ) from hata
    if not konum:
        raise RuntimeError("Klasor secilmedi. Islem iptal edildi.")
    return Path(konum)


def main() -> None:
    parser = argparse.ArgumentParser(description="PDF'lerden kaynak envanteri CSV'si olusturur.")
    parser.add_argument("--folder", type=Path, default=None, help="PDF ana klasoru (istege bagli)")
    args = parser.parse_args()

    klasor = args.folder if args.folder else klasor_sec()
    if not klasor.is_dir():
        print(f"Klasor bulunamadi: {klasor}")
        sys.exit(1)

    pdfler = sorted((p for p in klasor.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"),
                    key=lambda p: str(p).casefold())
    if not pdfler:
        print("Secilen klasorde veya alt klasorlerinde PDF bulunamadi.")
        sys.exit(1)

    proje = Path(__file__).resolve().parent.parent
    hedef = proje / "reports" / "corpus" / "pdf_kaynak_envanteri.csv"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    alanlar = [
        "pdf_file", "relative_path", "file_size_mb", "pages",
        "pdf_title", "pdf_author", "pdf_subject", "pdf_keywords",
        "source_group_candidate", "url_inside_pdf_candidate_not_verified",
        "first_page_sample", "license_status", "read_status"
    ]
    sayac: Counter[str] = Counter()
    with hedef.open("w", encoding="utf-8-sig", newline="") as dosya:
        yazici = csv.DictWriter(dosya, fieldnames=alanlar)
        yazici.writeheader()
        for i, pdf in enumerate(pdfler, 1):
            satir = {alan: "" for alan in alanlar}
            satir["pdf_file"] = pdf.name
            satir["relative_path"] = pdf.relative_to(klasor).as_posix()
            satir["file_size_mb"] = round(pdf.stat().st_size / 1048576, 2)
            satir["license_status"] = "NOT_VERIFIED"
            try:
                with fitz.open(pdf) as doc:
                    meta = doc.metadata or {}
                    satir["pages"] = doc.page_count
                    satir["pdf_title"] = (meta.get("title") or "")[:250]
                    satir["pdf_author"] = (meta.get("author") or "")[:250]
                    satir["pdf_subject"] = (meta.get("subject") or "")[:250]
                    satir["pdf_keywords"] = (meta.get("keywords") or "")[:250]
                    ilk_sayfa = doc[0].get_text("text") if len(doc) else ""
                    satir["first_page_sample"] = temiz_metin(ilk_sayfa)
                    satir["source_group_candidate"] = kurum_adayi(
                        pdf.name, satir["pdf_title"], satir["pdf_author"], ilk_sayfa
                    )
                    satir["url_inside_pdf_candidate_not_verified"] = aday_url(ilk_sayfa)
                    satir["read_status"] = "OK"
            except Exception as hata:
                satir["read_status"] = f"ERROR: {str(hata)[:160]}"
                satir["source_group_candidate"] = "BELIRLENEMEDI"
            sayac[satir["read_status"].split(":")[0]] += 1
            yazici.writerow(satir)
            if i % 100 == 0:
                print(f"Islenen PDF: {i}/{len(pdfler)}")

    print(f"\nBitti. PDF sayisi: {len(pdfler)}")
    print(f"Okunabilen: {sayac['OK']} | Hata: {len(pdfler) - sayac['OK']}")
    print("PDF'lerin hicbiri degistirilmedi.")
    print(f"CSV dosyasi: {hedef}")
    print("NOT: Kaynak kurumu ve URL adaylari kesin degildir; lisanslar NOT_VERIFIED.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as hata:
        print(hata)
        sys.exit(1)
