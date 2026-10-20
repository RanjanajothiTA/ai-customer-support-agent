from pathlib import Path

from app.rag.embeddings import model
from app.rag.vector_store import load_index, load_chunks


VECTOR_STORE_PATH = Path(__file__).parent.parent.parent / "data" / "vector_store"

INDEX_PATH = VECTOR_STORE_PATH / "shopease.index"
CHUNKS_PATH = VECTOR_STORE_PATH / "chunks.json"


index = load_index(INDEX_PATH)
chunks = load_chunks(CHUNKS_PATH)



def search(query, top_k=3, max_distance=None):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_value in zip(distances[0], indices[0]):
        # FAISS can return -1 when there are not enough indexed items.
        if index_value < 0:
            continue

        distance = float(distance)

        # Skip chunks that are too far from the query.
        if max_distance is not None and distance > max_distance:
            continue

        results.append({
            "chunk": chunks[index_value],
            "distance": distance
        })

    return results
