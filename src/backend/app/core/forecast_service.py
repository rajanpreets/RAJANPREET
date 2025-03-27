from typing import Dict, List, Optional
from datetime import datetime
from ..models.forecast import ForecastRequest, ForecastResponse
from ...models.epidemiology.bayesian_model import BayesianEpidemiologicalModel
from ...data_pipeline.ingestion.api_connectors.fda_connector import FDAConnector
from ...data_pipeline.ingestion.api_connectors.cdc_connector import CDCConnector
from ...data_pipeline.ingestion.api_connectors.grok_connector import GrokConnector
from ...data_pipeline.ingestion.api_connectors.serper_connector import SerperConnector

class ForecastService:
    def __init__(self):
        self.bayesian_model = BayesianEpidemiologicalModel()
        self.fda_connector = FDAConnector()
        self.cdc_connector = CDCConnector()
        self.grok_connector = GrokConnector()
        self.serper_connector = SerperConnector()

    async def get_market_data(self, disease: str) -> Dict:
        """Get market data from Serper API."""
        return await self.serper_connector.get_market_research(disease)

    async def get_competitor_info(self, disease: str) -> Dict:
        """Get competitor information from Serper API."""
        return await self.serper_connector.get_competitor_info(disease)

    async def get_regulatory_info(self, disease: str) -> Dict:
        """Get regulatory information from FDA API."""
        return await self.fda_connector.get_approval_data(disease)

    async def get_epi_data(self, disease: str) -> Dict:
        """Get epidemiological data from CDC API."""
        return await self.cdc_connector.get_disease_data(disease)

    async def get_ai_analysis(self, disease: str) -> Dict:
        """Get AI analysis from Grok API."""
        return await self.grok_connector.analyze_market(disease)

    async def generate_forecast(self, request: ForecastRequest) -> ForecastResponse:
        """Generate forecast using all available data sources."""
        # Gather data from all sources
        market_data = await self.get_market_data(request.disease)
        competitor_info = await self.get_competitor_info(request.disease)
        regulatory_info = await self.get_regulatory_info(request.disease)
        epi_data = await self.get_epi_data(request.disease)
        ai_analysis = await self.get_ai_analysis(request.disease)

        # Generate forecasts using Bayesian model
        market_size_forecast = self.bayesian_model.forecast_market_size(
            market_data=market_data,
            epi_data=epi_data,
            fda_data=regulatory_info,
            forecast_horizon=request.forecast_horizon
        )

        patient_share_forecast = self.bayesian_model.forecast_patient_share(
            market_data=market_data,
            ai_analysis=ai_analysis,
            forecast_horizon=request.forecast_horizon
        )

        revenue_forecast = self.bayesian_model.forecast_revenue(
            market_size=market_size_forecast["market_size"],
            patient_share=patient_share_forecast["patient_share"],
            pricing_data=regulatory_info,
            forecast_horizon=request.forecast_horizon
        )

        return ForecastResponse(
            disease=request.disease,
            forecast_horizon=request.forecast_horizon,
            market_size=market_size_forecast["market_size"],
            market_size_ci=market_size_forecast["confidence_interval"],
            patient_share=patient_share_forecast["patient_share"],
            patient_share_ci=patient_share_forecast["confidence_interval"],
            revenue=revenue_forecast["revenue"],
            revenue_ci=revenue_forecast["confidence_interval"],
            generated_at=datetime.utcnow(),
            data_sources={
                "market_data": market_data,
                "competitor_info": competitor_info,
                "regulatory_info": regulatory_info,
                "epi_data": epi_data,
                "ai_analysis": ai_analysis
            }
        ) 