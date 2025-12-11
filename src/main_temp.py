import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.scraping.build_corpus import main as build_corpus_main
from src.preprocessing.clean_corpus import main as clean_corpus_main

def main():
    print("Scraping and Corpus Building")
    try:
        build_corpus_main()
    except Exception as e:
        print(f"[ERROR] Scraping failed: {e}")
    
    print("\nPreprocessing")
    try:
        clean_corpus_main()
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")

    print("\nAll Tasks Completed")

if __name__ == "__main__":
    main()