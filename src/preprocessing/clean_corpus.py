import os
from glob import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.preprocessing.pipeline import preprocess_to_string

RAW_TEXT_BASE = "data/raw_text"
OUT_BASE = "data/processed"

os.makedirs(OUT_BASE, exist_ok=True)

def process_category(cat):
    raw_dir = os.path.join(RAW_TEXT_BASE, cat)
    out_dir = os.path.join(OUT_BASE, cat)
    
    os.makedirs(out_dir, exist_ok=True)
    
    files = glob(os.path.join(raw_dir, "*.txt"))

    print(f"[INFO] Processing {len(files)} files for {cat}...")

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                raw_content = f.read()
            
            text = preprocess_to_string(raw_content)

            if text:
                filename = os.path.basename(fpath)
                out_file_path = os.path.join(out_dir, filename)
                
                with open(out_file_path, "w", encoding="utf-8") as f_out:
                    f_out.write(text)

        except Exception as e:
            print(f"[ERROR] Failed to process {fpath}: {e}")

    print(f"[INFO] Saved processed files to {out_dir}")

def main():
    process_category("gaza")
    process_category("ukraine")
    print("[DONE] Corpus cleaned and built!")

if __name__ == "__main__":
    main()