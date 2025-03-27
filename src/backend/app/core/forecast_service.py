from typing import Dict, List, Optional
from datetime import datetime
import logging # Added for potential error logging

# Import schemas (Pydantic models) - Assuming these are defined correctly in schemas/forecast.py
from ..schemas.forecast import ForecastRequest, ForecastResponse

# Use absolute imports for modules outside the current 'app' package
from models.epidemiology.bayesian_model import BayesianEpidemiologicalModel
from data_pipeline.ingestion.api_connectors.fda_connector import FDAConnector
from data_pipeline.ingestion.api_connectors.cdc_connector import CDCConnector
from data_pipeline.ingestion.api_connectors.grok_connector import GrokConnector
from data_pipeline.ingestion.api_connectors.serper_connector import SerperConnector

# --- Import the settings object ---
from ..core.config import settings # Loads settings from config.py (which loads from Env Vars)

# Note: Ensure your PYTHONPATH includes the project root directory for these absolute imports to work.
# This is usually handled correctly by Uvicorn/Docker if run from the project root.

logger = logging.getLogger(__name__) # Added logger


class ForecastService:
    def __init__(self):
        """
        Initializes the service with necessary models and connectors,
        injecting API keys from loaded settings.
        """
        logger.info("Initializing ForecastService...")

        # --- Instantiate connectors with API keys from settings ---

        # Grok Connector
        if not settings.grok_api_key:
            logger.error("GROK_API_KEY environment variable not set or loaded!")
            raise ValueError("GROK_API_KEY environment variable not set or loaded!")
        self.grok_connector = GrokConnector(api_key=settings.grok_api_key)
        logger.debug("GrokConnector initialized.")

        # Serper Connector
        if not settings.serper_api_key:
            logger.error("SERPER_API_KEY environment variable not set or loaded!")
            raise ValueError("SERPER_API_KEY environment variable not set or loaded!")
        # Assuming SerperConnector __init__ takes api_key
        self.serper_connector = SerperConnector(api_key=settings.serper_api_key)
        logger.debug("SerperConnector initialized.")

        # FDA Connector - Adjust if its __init__ needs an API key or other config from settings
        # Example: self.fda_connector = FDAConnector(api_key=settings.fda_api_key)
        self.fda_connector = FDAConnector()
        logger.debug("FDAConnector initialized.")

        # CDC Connector - Adjust if its __init__ needs an API key or other config from settings
        self.cdc_connector = CDCConnector()
        logger.debug("CDCConnector initialized.")

        # Bayesian Model - Assuming it doesn't need external keys/config for init
        self.bayesian_model = BayesianEpidemiologicalModel()
        logger.debug("BayesianEpidemiologicalModel initialized.")

        logger.info("ForecastService initialized successfully.")


    async def get_market_data(self, disease: str) -> Dict:
        """Get market data using the Serper connector."""
        try:
            logger.debug(f"Fetching market data for {disease} via Serper...")
            # Assuming SerperConnector has an async method like get_market_research
            return await self.serper_connector.get_market_research(disease)
        except Exception as e:
            logger.error(f"Error fetching market data from Serper for {disease}: {e}", exc_info=True)
            # Decide how to handle errors - return empty dict, raise specific exception?
            return {"error": f"Failed to fetch market data: {e}"}

    async def get_competitor_info(self, disease: str) -> Dict:
        """Get competitor information using the Serper connector."""
        try:
            logger.debug(f"Fetching competitor info for {disease} via Serper...")
            # Assuming SerperConnector has an async method like get_competitor_info
            return await self.serper_connector.get_competitor_info(disease)
        except Exception as e:
            logger.error(f"Error fetching competitor info from Serper for {disease}: {e}", exc_info=True)
            return {"error": f"Failed to fetch competitor info: {e}"}

    async def get_regulatory_info(self, disease: str) -> Dict:
        """Get regulatory information using the FDA connector."""
        try:
            logger.debug(f"Fetching regulatory info for {disease} via FDA...")
            # Assuming FDAConnector has an async method like get_approval_data
            return await self.fda_connector.get_approval_data(disease)
        except Exception as e:
            logger.error(f"Error fetching regulatory info from FDA for {disease}: {e}", exc_info=True)
            return {"error": f"Failed to fetch regulatory info: {e}"}

    async def get_epi_data(self, disease: str) -> Dict:
        """Get epidemiological data using the CDC connector."""
        try:
            logger.debug(f"Fetching epi data for {disease} via CDC...")
            # Assuming CDCConnector has an async method like get_disease_data
            return await self.cdc_connector.get_disease_data(disease)
        except Exception as e:
            logger.error(f"Error fetching epi data from CDC for {disease}: {e}", exc_info=True)
            return {"error": f"Failed to fetch epi data: {e}"}

    async def get_ai_analysis(self, disease: str) -> Dict:
        """Get AI analysis using the Grok connector."""
        try:
            logger.debug(f"Fetching AI analysis for {disease} via Grok...")
            # Assuming GrokConnector has an async method like analyze_market
            # You might need to pass region here too based on GrokConnector method signature
            # return await self.grok_connector.analyze_market(disease=disease, region="US") # Example
            # Adjust call based on actual GrokConnector method signature
            # Placeholder call if analyze_market takes only disease:
            return await self.grok_connector.analyze_market(disease=disease, region="global") # Adjust region as needed
        except Exception as e:
            logger.error(f"Error fetching AI analysis from Grok for {disease}: {e}", exc_info=True)
            return {"error": f"Failed to fetch AI analysis: {e}"}


    async def generate_forecast(self, request: ForecastRequest) -> ForecastResponse:
        """
        Generates a multi-phase forecast using available data and a simplified model approach.
        Includes basic error checks for data fetching.
        """
        logger.info(f"Generating forecast for disease: {request.disease}, horizon: {request.forecast_horizon}")

        # 1. Gather data asynchronously (Consider asyncio.gather for concurrency)
        # Add basic checks if data fetching failed
        market_data = await self.get_market_data(request.disease)
        if "error" in market_data: logger.warning("Market data fetch failed.")
        competitor_info = await self.get_competitor_info(request.disease)
        if "error" in competitor_info: logger.warning("Competitor info fetch failed.")
        regulatory_info = await self.get_regulatory_info(request.disease)
        if "error" in regulatory_info: logger.warning("Regulatory info fetch failed.")
        epi_data = await self.get_epi_data(request.disease)
        if "error" in epi_data: logger.warning("Epi data fetch failed.")
        ai_analysis = await self.get_ai_analysis(request.disease)
        if "error" in ai_analysis: logger.warning("AI analysis fetch failed.")


        # 2. Run forecasts (Simplified & using placeholder results if data fetch failed)
        # Add try-except blocks around model execution
        try:
            market_size_result = self.bayesian_model.forecast_market_size(
                market_data=market_data if "error" not in market_data else {}, # Pass empty dict if failed
                epi_data=epi_data if "error" not in epi_data else {},
                fda_data=regulatory_info if "error" not in regulatory_info else {},
                forecast_horizon=request.forecast_horizon
            )
        except Exception as e:
            logger.error(f"Error running market size forecast: {e}", exc_info=True)
            market_size_result = {"market_size": None, "confidence_interval": None, "error": str(e)}

        try:
            patient_share_result = self.bayesian_model.forecast_patient_share(
                market_data=market_data if "error" not in market_data else {},
                ai_analysis=ai_analysis if "error" not in ai_analysis else {},
                forecast_horizon=request.forecast_horizon
            )
        except Exception as e:
            logger.error(f"Error running patient share forecast: {e}", exc_info=True)
            patient_share_result = {"patient_share": None, "confidence_interval": None, "error": str(e)}

        try:
            revenue_result = self.bayesian_model.forecast_revenue(
                market_size=market_size_result.get("market_size"), # Pass potential None
                patient_share=patient_share_result.get("patient_share"), # Pass potential None
                pricing_data=regulatory_info if "error" not in regulatory_info else {}, # Needs better pricing source
                forecast_horizon=request.forecast_horizon
            )
        except Exception as e:
            logger.error(f"Error running revenue forecast: {e}", exc_info=True)
            revenue_result = {"revenue": None, "confidence_interval": None, "error": str(e)}


        # 3. Construct the response object
        logger.info(f"Forecast generation complete for disease: {request.disease}")
        response_data = ForecastResponse(
            disease=request.disease,
            forecast_horizon=request.forecast_horizon,
            market_size=market_size_result.get("market_size"),
            market_size_ci=market_size_result.get("confidence_interval"),
            patient_share=patient_share_result.get("patient_share"),
            patient_share_ci=patient_share_result.get("confidence_interval"),
            revenue=revenue_result.get("revenue"),
            revenue_ci=revenue_result.get("confidence_interval"),
            generated_at=datetime.utcnow(),
            # Optionally include status/error messages from model runs
            model_status={
                 "market_size_error": market_size_result.get("error"),
                 "patient_share_error": patient_share_result.get("error"),
                 "revenue_error": revenue_result.get("error"),
            }
        )

        # Consider saving results to PostgreSQL here

        return response_data

# Optional: If using FastAPI's dependency injection, you wouldn't instantiate globally.
# forecast_service = ForecastService()
