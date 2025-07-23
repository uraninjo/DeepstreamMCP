import os
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

TXT_DIR = "docs_txt"
CHROMA_DB_DIR = "chroma_db"

os.makedirs(TXT_DIR, exist_ok=True)
os.makedirs(CHROMA_DB_DIR, exist_ok=True)
# OpenAI veya benzeri bir gömücü kullanmak için örnek (yerel gömücü de kullanılabilir)
# Burada örnek olarak Chroma'nın default SentenceTransformer gömücüsü kullanılıyor
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/e5-base-v2")#all-MiniLM-L6-v2

client = PersistentClient(path=CHROMA_DB_DIR)

collection = client.get_or_create_collection(
    name="deepstream_docs",
    embedding_function=embedding_func
)

def get_txt_files():
    txt_files = []
    for root, _, files in os.walk(TXT_DIR):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def main():
    txt_files = get_txt_files()
    for path in txt_files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        doc_id = os.path.relpath(path, TXT_DIR)
        # Chroma'da id benzersiz olmalı
        collection.add(
            documents=[text],
            ids=[doc_id]
        )
        print(f"Vektörlendi: {doc_id}")
    print("Tüm dokümanlar vektör veritabanına eklendi.")

if __name__ == "__main__":
    main()
