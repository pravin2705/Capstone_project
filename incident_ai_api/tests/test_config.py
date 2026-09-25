from app.config import settings
 
 
def test_default_configuration():
 
    assert settings.APP_NAME == (
        "Incident AI API"
    )
 
    assert settings.APP_VERSION == (
        "1.0.0"
    )
 
    assert settings.ENVIRONMENT == (
        "development"
    )
 
    assert settings.LLM_PROVIDER == (
        "mock"
    )
 
    assert settings.LOG_LEVEL == (
        "INFO"
    )
 
 
def test_secret_is_not_hardcoded():
 
    # Default configuration must not contain
    # a real API key.
 
    assert settings.LLM_API_KEY == ""