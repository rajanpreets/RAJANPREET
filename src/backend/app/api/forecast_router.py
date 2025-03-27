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
from ..dependencies.database import get_db
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/forecast", tags=["forecast"])

@router.post("/market-size", response_model=ForecastResponse)
async def forecast_market_size(
    request: MarketSizeRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Generate market size forecast for a specific disease/condition.
    """
    try:
        service = ForecastService(db)
        result = await service.generate_market_size_forecast(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/patient-share", response_model=ForecastResponse)
async def forecast_patient_share(
    request: PatientShareRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Generate patient share forecast for a specific drug.
    """
    try:
        service = ForecastService(db)
        result = await service.generate_patient_share_forecast(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/revenue", response_model=ForecastResponse)
async def forecast_revenue(
    request: RevenueRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Generate revenue forecast for a specific drug.
    """
    try:
        service = ForecastService(db)
        result = await service.generate_revenue_forecast(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/results/{forecast_id}", response_model=ForecastResult)
async def get_forecast_results(
    forecast_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve results of a specific forecast run.
    """
    try:
        service = ForecastService(db)
        result = await service.get_forecast_results(forecast_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/history", response_model=List[ForecastResult])
async def get_forecast_history(
    drug_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Retrieve historical forecast results with optional filtering.
    """
    try:
        service = ForecastService(db)
        results = await service.get_forecast_history(
            drug_id=drug_id,
            start_date=start_date,
            end_date=end_date
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 