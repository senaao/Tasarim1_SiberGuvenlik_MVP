"""Siber Guvenlik projesi: corpus ve instruction bolmelerini dogrular.

Kullanim (projenin ana klasorunden):
    python scripts/08_validate_datasets.py

Bu dosya veri setlerini degistirmez; sadece okur ve ekrana rapor basar.
Yalnizca Python standart kutuphanesini kullanir.
"""

from collections import Counter
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
FINAL = ROOT / "data" / "final"

FILES = {
    "corpus": {
        "full": FINAL / "domain_corpus_v1_aday.jsonl",
        "train": FINAL / "corpus_v1" / "domain_corpus_train.jsonl",
        "val": FINAL / "corpus_v1" / "domain_corpus_val.jsonl",
        "test": FINAL / "corpus_v1" / "domain_corpus_test.jsonl",
    },
    "instruction": {
        "full": FINAL / "instruction_dataset_3075_aday.jsonl",
        "train": FINAL / "instruction_v1" / "train.jsonl",
        "val": FINAL / "instruction_v1" / "val.jsonl",
        "test": FINAL / "instruction_v1" / "test.jsonl",
    },
}

EXPECTED = {
    "corpus": {"full": 9554, "train": 7702, "val": 980, "test": 872},
    "instruction": {"full": 3075, "train": 2448, "val": 326, "test": 301},
}


def read_jsonl(path, dataset_kind, problems):
    if not path.is_file():
        problems.append(f"Eksik dosya: {path.relative_to(ROOT)}")
        return None

    ids = set()
    sources = set()
    n = 0
    missing_ids = 0
    missing_sources = 0
    missing_content = 0
    duplicate_ids = 0

    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append(f"Gecersiz JSON: {path.name}, satir {line_number}: {exc.msg}")
                continue
            if not isinstance(row, dict):
                problems.append(f"JSON nesnesi degil: {path.name}, satir {line_number}")
                continue

            n += 1
            record_id = row.get("id")
            source = row.get("source_document")
            content_field = "text" if dataset_kind == "corpus" else "output"
            content = row.get(content_field)

            if not isinstance(record_id, str) or not record_id.strip():
                missing_ids += 1
            elif record_id in ids:
                duplicate_ids += 1
            else:
                ids.add(record_id)

            if not isinstance(source, str) or not source.strip():
                missing_sources += 1
            else:
                sources.add(source)

            if not isinstance(content, str) or not content.strip():
                missing_content += 1

    for label, amount in (
        ("bos/eksik ID", missing_ids),
        ("tekrar ID", duplicate_ids),
        ("eksik kaynak", missing_sources),
        ("bos icerik", missing_content),
    ):
        if amount:
            problems.append(f"{path.name}: {amount} adet {label}")

    return {"count": n, "ids": ids, "sources": sources}


def main():
    print("=== SIBER GUVENLIK VERI SETI DOGRULAMASI ===")
    print(f"Proje: {ROOT}")
    problems = []
    results = {}

    for dataset_kind, paths in FILES.items():
        print(f"\n{dataset_kind.upper()}")
        results[dataset_kind] = {}
        for split, path in paths.items():
            data = read_jsonl(path, dataset_kind, problems)
            results[dataset_kind][split] = data
            if data is None:
                print(f"  {split:5}: DOSYA BULUNAMADI ({path.relative_to(ROOT)})")
                continue
            expected = EXPECTED[dataset_kind][split]
            mark = "OK" if data["count"] == expected else "KONTROL"
            print(f"  {split:5}: {data['count']:5} kayit | beklenen {expected:5} | {mark}")
            if data["count"] != expected:
                problems.append(f"{dataset_kind}/{split}: kayit sayisi beklenenden farkli")

        items = results[dataset_kind]
        if all(items.get(key) is not None for key in ("train", "val", "test")):
            splits = ("train", "val", "test")
            for i in range(3):
                for j in range(i + 1, 3):
                    a, b = splits[i], splits[j]
                    id_overlap = items[a]["ids"] & items[b]["ids"]
                    src_overlap = items[a]["sources"] & items[b]["sources"]
                    if id_overlap:
                        problems.append(f"{dataset_kind}: {a}/{b} arasinda {len(id_overlap)} ortak ID")
                    if src_overlap:
                        problems.append(f"{dataset_kind}: {a}/{b} arasinda {len(src_overlap)} ortak kaynak belge")

            if items.get("full") is not None:
                all_ids = set().union(*(items[s]["ids"] for s in splits))
                if all_ids != items["full"]["ids"]:
                    missing = len(items["full"]["ids"] - all_ids)
                    extra = len(all_ids - items["full"]["ids"])
                    problems.append(f"{dataset_kind}: tam dosya ile split ID'leri uyusmuyor (eksik {missing}, fazla {extra})")

    corpus = results["corpus"]
    instruction = results["instruction"]
    if all(corpus.get(s) and instruction.get(s) for s in ("train", "val", "test")):
        print("\nCORPUS-INSTRUCTION KAYNAK ESLESMESI")
        for split in ("train", "val", "test"):
            ins_sources = instruction[split]["sources"]
            corp_sources = corpus[split]["sources"]
            missing = ins_sources - corp_sources
            print(f"  {split:5}: {len(ins_sources)} instruction kaynagi, eslesmeyen {len(missing)}")
            if missing:
                problems.append(f"{split}: {len(missing)} instruction kaynagi ayni corpus bolmesinde bulunamadi")
            other_sources = set().union(*(corpus[s]["sources"] for s in ("train", "val", "test") if s != split))
            leakage = ins_sources & other_sources
            if leakage:
                problems.append(f"{split}: {len(leakage)} instruction kaynagi farkli corpus bolmesinde de var")

    print("\nSONUC")
    if problems:
        print(f"KONTROL GEREKIYOR: {len(problems)} bulgu")
        for p in problems[:30]:
            print(" -", p)
        if len(problems) > 30:
            print(f" ... ve {len(problems)-30} bulgu daha")
        print("Not: Bu kontrol anlamsal dogruluk ve near-duplicate incelemesi yapmaz.")
        return 1
    print("TEKNIK KONTROL GECTI: sayilar, JSON, ID ve kaynak bazli bolmeler uyumlu.")
    print("Not: Anlamsal dogruluk, kaynak lisanslari ve near-duplicate incelemesi ayrica gereklidir.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
