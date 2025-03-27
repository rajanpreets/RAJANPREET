import requests
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CDCConnector:
    def __init__(self, base_url: str = "https://api.cdc.gov"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get_disease_data(self, 
                        disease: str,
                        start_date: datetime,
                        end_date: datetime,
                        region: str = "US") -> List[Dict[str, Any]]:
        """
        Fetch disease data from CDC API.
        
        Args:
            disease: Name of the disease
            start_date: Start date for the search
            end_date: End date for the search
            region: Region to get data for
            
        Returns:
            List of disease data points
        """
        try:
            # Example endpoint for disease data
            url = f"{self.base_url}/disease/{disease.lower()}/data.json"
            params = {
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d"),
                'region': region
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('data', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching CDC disease data: {str(e)}")
            raise

    def get_vaccination_data(self, 
                           vaccine: str,
                           start_date: datetime,
                           end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch vaccination data from CDC API.
        
        Args:
            vaccine: Name of the vaccine
            start_date: Start date for the search
            end_date: End date for the search
            
        Returns:
            List of vaccination data points
        """
        try:
            url = f"{self.base_url}/vaccination/{vaccine.lower()}/data.json"
            params = {
                'start_date': start_date.strftime("%Y-%m-%d"),
                'end_date': end_date.strftime("%Y-%m-%d")
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('data', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching CDC vaccination data: {str(e)}")
            raise 