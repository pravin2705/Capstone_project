from pathlib import Path
 
from app.week4.replay import (
    save_checkpoint,
    load_checkpoint,
    merge_evidence,
)
 
from app.agents.recommender import AgentRecommender
 
 
def test_checkpoint_save_and_load(tmp_path, monkeypatch):
    import app.week4.replay as replay_module
 
    # Use temporary checkpoint directory
    test_checkpoint_dir = tmp_path / "checkpoints"
 
    monkeypatch.setattr(
        replay_module,
        "CHECKPOINT_DIR",
        test_checkpoint_dir,
    )
 
    test_checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
 
    checkpoint = save_checkpoint(
        case_id="CASE-TEST-001",
        correlation_id="CORR-TEST123456",
        incident={
            "case_id": "CASE-TEST-001",
            "asset_id": "PUMP-101",
            "machine_model": "PUMP-X100",
            "manual_version": "V1.0",
            "alarm": "High temperature alarm",
        },
        evidence={
            "telemetry": {
                "temperature": 80
            },
            "maintenance_history": [],
            "inventory": [],
            "rag_evidence": [],
        },
        recommendation=(
            "Inspect the temperature sensor "
            "and cooling system."
        ),
        reasoning=None,
        status="READY_FOR_HITL",
    )
 
    assert checkpoint.case_id == "CASE-TEST-001"
 
    loaded_checkpoint = load_checkpoint(
        "CASE-TEST-001"
    )
 
    assert loaded_checkpoint.case_id == (
        "CASE-TEST-001"
    )
 
    assert loaded_checkpoint.correlation_id == (
        "CORR-TEST123456"
    )
 
    assert loaded_checkpoint.recommendation == (
        "Inspect the temperature sensor "
        "and cooling system."
    )
 
 
def test_merge_evidence():
    original_evidence = {
        "telemetry": {
            "temperature": 80,
            "vibration": 3,
        },
        "maintenance_history": [],
        "inventory": [],
    }
 
    new_evidence = {
        "telemetry": {
            "temperature": 95,
        }
    }
 
    merged = merge_evidence(
        original_evidence,
        new_evidence,
    )
 
    assert merged["telemetry"]["temperature"] == 95
 
    assert (
        merged["maintenance_history"]
        == []
    )
 
 
def test_recommendation_changes_after_late_telemetry():
    recommender = AgentRecommender()
 
    # ---------------------------------------------------------
    # Original evidence
    # ---------------------------------------------------------
    original_recommendation = (
        recommender.recommend(
            alarm="High temperature alarm",
            telemetry={
                "temperature": 80
            },
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
    )
 
    # ---------------------------------------------------------
    # Late telemetry
    # ---------------------------------------------------------
    replayed_recommendation = (
        recommender.recommend(
            alarm="High temperature alarm",
            telemetry={
                "temperature": 95
            },
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
    )
 
    # ---------------------------------------------------------
    # Verify recommendation changed
    # ---------------------------------------------------------
    assert original_recommendation != (
        replayed_recommendation
    )
 
    assert original_recommendation == (
        "Inspect the temperature sensor "
        "and cooling system."
    )
 
    assert replayed_recommendation == (
        "Inspect the cooling system, "
        "cooling fan and temperature sensor."
    )
 
 
def test_recommendation_does_not_change_for_same_evidence():
    recommender = AgentRecommender()
 
    first_recommendation = (
        recommender.recommend(
            alarm="High temperature alarm",
            telemetry={
                "temperature": 80
            },
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
    )
 
    replay_recommendation = (
        recommender.recommend(
            alarm="High temperature alarm",
            telemetry={
                "temperature": 80
            },
            maintenance_history=[],
            spare_inventory=[],
            rag_evidence=[],
        )
    )
 
    assert first_recommendation == (
        replay_recommendation
    )