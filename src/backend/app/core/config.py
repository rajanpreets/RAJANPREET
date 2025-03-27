from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    grok_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    
    # Database
    database_url: Optional[str] = None
    
    # API Settings
    api_prefix: str = "/api/v1"
    project_name: str = "Pharma Forecasting API"
    
    # External API URLs
    grok_api_url: str = "https://api.grok.ai/v1"
    serper_api_url: str = "https://google.serper.dev/search"
    fda_api_url: str = "https://api.fda.gov"
    cdc_api_url: str = "https://api.cdc.gov"

    # Rate Limiting
    requests_per_minute: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings() 
