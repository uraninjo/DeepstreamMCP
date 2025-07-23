from fastapi import FastAPI, Query
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

app = FastAPI()
CHROMA_DB_DIR = "chroma_db"

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/e5-base-v2")
client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(
    name="deepstream_docs",
    embedding_function=embedding_func
)

@app.get("/search")
def search_docs(query: str = Query(..., description="Aranacak metin"), n_results: int = 5):
    results = collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]
    return [{"id": i, "text": d} for i, d in zip(ids, docs)]

@app.get("/count")
def count_docs():
    return {"count": collection.count()}

@app.get("/sample")
def sample_doc():
    results = collection.get(limit=1)
    docs = results.get("documents", [])
    ids = results.get("ids", [])
    return {"id": ids[0] if ids else None, "text": docs[0] if docs else None}
