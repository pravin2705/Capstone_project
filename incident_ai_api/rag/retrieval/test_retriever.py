from rag.retrieval.retriever import Retriever
 
 
retriever = Retriever()
 
 
query = "What should I check for a high temperature alarm?"
 
 
results = retriever.search(
    query=query,
    top_k=3,
    machine_model="PX-500",
    manual_version="3.2",
)
 
 
print("=" * 70)
 
print("QUERY:")
print(query)
 
print("\nFILTER:")
print("Machine Model: PX-500")
print("Manual Version: 3.2")
 
print("\nRETRIEVED EVIDENCE:")
 
print("=" * 70)
 
 
for result in results:
 
    metadata = result["metadata"]
 
    print("-" * 70)
 
    print(f"Score: {result['score']:.4f}")
 
    print(f"Chunk ID: {result['chunk_id']}")
 
    print(f"Model: {metadata['machine_model']}")
 
    print(f"Version: {metadata['manual_version']}")
 
    print(f"Section: {metadata['section']}")
 
    print(f"Source: {metadata['file_name']}")
 
    print("\nEvidence:")
 
    print(result["text"])