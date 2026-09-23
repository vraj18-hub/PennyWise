from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

_client = chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    return _client.get_or_create_collection(
        name="finance_knowledge",
        embedding_function=_embedding_fn,
    )

def search(query: str, n_results: int = 3) -> list[dict]:
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)

    matches = []
    for text, distance, metadata in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ):
        matches.append(
            {
                "text": text,
                "distance": distance,
                "source": metadata.get("source", "unknown"),
            }
        )

    return matches