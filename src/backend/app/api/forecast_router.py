from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..core.forecast_service import ForecastService
from ..schemas.forecast import (
    ForecastRequest,
    ForecastResponse,
    ForecastResult,
    MarketSizeRequest,
    PatientShareRequest,
    RevenueRequest
)
from ..dependencies.database import get_db_session
from ..dependencies.auth import get_current_user
from ..models.forecast import (
    MarketSizeForecast,
    PatientShareForecast,
    RevenueForecast
)
from ..core.config import settings

router = APIRouter(prefix="/forecast", tags=["forecast"])

# Initialize forecast service
forecast_service = ForecastService()

@router.post("/market-size", response_model=MarketSizeForecast)
async def forecast_market_size(request: ForecastRequest):
    try:
        forecast = await forecast_service.generate_forecast(request)
        return MarketSizeForecast(
            disease=forecast.disease,
            region=request.region,
            forecast_horizon=forecast.forecast_horizon,
            market_size=forecast.market_size,
            confidence_interval=forecast.market_size_ci
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/patient-share", response_model=PatientShareForecast)
async def forecast_patient_share(request: ForecastRequest):
    try:
        forecast = await forecast_service.generate_forecast(request)
        return PatientShareForecast(
            disease=forecast.disease,
            region=request.region,
            forecast_horizon=forecast.forecast_horizon,
            patient_share=forecast.patient_share,
            confidence_interval=forecast.patient_share_ci
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/revenue", response_model=RevenueForecast)
async def forecast_revenue(request: ForecastRequest):
    try:
        forecast = await forecast_service.generate_forecast(request)
        return RevenueForecast(
            disease=forecast.disease,
            region=request.region,
            forecast_horizon=forecast.forecast_horizon,
            revenue=forecast.revenue,
            confidence_interval=forecast.revenue_ci
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{forecast_id}", response_model=ForecastResult)
async def get_forecast_results(
    forecast_id: str,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    # Implementation for getting forecast results
    pass

@router.get("/history", response_model=List[ForecastResult])
async def get_forecast_history(
    drug_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user)
):
    # Implementation for getting forecast history
    pass 