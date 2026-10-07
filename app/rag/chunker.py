def chunk_text(text, source, chunk_size=700, overlap=200):
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append({
            "text": chunk,
            "source": source,
            "chunk_id": chunk_id
        })

        chunk_id += 1
        start = end - overlap

    return chunks