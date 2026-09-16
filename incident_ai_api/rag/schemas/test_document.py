from rag.schemas.document import DocumentMetadata
 
 
metadata = DocumentMetadata(
    file_name="PX-500_manual_v3.2.txt",
    machine_model="PX-500",
    manual_version="3.2",
    document_type="MANUAL",
    section="High Temperature Alarm",
    page=1,
)
 
print(metadata)