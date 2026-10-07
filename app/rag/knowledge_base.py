from document_loader import load_pdf, KNOWLEDGE_BASE_PATH
from chunker import chunk_text


def load_knowledge_base():
    all_chunks = []

    pdf_files = KNOWLEDGE_BASE_PATH.glob("*.pdf")

    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path.name}")
        text = load_pdf(pdf_path)
        chunks = chunk_text(text, source=pdf_path.name)
        all_chunks.extend(chunks)

    return all_chunks