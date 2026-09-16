from rag.retrieval.retriever import Retriever
 
 
def run_end_to_end_test():
    print("=" * 70)
    print("WEEK 2 - FINAL END-TO-END RAG VALIDATION")
    print("=" * 70)
 
    # --------------------------------------------------
    # Incident details
    # --------------------------------------------------
 
    asset_id = "PUMP-101"
    machine_model = "PX-500"
    manual_version = "3.2"
    alarm = "High temperature"
 
    query = "What should I check for a high temperature alarm?"
 
    print("\nINCIDENT")
    print("-" * 70)
    print(f"Asset ID       : {asset_id}")
    print(f"Machine Model  : {machine_model}")
    print(f"Manual Version : {manual_version}")
    print(f"Alarm          : {alarm}")
    print(f"Query          : {query}")
 
    # --------------------------------------------------
    # Create retriever
    # --------------------------------------------------
 
    retriever = Retriever()
 
    # --------------------------------------------------
    # Retrieve relevant maintenance evidence
    # --------------------------------------------------
 
    results = retriever.search(
        query=query,
        top_k=3,
        machine_model=machine_model,
        manual_version=manual_version,
    )
 
    print("\nRETRIEVED EVIDENCE")
    print("=" * 70)
 
    if not results:
        print("ERROR: No relevant evidence found.")
        return False
 
    for i, result in enumerate(results, start=1):
 
        metadata = result["metadata"]
 
        print(f"\nRESULT {i}")
        print("-" * 70)
 
        print(f"Score   : {result['score']:.4f}")
        print(f"Source  : {metadata['file_name']}")
        print(f"Model   : {metadata['machine_model']}")
        print(f"Version : {metadata['manual_version']}")
        print(f"Section : {metadata['section']}")
 
        print("\nEvidence:")
        print(result["text"])
 
    # --------------------------------------------------
    # Validate retrieved evidence
    # --------------------------------------------------
 
    best_result = results[0]
    metadata = best_result["metadata"]
 
    print("\nVALIDATION")
    print("=" * 70)
 
    model_correct = (
        metadata["machine_model"] == machine_model
    )
 
    version_correct = (
        str(metadata["manual_version"]).rstrip(".")
        == str(manual_version).rstrip(".")
    )
 
    source_found = bool(metadata.get("file_name"))
 
    section_found = bool(metadata.get("section"))
 
    print(f"Model Match      : {'PASS' if model_correct else 'FAIL'}")
    print(f"Version Match    : {'PASS' if version_correct else 'FAIL'}")
    print(f"Source Available : {'PASS' if source_found else 'FAIL'}")
    print(f"Section Available: {'PASS' if section_found else 'FAIL'}")
 
    # --------------------------------------------------
    # Final result
    # --------------------------------------------------
 
    if (
        model_correct
        and version_correct
        and source_found
        and section_found
    ):
        print("\n" + "=" * 70)
        print("FINAL RESULT: PASS")
        print("=" * 70)
        print("Week 2 RAG end-to-end validation completed successfully.")
 
        return True
 
    print("\n" + "=" * 70)
    print("FINAL RESULT: FAIL")
    print("=" * 70)
 
    return False
 
 
if __name__ == "__main__":
    run_end_to_end_test()