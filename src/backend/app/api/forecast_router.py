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
from ..models.forecast import (
    MarketSizeForecast,
    PatientShareForecast,
    RevenueForecast,
    ForecastRequest
)
from ..core.config import settings
from data_pipeline.ingestion.api_connectors.grok_connector import GrokConnector
from data_pipeline.ingestion.api_connectors.serper_connector import SerperConnector
from data_pipeline.ingestion.api_connectors.fda_connector import FDAConnector
from data_pipeline.ingestion.api_connectors.cdc_connector import CDCConnector
from models.epidemiology.bayesian_model import BayesianEpidemiologicalModel

router = APIRouter(prefix="/forecast", tags=["forecast"])

# Initialize connectors
grok_connector = GrokConnector(api_key=settings.grok_api_key)
serper_connector = SerperConnector(api_key=settings.serper_api_key)
fda_connector = FDAConnector()
cdc_connector = CDCConnector()

# Initialize models
bayesian_model = BayesianEpidemiologicalModel()

@router.post("/market-size", response_model=MarketSizeForecast)
async def forecast_market_size(request: ForecastRequest):
    try:
        # Get market research data from Serper
        market_data = await serper_connector.get_market_research(
            disease=request.disease,
            region=request.region
        )
        
        # Get epidemiological data from CDC
        epi_data = await cdc_connector.get_disease_data(
            disease=request.disease,
            region=request.region
        )
        
        # Get FDA approval data
        fda_data = await fda_connector.get_approval_data(
            disease=request.disease
        )
        
        # Generate forecast using Bayesian model
        forecast = bayesian_model.forecast_market_size(
            market_data=market_data,
            epi_data=epi_data,
            fda_data=fda_data,
            forecast_horizon=request.forecast_horizon
        )
        
        return MarketSizeForecast(
            disease=request.disease,
            region=request.region,
            forecast_horizon=request.forecast_horizon,
            market_size=forecast["market_size"],
            confidence_interval=forecast["confidence_interval"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/patient-share", response_model=PatientShareForecast)
async def forecast_patient_share(request: ForecastRequest):
    try:
        # Get market research data
        market_data = await serper_connector.get_market_research(
            disease=request.disease,
            region=request.region
        )
        
        # Get AI analysis from Grok
        ai_analysis = await grok_connector.analyze_market(
            disease=request.disease,
            region=request.region
        )
        
        # Generate forecast
        forecast = bayesian_model.forecast_patient_share(
            market_data=market_data,
            ai_analysis=ai_analysis,
            forecast_horizon=request.forecast_horizon
        )
        
        return PatientShareForecast(
            disease=request.disease,
            region=request.region,
            forecast_horizon=request.forecast_horizon,
            patient_share=forecast["patient_share"],
            confidence_interval=forecast["confidence_interval"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/revenue", response_model=RevenueForecast)
async def forecast_revenue(request: ForecastRequest):
    try:
        # Get market size forecast
        market_size = await forecast_market_size(request)
        
        # Get patient share forecast
        patient_share = await forecast_patient_share(request)
        
        # Get pricing data from FDA
        pricing_data = await fda_connector.get_pricing_data(
            disease=request.disease
        )
        
        # Generate revenue forecast
        forecast = bayesian_model.forecast_revenue(
            market_size=market_size.market_size,
            patient_share=patient_share.patient_share,
            pricing_data=pricing_data,
            forecast_horizon=request.forecast_horizon
        )
        
        return RevenueForecast(
            disease=request.disease,
            region=request.region,
            forecast_horizon=request.forecast_horizon,
            revenue=forecast["revenue"],
            confidence_interval=forecast["confidence_interval"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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