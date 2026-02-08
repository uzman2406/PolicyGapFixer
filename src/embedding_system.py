import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from typing import List, Dict

class VectorStore:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.dimension = 384  
        
    def create_embeddings(self, chunks: List[Dict]) -> np.ndarray:
        """Create embeddings for text chunks"""
        texts = [chunk['text'] for chunk in chunks]
        self.chunks = chunks
        
        print("Creating embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
       
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings.astype('float32'))
        
        return embeddings
    
    def save_index(self, index_path: str, chunks_path: str):
        """Save FAISS index and chunks"""
        faiss.write_index(self.index, index_path)
        with open(chunks_path, 'wb') as f:
            pickle.dump(self.chunks, f)
    
    def load_index(self, index_path: str, chunks_path: str):
        """Load FAISS index and chunks"""
        self.index = faiss.read_index(index_path)
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar chunks"""
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.chunks):
                results.append({
                    'chunk': self.chunks[idx],
                    'score': float(distances[0][i])
                })
        
        return results