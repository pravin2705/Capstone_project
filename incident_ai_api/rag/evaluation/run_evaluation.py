import json
 
from rag.retrieval.retriever import Retriever
 
 
def load_questions():
 
    with open(
        "rag/evaluation/evaluation_questions.json",
        "r",
        encoding="utf-8",
    ) as file:
 
        return json.load(file)
 
 
def run_evaluation():
 
    questions = load_questions()
 
    retriever = Retriever()
 
    total = len(questions)
    correct = 0
 
    print("=" * 70)
    print("RAG BASELINE EVALUATION")
    print("=" * 70)
 
    for question in questions:
 
        results = retriever.search(
            query=question["question"],
            top_k=1,
            machine_model=question["machine_model"],
            manual_version=question["manual_version"],
        )
 
        expected = question["expected_section"]
 
        if results:
 
            retrieved_section = results[0]["metadata"]["section"]
 
            is_correct = (
                retrieved_section.lower()
                == expected.lower()
            )
 
        else:
 
            retrieved_section = "NO RESULT"
            is_correct = False
 
        if is_correct:
 
            correct += 1
            status = "CORRECT"
 
        else:
 
            status = "WRONG"
 
            print()
            print("!" * 70)
            print("POOR RETRIEVAL FOUND")
            print("!" * 70)
 
            print(f"Question ID : {question['id']}")
            print(f"Question    : {question['question']}")
            print(f"Model       : {question['machine_model']}")
            print(f"Version     : {question['manual_version']}")
            print(f"Expected    : {expected}")
            print(f"Retrieved   : {retrieved_section}")
 
            if results:
 
                print(f"Score       : {results[0]['score']:.4f}")
 
                print()
                print("Retrieved Text:")
                print("-" * 70)
                print(results[0]["text"])
 
            else:
 
                print("No evidence was retrieved.")
 
            print("!" * 70)
 
        print()
        print(f"Question {question['id']}")
        print(f"Expected : {expected}")
        print(f"Retrieved: {retrieved_section}")
        print(f"Result   : {status}")
 
    accuracy = (correct / total) * 100
 
    print()
    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
 
    print(f"Total questions : {total}")
    print(f"Correct         : {correct}")
    print(f"Incorrect       : {total - correct}")
    print(f"Accuracy        : {accuracy:.2f}%")
 
    print("=" * 70)
 
 
if __name__ == "__main__":
    run_evaluation()