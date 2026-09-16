from rag.retrieval.retriever import Retriever
from rag.retrieval.citations import create_citation
 
 
class RAGService:
 
    def __init__(self):
        self.retriever = Retriever()
 
    def get_maintenance_guidance(
        self,
        query: str,
        machine_model: str,
        manual_version: str,
    ):
 
        results = self.retriever.search(
            query=query,
            top_k=3,
            machine_model=machine_model,
            manual_version=manual_version,
        )
 
        evidence = []
 
        for result in results:
 
            evidence.append(
                {
                    "text": result["text"],
                    "score": result["score"],
                    "citation": create_citation(result),
                }
            )
 
        return evidence