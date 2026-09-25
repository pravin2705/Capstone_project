from app.week4.evaluation import Week4Evaluator
 
 
def test_week4_evaluation():
 
    evaluator = Week4Evaluator()
 
    result = evaluator.run_evaluation()
 
    assert result["total_tests"] == 5
 
    assert result["passed"] == 5
 
    assert result["failed"] == 0
 
    assert result["score_percent"] == 100