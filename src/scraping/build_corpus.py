import os
import json
import hashlib
from glob import glob
from scrape_ukrain import (main_ukrain)
from scrape_gaza import (main_gaza)

RAW_BASE = "data/raw"
OUT_BASE = "data/raw_text"

os.makedirs(OUT_BASE, exist_ok=True)

def normalize(text):
    return " ".join(text.split()).strip()

def hash_text(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()

def process_category(cat):
    raw_dir = os.path.join(RAW_BASE, cat)
    out_dir = os.path.join(OUT_BASE, cat)
    os.makedirs(out_dir, exist_ok=True)

    files = glob(os.path.join(raw_dir, "*.json"))
    seen_hashes = set()
    saved = 0

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            obj = json.load(f)

        text = normalize(obj.get("content", ""))


        h = hash_text(text)
        if h in seen_hashes:
            continue

        seen_hashes.add(h)
        article_id = obj.get("id") or abs(hash(obj["url"]))
        out_path = os.path.join(out_dir, f"{article_id}.txt")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

        saved += 1

    print(f"[INFO] Saved {saved} cleaned TXT files for {cat}")

def main():
    main_gaza()
    main_ukrain()
    process_category("gaza")
    process_category("ukraine")
    print("[DONE] Corpus built!")

if __name__ == "__main__":
    main()
