import re
 
from rag.schemas.document import DocumentMetadata
 
 
def build_metadata(file_name: str) -> DocumentMetadata:
 
    # Check whether this is a pump manual
    manual_match = re.search(
        r"(PX-\d+)_manual_v([\d.]+)",
        file_name,
        re.IGNORECASE,
    )
 
    # Check whether this is an SOP
    sop_match = re.search(
        r"_sop_v([\d.]+)",
        file_name,
        re.IGNORECASE,
    )
 
    if manual_match:
        machine_model = manual_match.group(1).upper()
        manual_version = manual_match.group(2)
        document_type = "MANUAL"
 
    elif sop_match:
        machine_model = None
        manual_version = sop_match.group(1)
        document_type = "SOP"
 
    else:
        machine_model = None
        manual_version = None
        document_type = "UNKNOWN"
 
    return DocumentMetadata(
        file_name=file_name,
        machine_model=machine_model,
        manual_version=manual_version,
        document_type=document_type,
    )
 
 
if __name__ == "__main__":
 
    test_files = [
        "PX-500_manual_v3.2.txt",
        "PX-700_manual_v2.1.txt",
        "pump_alarm_sop_v1.0.txt",
    ]
 
    for file_name in test_files:
 
        metadata = build_metadata(file_name)
 
        print("-" * 50)
        print(metadata)