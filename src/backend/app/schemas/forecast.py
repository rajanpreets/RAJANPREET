from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ForecastRequest(BaseModel):
    disease: str
    region: str
    forecast_horizon: int

class ForecastResponse(BaseModel):
    disease: str
    forecast_horizon: int
    market_size: float
    market_size_ci: List[float]
    patient_share: float
    patient_share_ci: List[float]
    revenue: float
    revenue_ci: List[float]
    generated_at: datetime
    data_sources: dict

class MarketSizeRequest(BaseModel):
    disease: str
    region: str
    forecast_horizon: int

class PatientShareRequest(BaseModel):
    disease: str
    region: str
    forecast_horizon: int

class RevenueRequest(BaseModel):
    disease: str
    region: str
    forecast_horizon: int

class ForecastResult(BaseModel):
    id: str
    disease: str
    forecast_type: str
    status: str
    created_at: datetime
    updated_at: datetime
    parameters: dict
    results: Optional[dict]
    error_message: Optional[str] 