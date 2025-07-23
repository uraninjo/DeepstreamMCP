import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://docs.nvidia.com/metropolis/deepstream/dev-guide/"
DOCS_DIR = "docs"

visited = set()

def is_valid_link(href):
    if not href:
        return False
    # Sadece aynı domain ve html dosyaları
    if href.startswith("#") or href.startswith("mailto:"):
        return False
    if href.startswith("http") and not href.startswith(BASE_URL):
        return False
    if not (href.endswith(".html") or href.endswith("/")):
        return False
    return True

def get_local_path(url):
    rel_path = url.replace(BASE_URL, "")
    if rel_path == "" or rel_path.endswith("/"):
        rel_path += "index.html"
    return os.path.join(DOCS_DIR, rel_path)

def download_and_crawl(url):
    if url in visited:
        return
    visited.add(url)
    local_path = get_local_path(url)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print(f"Downloading {url} -> {local_path}")
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Failed to download {url}: {resp.status_code}")
            return
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a"):
            href = link.get("href")
            if is_valid_link(href):
                next_url = urljoin(url, href)
                # Sadece BASE_URL ile başlayanları takip et
                if next_url.startswith(BASE_URL):
                    download_and_crawl(next_url)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    download_and_crawl(BASE_URL + "index.html")

if __name__ == "__main__":
    main()
