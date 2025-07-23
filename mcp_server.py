from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any
import chromadb
from chromadb import PersistentClient
from chromadb.utils import embedding_functions

CHROMA_DB_DIR = "chroma_db"
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/e5-base-v2")
client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection(
    name="deepstream_docs",
    embedding_function=embedding_func
)

mcp = FastMCP("deepstream_docs")

@mcp.tool()
def search_docs(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """Search documents in the Deepstream collection.
    Args:
        query: Text to search for.
        n_results: Number of results to return.
    Returns:
        List of dicts with 'id' and 'text'.
    """
    results = collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]
    return [{"id": i, "text": d} for i, d in zip(ids, docs)]

@mcp.tool()
def count_docs() -> Dict[str, int]:
    """Count the number of documents in the Deepstream collection.
    Returns:
        Dict with 'count' key.
    """
    return {"count": collection.count()}

@mcp.tool()
def sample_doc() -> Dict[str, Any]:
    """Get a sample document from the Deepstream collection.
    Returns:
        Dict with 'id' and 'text'.
    """
    results = collection.get(limit=1)
    docs = results.get("documents", [])
    ids = results.get("ids", [])
    return {"id": ids[0] if ids else None, "text": docs[0] if docs else None}

if __name__ == "__main__":
    mcp.run(transport="stdio")
