
import os
from readability import Document
from bs4 import BeautifulSoup

DOCS_DIR = "docs"
TXT_DIR = "docs_txt"

os.makedirs(TXT_DIR, exist_ok=True)

def html_to_text(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    doc = Document(html)
    main_html = doc.summary()
    title = doc.title()
    soup = BeautifulSoup(main_html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return f"{title}\n\n{text}"

def main():
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".html"):
                html_path = os.path.join(root, file)
                rel_path = os.path.relpath(html_path, DOCS_DIR)
                txt_path = os.path.join(TXT_DIR, rel_path[:-5] + ".txt")
                os.makedirs(os.path.dirname(txt_path), exist_ok=True)
                text = html_to_text(html_path)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Converted {html_path} -> {txt_path}")

if __name__ == "__main__":
    main()
