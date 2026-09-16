from app.tools.rag_tool import RAGKnowledgeTool
 
 
def test_rag_tool():
 
    tool = RAGKnowledgeTool()
 
    results = tool.search_knowledge(
        query="High Temperature Alarm",
        machine_model="PX-500",
        manual_version="3.2",
    )
 
    assert isinstance(results, list)