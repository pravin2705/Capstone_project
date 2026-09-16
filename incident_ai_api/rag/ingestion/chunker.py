import re
 
from rag.schemas.document import DocumentChunk
 
 
def find_section(text: str):
    """
    Find the section name from the text.
    """
 
    match = re.search(
        r"Section\s+\d+:\s*(.+)",
        text,
        re.IGNORECASE,
    )
 
    if match:
        return match.group(1).strip()
 
    return None
 
 
def chunk_document(
    text: str,
    metadata,
    chunk_size: int = 500,
    overlap: int = 50,
):
    chunks = []
 
    start = 0
    chunk_number = 1
 
    current_section = None
 
    while start < len(text):
 
        end = start + chunk_size
 
        chunk_text = text[start:end].strip()
 
        if chunk_text:
 
            detected_section = find_section(chunk_text)
 
            if detected_section:
                current_section = detected_section
 
            chunk_metadata = metadata.model_copy(
                update={
                    "section": current_section
                }
            )
 
            chunk = DocumentChunk(
                chunk_id=f"{metadata.file_name}_{chunk_number}",
                text=chunk_text,
                metadata=chunk_metadata,
            )
 
            chunks.append(chunk)
 
        start = end - overlap
        chunk_number += 1
 
    return chunks