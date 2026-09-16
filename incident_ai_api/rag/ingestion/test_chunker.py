from rag.ingestion.document_loader import load_documents
from rag.ingestion.chunker import chunk_document
 
 
documents = load_documents()
 
for document in documents:
 
    chunks = chunk_document(
        text=document["text"],
        metadata=document["metadata"],
    )
 
    print("=" * 70)
 
    print(f"Document: {document['file_name']}")
 
    print(f"Number of chunks: {len(chunks)}")
 
    for chunk in chunks:
 
        print("-" * 70)
 
        print(f"Chunk ID: {chunk.chunk_id}")
 
        print(f"Text:\n{chunk.text[:200]}")
 
        print(f"Model: {chunk.metadata.machine_model}")
 
        print(f"Version: {chunk.metadata.manual_version}")