import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ProjectNLPBot/1.0)"
}

def read_links(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
    
def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")


def remove_link_from_file(link, filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # keep only the lines that are not the link
        new_lines = [l for l in lines if l.strip() != link]

        with open(filename, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(f"[INFO] Removed bad link from {filename} : {link}")

    except Exception as e:
        print(f"[ERROR] Failed to remove link: {e}")


def extract_article(url, LINKS_FILE):
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Cannot fetch {url}: {e}")
        remove_link_from_file(url, LINKS_FILE)
        return None
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {url}: {e}")
        return None 

    soup = BeautifulSoup(r.text, "html.parser")

    # Title
    title = ""
    if soup.title:
        title = soup.title.get_text().strip()

    # Extract paragraphs
    paragraphs = [p.get_text().strip() for p in soup.find_all("p")]
    paragraphs = [p for p in paragraphs if len(p) > 0]

    content = "\n".join(paragraphs)

    if len(content.split()) < 150:
        print(f"[WARNING] Content too short for {url}")
        remove_link_from_file(url, LINKS_FILE)
        return None
    return {    
        "url": url,
        "media": get_domain(url),
        "title": title,
        "content": content,
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }


def save_json(article, OUTPUT_DIR):
    article_id = abs(hash(article["url"]))
    path = os.path.join(OUTPUT_DIR, f"{article_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved {path}")

