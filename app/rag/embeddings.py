from sentence_transformers import SentenceTransformer
model_name="all-MiniLM-L6-v2"
model=SentenceTransformer(model_name)
def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    return embeddings