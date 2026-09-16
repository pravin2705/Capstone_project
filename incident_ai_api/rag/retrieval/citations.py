def create_citation(result: dict):
 
    metadata = result["metadata"]
 
    return {
        "source": metadata["file_name"],
        "machine_model": metadata["machine_model"],
        "manual_version": metadata["manual_version"],
        "section": metadata["section"],
        "chunk_id": result["chunk_id"],
    }