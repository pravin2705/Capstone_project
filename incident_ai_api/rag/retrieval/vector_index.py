import json
from pathlib import Path
 
from rag.ingestion.document_loader import load_documents
from rag.ingestion.chunker import chunk_document
from rag.retrieval.embedding import SimpleEmbeddingModel
 
 
INDEX_FILE = Path("rag/retrieval/vector_index.json")
 
 
def build_index():
 
    # Step 1: Load documents
    documents = load_documents()
 
    all_chunks = []
 
    # Step 2: Create chunks
    for document in documents:
 
        chunks = chunk_document(
            text=document["text"],
            metadata=document["metadata"],
        )
 
        all_chunks.extend(chunks)
 
    # Step 3: Create embedding model
    embedding_model = SimpleEmbeddingModel()
 
    # Step 4: Get chunk texts
    texts = [
        chunk.text
        for chunk in all_chunks
    ]
 
    # Step 5: Generate embeddings
    vocabulary, vectors = embedding_model.embed_documents(texts)
 
    # Step 6: Create index records
    index_data = {
        "vocabulary": vocabulary,
        "chunks": [],
    }
 
    for chunk, vector in zip(all_chunks, vectors):
 
        index_data["chunks"].append(
            {
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "metadata": chunk.metadata.model_dump(),
                "vector": vector,
            }
        )
 
    # Step 7: Save index
    INDEX_FILE.write_text(
        json.dumps(index_data, indent=2),
        encoding="utf-8",
    )
 
    print(f"Index created successfully.")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Vocabulary size: {len(vocabulary)}")
    print(f"Index file: {INDEX_FILE}")
 
 
if __name__ == "__main__":
    build_index()