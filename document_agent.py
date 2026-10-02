import os
import re
from typing import Dict, List, Any
from pypdf import PdfReader


class DocumentProcessingAgent:
    """
    Member 2: Document Processing Agent for StudyLens AI
    Extracts text from uploaded study materials, cleans noise,
    and produces structured chunks for downstream AI agents.
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def clean_text(self, text: str) -> str:
        """Removes extra whitespaces, noisy line breaks, and page header artifacts."""
        if not text:
            return ""
        # Newlines aur multiple spaces ko normalize karna
        text = re.sub(r"\r\n|\r", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def chunk_text(self, text: str, page_number: int = 1) -> List[Dict[str, Any]]:
        """Divides large content into overlapping chunks with metadata."""
        chunks = []
        start = 0
        text_length = len(text)
        chunk_idx = 1

        while start < text_length:
            end = start + self.chunk_size
            chunk_content = text[start:end]

            chunks.append({
                "chunk_id": chunk_idx,
                "page": page_number,
                "text": chunk_content.strip(),
                "char_length": len(chunk_content.strip())
            })

            # Overlap ke sath aage shift karna
            start += self.chunk_size - self.chunk_overlap
            chunk_idx += 1

        return chunks

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Main entry point for Member 1 (Orchestrator).
        Reads PDF, cleans content, and generates unified payload.
        """
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"File not found at path: {file_path}",
                "total_pages": 0,
                "full_text": "",
                "chunks": []
            }

        try:
            reader = PdfReader(file_path)
            total_pages = len(reader.pages)
            full_cleaned_text = []
            all_chunks = []

            for page_idx, page in enumerate(reader.pages, start=1):
                raw_page_text = page.extract_text() or ""
                cleaned_page_text = self.clean_text(raw_page_text)

                if cleaned_page_text:
                    full_cleaned_text.append(cleaned_page_text)
                    page_chunks = self.chunk_text(cleaned_page_text, page_number=page_idx)
                    all_chunks.extend(page_chunks)

            combined_text = "\n\n".join(full_cleaned_text)

            # Global chunk IDs assign karna
            for idx, c in enumerate(all_chunks, start=1):
                c["chunk_id"] = idx

            return {
                "status": "success",
                "file_name": os.path.basename(file_path),
                "total_pages": total_pages,
                "total_characters": len(combined_text),
                "total_chunks": len(all_chunks),
                "full_text": combined_text,
                "chunks": all_chunks
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to parse document: {str(e)}",
                "total_pages": 0,
                "full_text": "",
                "chunks": []
            }


# --- Local Standalone Test ---
if __name__ == "__main__":
    agent = DocumentProcessingAgent(chunk_size=800, chunk_overlap=100)
    
    # Aapke project folder mein maujood file:
    sample_pdf = "SC & D Lab Manual 02.pdf"
    
    if os.path.exists(sample_pdf):
        print(f"Reading file: {sample_pdf}...")
        result = agent.process_document(sample_pdf)
        
        print("\n--- Processing Results ---")
        print("Status:", result["status"])
        print("File Name:", result["file_name"])
        print("Total Pages:", result["total_pages"])
        print("Total Characters Extracted:", result["total_characters"])
        print("Total Chunks Created:", result["total_chunks"])
        
        if result["chunks"]:
            print("\n--- Preview of Chunk 1 ---")
            print("Chunk ID:", result["chunks"][0]["chunk_id"])
            print("Page Number:", result["chunks"][0]["page"])
            print("Character Length:", result["chunks"][0]["char_length"])
            print("Text Content:\n", result["chunks"][0]["text"][:300] + "...")
    else:
        print(f"Error: '{sample_pdf}' file folder mein nahi mili. Name verify karein.")