import json
from embedding_system import VectorStore
from data_preparation import PDFExtractor
import os

def build_knowledge_base():
    # Extract text from PDF
    pdf_path = "../data/cis-ms-isac-nist-cybersecurity-framework-policy-template-guide-2024.pdf"
    extractor = PDFExtractor(pdf_path)
    text = extractor.extract_text()
    
    # Chunk the text
    chunks = extractor.chunk_text(text, chunk_size=500)
    
    # Create embeddings
    vector_store = VectorStore()
    embeddings = vector_store.create_embeddings(chunks)
    
    # Save index
    os.makedirs("../models", exist_ok=True)
    vector_store.save_index(
        "../models/faiss_index.bin",
        "../models/chunks.pkl"
    )
    
    print(f"Knowledge base created with {len(chunks)} chunks")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    
    # Also save text chunks for reference
    with open("../data/reference_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)
    
    return vector_store

if __name__ == "__main__":
    build_knowledge_base()