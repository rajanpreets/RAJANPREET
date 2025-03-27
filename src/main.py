from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime

app = FastAPI(
    title="Pharma Forecasting API",
    description="API for pharmaceutical demand forecasting",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForecastRequest(BaseModel):
    product_id: str
    historical_data: List[dict]
    forecast_periods: int

class ForecastResponse(BaseModel):
    product_id: str
    forecast: List[dict]
    confidence_intervals: List[dict]

@app.get("/")
async def root():
    return {"message": "Welcome to Pharma Forecasting API"}

@app.post("/forecast", response_model=ForecastResponse)
async def create_forecast(request: ForecastRequest):
    try:
        # Convert historical data to DataFrame
        df = pd.DataFrame(request.historical_data)
        
        # Basic forecasting logic (placeholder)
        # In a real implementation, you would use more sophisticated models
        last_value = df['value'].iloc[-1]
        forecast_values = [last_value * (1 + np.random.normal(0, 0.1)) 
                         for _ in range(request.forecast_periods)]
        
        # Generate dates for forecast
        last_date = pd.to_datetime(df['date'].iloc[-1])
        forecast_dates = pd.date_range(start=last_date, 
                                     periods=request.forecast_periods + 1, 
                                     freq='M')[1:]
        
        # Create forecast response
        forecast = [
            {"date": date.strftime("%Y-%m-%d"), "value": value}
            for date, value in zip(forecast_dates, forecast_values)
        ]
        
        # Calculate confidence intervals (placeholder)
        confidence_intervals = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "lower_bound": value * 0.9,
                "upper_bound": value * 1.1
            }
            for date, value in zip(forecast_dates, forecast_values)
        ]
        
        return ForecastResponse(
            product_id=request.product_id,
            forecast=forecast,
            confidence_intervals=confidence_intervals
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 