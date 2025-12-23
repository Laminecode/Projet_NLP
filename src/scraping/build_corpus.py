import os
import json
import hashlib
from glob import glob
from scrape_ukrain import main_ukrain
from scrape_gaza import main_gaza

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
    duplicates = 0
    errors = 0
    
    stats = {
        "total_files": len(files),
        "saved": 0,
        "duplicates": 0,
        "errors": 0,
        "word_counts": []
    }

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                obj = json.load(f)

            text = normalize(obj.get("content", ""))
            
            if len(text.split()) < 100:  # Minimum word count
                print(f"[WARNING] Skipping short article: {fpath}")
                errors += 1
                continue

            h = hash_text(text)
            if h in seen_hashes:
                duplicates += 1
                continue

            seen_hashes.add(h)
            article_id = obj.get("id") or abs(hash(obj["url"]))
            out_path = os.path.join(out_dir, f"{article_id}.txt")

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

            saved += 1
            stats["word_counts"].append(len(text.split()))
            
        except Exception as e:
            print(f"[ERROR] Failed processing {fpath}: {e}")
            errors += 1

    stats["saved"] = saved
    stats["duplicates"] = duplicates
    stats["errors"] = errors
    stats["avg_words"] = sum(stats["word_counts"]) / len(stats["word_counts"]) if stats["word_counts"] else 0
    
    print(f"[INFO] {cat}: Saved={saved}, Duplicates={duplicates}, Errors={errors}, Avg Words={stats['avg_words']:.0f}")
    
    # Save statistics
    with open(os.path.join(out_dir, "_stats.json"), "w") as f:
        json.dump(stats, f, indent=2)
    
    return stats

def main():
    result_g = main_gaza()
    result_u = main_ukrain()
    process_category("gaza")
    process_category("ukraine")
    #save overall stats
    overall_stats = {
        "gaza": result_g,
        "ukraine": result_u 
    }
    with open(os.path.join(OUT_BASE, "_overall_stats.json"), "w") as f:
        json.dump(overall_stats, f, indent=2)

    print("[DONE] Corpus built!")

if __name__ == "__main__":
    main()
