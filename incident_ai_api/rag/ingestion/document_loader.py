from pathlib import Path
 
from rag.ingestion.metadata_builder import build_metadata
 
 
DOCUMENTS_DIR = Path("rag/documents")
 
 
def load_documents():
 
    documents = []
 
    for file_path in DOCUMENTS_DIR.glob("*.txt"):
 
        text = file_path.read_text(encoding="utf-8")
 
        metadata = build_metadata(file_path.name)
 
        documents.append(
            {
                "file_name": file_path.name,
                "text": text,
                "metadata": metadata,
            }
        )
 
    return documents
 
 
if __name__ == "__main__":
 
    documents = load_documents()
 
    print(f"Loaded documents: {len(documents)}")
 
    for document in documents:
 
        print("-" * 60)
 
        print(f"File: {document['file_name']}")
 
        print(f"Characters: {len(document['text'])}")
 
        print(f"Metadata: {document['metadata']}")