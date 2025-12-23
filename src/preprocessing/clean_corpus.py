import os
from glob import glob
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from pipeline import preprocess_to_string

def process_category(cat, raw_base="data/raw_text", out_base="data/processed_clean"):
    raw_dir = os.path.join(raw_base, cat)
    out_dir = os.path.join(out_base, cat)
    
    os.makedirs(out_dir, exist_ok=True)
    
    files = glob(os.path.join(raw_dir, "*.txt"))

    if not files:
        print(f"[WARNING] No files found in {raw_dir}")
        return

    print(f"[INFO] Processing {len(files)} files for category '{cat}'...")
    successful = 0
    failed = 0

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                raw_content = f.read()
            
            # Preprocess
            text = preprocess_to_string(raw_content)

            if text:
                filename = os.path.basename(fpath)
                out_file_path = os.path.join(out_dir, filename)
                
                with open(out_file_path, "w", encoding="utf-8") as f_out:
                    f_out.write(text)
                
                successful += 1
            else:
                print(f"[WARNING] No tokens after preprocessing: {os.path.basename(fpath)}")

        except Exception as e:
            failed += 1
            print(f"[ERROR] Failed to process {fpath}: {e}")

    print(f"[INFO] Category '{cat}': {successful} successful, {failed} failed")
    print(f"[INFO] Saved processed files to {out_dir}")


def main():
    categories = ["gaza", "ukraine"]
    
    for cat in categories:
        process_category(cat)
    
    print("[DONE] Corpus cleaned and built!")


if __name__ == "__main__":
    main()
