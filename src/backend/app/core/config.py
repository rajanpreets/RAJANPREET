from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "Pharma Forecasting API"
    api_description: str = "API for pharmaceutical demand forecasting"
    api_version: str = "1.0.0"
    api_docs_url: str = "/docs"
    api_redoc_url: str = "/redoc"

    # Database Configuration
    database_url: str

    # External API Keys
    grok_api_key: str
    serper_api_key: str

    # External API URLs
    grok_api_url: str = "https://api.grok.ai/v1"
    serper_api_url: str = "https://google.serper.dev/search"
    fda_api_url: str = "https://api.fda.gov"
    cdc_api_url: str = "https://api.cdc.gov"

    # Rate Limiting
    requests_per_minute: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 