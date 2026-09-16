from rag.retrieval.retriever import Retriever
from rag.retrieval.citations import create_citation
 
 
retriever = Retriever()
 
 
results = retriever.search(
    query="What should I check for high temperature?",
    top_k=1,
    machine_model="PX-500",
    manual_version="3.2",
)
 
 
if results:
 
    citation = create_citation(results[0])
 
    print("CITATION")
    print("=" * 50)
 
    print(f"Source: {citation['source']}")
    print(f"Model: {citation['machine_model']}")
    print(f"Version: {citation['manual_version']}")
    print(f"Section: {citation['section']}")
    print(f"Chunk ID: {citation['chunk_id']}")
 
else:
 
    print("No evidence found.")