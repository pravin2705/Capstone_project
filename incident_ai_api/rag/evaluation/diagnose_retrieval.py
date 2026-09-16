from rag.retrieval.retriever import Retriever
 
 
retriever = Retriever()
 
 
query = "What routine maintenance should be performed on the pump?"
 
results = retriever.search(
    query=query,
    top_k=3,
    machine_model="PX-500",
    manual_version="3.2",
)
 
 
print("=" * 70)
print("RETRIEVAL DIAGNOSTIC")
print("=" * 70)
 
print()
print("Query:")
print(query)
 
print()
print("Model: PX-500")
print("Version: 3.2")
 
print()
print("=" * 70)
print("TOP 3 RETRIEVED RESULTS")
print("=" * 70)
 
 
for index, result in enumerate(results, start=1):
 
    print()
    print(f"RESULT {index}")
    print("-" * 70)
 
    print(f"Score   : {result['score']:.4f}")
 
    print(
        f"Section : "
        f"{result['metadata']['section']}"
    )
 
    print(
        f"Source  : "
        f"{result['metadata']['file_name']}"
    )
 
    print()
    print("Text:")
    print(result["text"])