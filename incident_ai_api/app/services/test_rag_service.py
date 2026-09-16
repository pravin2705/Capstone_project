from app.services.rag_service import RAGService
 
 
rag_service = RAGService()
 
 
results = rag_service.get_maintenance_guidance(
    query="What should I check for a high temperature alarm?",
    machine_model="PX-500",
    manual_version="3.2",
)
 
 
print("=" * 70)
print("MAINTENANCE GUIDANCE")
print("=" * 70)
 
 
if not results:
 
    print("No maintenance evidence found.")
 
else:
 
    for index, result in enumerate(results, start=1):
 
        print()
        print(f"Evidence {index}")
        print("-" * 70)
 
        print(
            f"Score: "
            f"{result['score']:.4f}"
        )
 
        print("\nText:")
        print(result["text"])
 
        print("\nCitation:")
 
        citation = result["citation"]
 
        print(
            f"Source: {citation['source']}"
        )
 
        print(
            f"Model: {citation['machine_model']}"
        )
 
        print(
            f"Version: {citation['manual_version']}"
        )
 
        print(
            f"Section: {citation['section']}"
        )