from app.agents.recommender import AgentRecommender
 
 
def test_high_temperature_recommendation():
 
    recommender = AgentRecommender()
 
    result = recommender.recommend(
        alarm="High Temperature Alarm",
        telemetry={
            "temperature": 95.0,
            "vibration": 2.1,
            "pressure": 4.5,
        },
        maintenance_history=[
            {
                "issue": "High Temperature Alarm",
                "action": "Cooling fan inspected",
            }
        ],
        spare_inventory=[
            {
                "part_name": "Cooling Fan",
                "quantity": 3,
                "status": "AVAILABLE",
            }
        ],
        rag_evidence=[
            {
                "text": "Inspect cooling system.",
            }
        ],
    )
 
    assert "cooling" in result.lower()
 
 
def test_vibration_recommendation():
 
    recommender = AgentRecommender()
 
    result = recommender.recommend(
        alarm="Vibration Alarm",
        telemetry={
            "temperature": 75.0,
            "vibration": 5.0,
            "pressure": 4.5,
        },
        maintenance_history=[],
        spare_inventory=[],
        rag_evidence=[],
    )
 
    assert "vibration" in result.lower()
 
 
def test_pressure_recommendation():
 
    recommender = AgentRecommender()
 
    result = recommender.recommend(
        alarm="High Pressure Alarm",
        telemetry={
            "temperature": 75.0,
            "vibration": 2.0,
            "pressure": 8.0,
        },
        maintenance_history=[],
        spare_inventory=[],
        rag_evidence=[],
    )
 
    assert "pressure" in result.lower()