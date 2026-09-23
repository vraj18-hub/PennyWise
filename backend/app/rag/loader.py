from pathlib import Path

from app.rag.chunking import chunk_text

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "data" / "knowledge_base"


def load_and_chunk_documents() -> list[dict]:
    """
    Reads every .txt file in the knowledge base folder, splits each into
    chunks, and returns a list of dicts with the chunk text and its source.
    """
    all_chunks = []

    for file_path in KNOWLEDGE_BASE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text, chunk_size=400, overlap=60)

        for i, chunk in enumerate(chunks):
            all_chunks.append(
                {
                    "id": f"{file_path.stem}_{i}",
                    "text": chunk,
                    "source": file_path.name,
                }
            )

    return all_chunks