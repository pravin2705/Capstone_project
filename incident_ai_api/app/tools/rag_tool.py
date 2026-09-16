from typing import Any
 
from rag.retrieval.retriever import Retriever
 
 
class RAGKnowledgeTool:
    """
    Week 3 wrapper around the Week 2 RAG retriever.
    """
 
    def __init__(self):
        self.retriever = Retriever()
 
    def search_knowledge(
        self,
        query: str,
        machine_model: str,
        manual_version: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search maintenance knowledge using
        machine model and manual version.
        """
 
        results = self.retriever.search(
            query=query,
            top_k=3,
            machine_model=machine_model,
            manual_version=manual_version,
        )
 
        return results