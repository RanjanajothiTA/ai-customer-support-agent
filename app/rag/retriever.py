from pathlib import Path

from rag.embeddings import model
from rag.vector_store import load_index, load_chunks


VECTOR_STORE_PATH = Path(__file__).parent.parent.parent / "data" / "vector_store"

INDEX_PATH = VECTOR_STORE_PATH / "shopease.index"
CHUNKS_PATH = VECTOR_STORE_PATH / "chunks.json"


index = load_index(INDEX_PATH)
chunks = load_chunks(CHUNKS_PATH)


def search(query, top_k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_value in zip(distances[0], indices[0]):
        results.append({
            "chunk": chunks[index_value],
            "distance": float(distance)
        })

    return results