#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vize: gerçek Qwen3 token sayımı + kaynak metin öncesi/sonrası kanıtları.
Mevcut dosyaları değiştirmez; reports/corpus/ altında TEK metin raporu üretir.
"""
from __future__ import annotations
import difflib
import json
import random
import re
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "corpus" / "VIZE_TOKEN_VE_ONCE_SONRA_RAPORU.txt"
MODEL = "Qwen/Qwen3-4B-Base"  # Hocanın rehberinde verilen model ailesi / tokenizer.


def input_files():
    folder = ROOT / "data" / "final" / "guvenli_split_aday" / "corpus"
    three = [folder / f"domain_corpus_{name}.jsonl" for name in ("train", "val", "test")]
    if all(f.is_file() for f in three):
        return three
    singles = [
        ROOT / "data" / "final" / "guvenli_split_aday" / "domain_corpus_v1_resplit_aday.jsonl",
        ROOT / "data" / "final" / "domain_corpus_v1_aday.jsonl",
        ROOT / "data" / "final" / "corpus_v1" / "domain_corpus_v1_aday.jsonl",
    ]
    for path in singles:
        if path.is_file():
            return [path]
    raise FileNotFoundError("Corpus bulunamadi. Beklenen: data/final/guvenli_split_aday/corpus/domain_corpus_{train,val,test}.jsonl")


def load_corpus(paths):
    entries = []
    ids = set()
    for path in paths:
        with path.open(encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                item = json.loads(line)
                if not isinstance(item.get("text"), str) or not item.get("source_document"):
                    raise ValueError(f"{path.name}:{lineno}: source_document veya text eksik")
                ident = item.get("id")
                if ident and ident in ids:
                    raise ValueError(f"Ayni kayit iki kez bulundu: {ident}")
                if ident:
                    ids.add(ident)
                entries.append(item)
    return entries


def load_tokenizer():
    try:
        from transformers import AutoTokenizer
    except ImportError:
        print("transformers kuruluyor; bu islem yalnizca ilk calistirmada gerekir...", flush=True)
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "transformers>=4.51,<5"
        ])
        from transformers import AutoTokenizer
    print("Qwen3-4B-Base tokenizer yukleniyor (MODEL AGIRLIKLARI indirilmiyor)...", flush=True)
    return AutoTokenizer.from_pretrained(MODEL, use_fast=True, trust_remote_code=False)


def distribution(values):
    a = sorted(values)
    if not a:
        return {"min": 0, "median": 0, "mean": 0, "p95": 0, "max": 0}
    return {
        "min": a[0],
        "median": round(statistics.median(a), 1),
        "mean": round(statistics.mean(a), 1),
        "p95": a[max(0, int(0.95 * (len(a) - 1)))],
        "max": a[-1],
    }


def tokens_report(entries):
    tokenizer = load_tokenizer()
    per_doc = defaultdict(int)
    per_split = defaultdict(int)
    counts = []
    for i, entry in enumerate(entries, 1):
        length = len(tokenizer.encode(entry["text"], add_special_tokens=False))
        counts.append(length)
        per_doc[entry["source_document"]] += length
        per_split[str(entry.get("split", "belirtilmedi"))] += length
        if i % 1000 == 0:
            print(f"Token sayimi: {i}/{len(entries)}", flush=True)
    return sum(counts), distribution(counts), distribution(list(per_doc.values())), dict(per_split), len(per_doc)


def normalized_stem(path):
    return re.sub(r"[^\w]", "", Path(path).stem.casefold(), flags=re.UNICODE)


def index_files(directories, ext):
    result = defaultdict(list)
    for base in directories:
        folder = ROOT / base
        if not folder.is_dir():
            continue
        for path in folder.rglob(f"*.{ext}"):
            result[normalized_stem(path.name)].append(path)
    return result


def text_from(path):
    if path.suffix.lower() == ".pdf":
        try:
            import pymupdf as fitz
        except ImportError:
            import fitz
        with fitz.open(str(path)) as doc:
            return "\n".join(doc[i].get_text("text") for i in range(min(len(doc), 2)))
    return path.read_text(encoding="utf-8", errors="replace")


def compact(s):
    return " ".join(s.replace("\x00", " ").split())


def cut(s, n=350):
    x = compact(s)
    return x[:n] + ("..." if len(x) > n else "")


def samples_report(entries, target=12):
    docs = sorted(set(item["source_document"] for item in entries))
    random.Random(42).shuffle(docs)
    extracted = index_files([Path("data/extracted"), Path("data/extracted_text"), Path("data/extracted_v2")], "txt")
    cleaned = index_files([Path("data/cleaned_v2"), Path("data/cleaned"), Path("data/cleaned_text")], "txt")
    pdfs = index_files([Path("data/raw")], "pdf")
    results = []
    visited = 0
    for doc in docs:
        key = normalized_stem(doc)
        if len(cleaned.get(key, [])) != 1:
            continue
        clean_path = cleaned[key][0]
        before_candidates = extracted.get(key, [])
        method = "extracted TXT -> cleaned TXT"
        if len(before_candidates) == 1:
            before_path = before_candidates[0]
        elif len(before_candidates) == 0 and len(pdfs.get(key, [])) == 1:
            before_path = pdfs[key][0]
            method = "PDF ilk 2 sayfa extraction -> cleaned TXT"
        else:
            continue  # Belirsiz dosya eşleşmesini kaydetme.
        visited += 1
        try:
            before = text_from(before_path)
            after = text_from(clean_path)
        except Exception:
            continue
        b, a = compact(before), compact(after)
        if min(len(a), len(b)) < 200 or a == b:
            continue
        # İncelenen bölümler aynı belgeye ait olsun; aşırı uyumsuz eşleşmeyi ele.
        ratio = difflib.SequenceMatcher(None, b[:950], a[:950], autojunk=True).ratio()
        if b[:350] == a[:350]:
            continue
        results.append({"name": doc, "before": cut(before), "after": cut(after),
                        "kind": method, "match": round(ratio, 3),
                        "from": str(before_path.relative_to(ROOT)),
                        "to": str(clean_path.relative_to(ROOT))})
        if len(results) >= target:
            break
    return results, visited, len(extracted), len(cleaned), len(pdfs)


def write_result(lines):
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print("\nRAPOR: " + str(REPORT), flush=True)


def main():
    paths = input_files()
    entries = load_corpus(paths)
    print("Okunan Corpus kaydi:", len(entries), "| benzersiz kaynak:", len(set(e['source_document'] for e in entries)), flush=True)
    lines = ["VIZE - CORPUS TOKEN VE TEMIZLEME KANIT RAPORU", "",
             "KAYNAK JSONL: " + "; ".join(str(x.relative_to(ROOT)) for x in paths),
             f"Corpus kaydi: {len(entries)}",
             f"Farkli kaynak belge: {len(set(x['source_document'] for x in entries))}", ""]
    try:
        total, chunks, docs, splits, docnum = tokens_report(entries)
        lines.extend(["=== GERCEK TOKEN SAYIMI ===", "Tokenizer: " + MODEL,
                      "Yontem: Her Corpus text alanini add_special_tokens=False ile tokenize edip toplama",
                      f"TOPLAM_TOKEN: {total:,}", f"CHUNK_DAGILIMI: {chunks}",
                      f"DOKUMAN_DAGILIMI: {docs}",
                      f"SPLIT_TOKENLERI: {splits}",
                      f"Tokenlanan belge: {docnum}", ""])
        print("TOPLAM TOKEN:", f"{total:,}", flush=True)
    except Exception as e:
        lines.extend(["=== TOKEN SAYIMI TAMAMLANAMADI ===", "Sebep: " + str(e),
                      "Bu nedenle raporda tahmini token sayisi yazilmadi.", ""])
        print("Token sayimi hatasi:", e, flush=True)
    try:
        samples, checked, n_extract, n_clean, n_pdf = samples_report(entries)
        lines.extend(["=== GERCEK ONCE / SONRA METIN ORNEKLERI ===",
                      "Eslesme: Ayni kaynak dosya adina sahip extracted/PDF ve cleaned_v2 metni.",
                      "Alintilar ilgili dosyalarin baslangic kesitleridir; yer degistirmis paragraflar bire bir hizalanmis degildir.",
                      f"OLUSTURULAN_ORNEK: {len(samples)}",
                      f"KONTROL_EDILEN_ESLESME: {checked}",
                      f"Taranan dosya anahtarlari: extracted={n_extract}, cleaned={n_clean}, pdf={n_pdf}", ""])
        for i, sample in enumerate(samples, 1):
            lines.extend([f"ORNEK {i:02d} - {sample['name']}",
                          f"Yontem: {sample['kind']}",
                          f"Once dosyasi: {sample['from']}",
                          f"Sonra dosyasi: {sample['to']}",
                          "ONCE: " + sample["before"],
                          "SONRA: " + sample["after"], ""])
        if not samples:
            lines.append("Ornek cikmadi. data/extracted ve data/cleaned_v2 klasorlerinin oldugunu kontrol edin. Eslesmeyen dosyalar tahmin edilmedi.")
        print("Gercek metin karsilastirmasi:", len(samples), "ornek", flush=True)
    except Exception as e:
        lines.extend(["=== METIN KARSILASTIRMA TAMAMLANAMADI ===", "Sebep: " + str(e)])
        print("Karsilastirma hatasi:", e, flush=True)
    write_result(lines)
    print("ESKI VERILER DEGISTIRILMEDI. Raporu ChatGPT'ye gonderin.")

if __name__ == "__main__":
    main()
