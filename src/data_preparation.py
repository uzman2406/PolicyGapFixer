import PyPDF2
import re
from typing import List, Dict
import json

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        
    def extract_text(self) -> str:
        """Extract text from PDF"""
        text = ""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[Dict]:
        """Split text into manageable chunks"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length > chunk_size and current_chunk:
                chunks.append({
                    'text': ' '.join(current_chunk),
                    'chunk_id': len(chunks)
                })
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:
            chunks.append({
                'text': ' '.join(current_chunk),
                'chunk_id': len(chunks)
            })
        
        return chunks


if __name__ == "__main__":
    extractor = PDFExtractor("../data/cis-ms-isac-nist-cybersecurity-framework-policy-template-guide-2024.pdf")
    text = extractor.extract_text()
    chunks = extractor.chunk_text(text)
    
    # Save chunks
    with open("../data/reference_chunks.json", "w") as f:
        json.dump(chunks, f, indent=2)
    
    print(f"Extracted {len(chunks)} chunks")