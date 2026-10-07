import faiss
import json

def create_index(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index

def save_index(index, file_path):
    faiss.write_index(index, file_path)

def save_chunks(chunks, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

def load_index(file_path):
    return faiss.read_index(str(file_path))

def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)