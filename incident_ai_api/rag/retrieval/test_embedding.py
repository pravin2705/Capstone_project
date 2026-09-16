from rag.retrieval.embedding import (
    SimpleEmbeddingModel,
    cosine_similarity,
)
 
 
model = SimpleEmbeddingModel()
 
texts = [
    "Check cooling water flow for high temperature alarm.",
    "Inspect bearing temperature and lubrication.",
    "Check shaft alignment for vibration alarm.",
]
 
vocabulary, vectors = model.embed_documents(texts)
 
query = "high temperature cooling water"
 
query_vector = model.embed_text(
    query,
    vocabulary,
)
 
print("Vocabulary size:", len(vocabulary))
 
print("\nEmbedding dimension:", len(query_vector))
 
print("\nSimilarity scores:")
 
for text, vector in zip(texts, vectors):
 
    score = cosine_similarity(
        query_vector,
        vector,
    )
 
    print(f"{score:.4f} -> {text}")