from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

_client = None
_embedding_fn = None


def _get_client():
    global _client
    if _client is None:
        import chromadb
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


def _get_embedding_fn():
    global _embedding_fn
    if _embedding_fn is None:
        from chromadb.utils import embedding_functions
        _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedding_fn


def get_collection():
    return _get_client().get_or_create_collection(
        name="finance_knowledge",
        embedding_function=_get_embedding_fn(),
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