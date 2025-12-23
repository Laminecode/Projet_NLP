import os
from functions import (
    extract_article, read_links,
     save_json
)

LINKS_FILE = "./data/ukraine_links.txt"
OUTPUT_DIR = "./data/raw/ukraine"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def main_ukrain():
    links = read_links(LINKS_FILE)
    print(f"[INFO] Found {len(links)} Ukraine links")
    statistics = {"total": len(links), "successful": 0, "failed": 0, "details": {}}
    for url in links:
        article = extract_article(url, LINKS_FILE)
        if article:
            save_json(article, OUTPUT_DIR)
            statistics["successful"] += 1
            media = article["media"]
            if media in statistics["details"]:
                statistics["details"][media] += 1
            else:
                 statistics["details"][media] = 1
        else:
            statistics["failed"] += 1
    print(f"[INFO] Scraping completed. Successful:",statistics)
    return statistics
