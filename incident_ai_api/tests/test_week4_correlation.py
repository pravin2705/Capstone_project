from app.week4.correlation import generate_correlation_id
 
 
def test_generate_correlation_id():
    correlation_id = generate_correlation_id()
 
    assert correlation_id.startswith("CORR-")
    assert len(correlation_id) == 17