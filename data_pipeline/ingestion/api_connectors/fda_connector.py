import requests
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FDAConnector:
    def __init__(self, base_url: str = "https://api.fda.gov"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get_drug_labels(self, drug_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch drug label information from FDA API.
        
        Args:
            drug_name: Name of the drug to search for
            limit: Maximum number of results to return
            
        Returns:
            List of drug label information
        """
        try:
            url = f"{self.base_url}/drug/label.json"
            params = {
                'search': f'openfda.brand_name:"{drug_name}"',
                'limit': limit
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('results', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FDA drug labels: {str(e)}")
            raise

    def get_adverse_events(self, drug_name: str, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch adverse event reports for a specific drug.
        
        Args:
            drug_name: Name of the drug
            start_date: Start date for the search
            end_date: End date for the search
            
        Returns:
            List of adverse event reports
        """
        try:
            url = f"{self.base_url}/drug/event.json"
            params = {
                'search': f'patient.drug.medicinalproduct:"{drug_name}" AND receivedate:[{start_date.strftime("%Y%m%d")} TO {end_date.strftime("%Y%m%d")}]'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('results', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FDA adverse events: {str(e)}")
            raise

    def get_drug_approvals(self, drug_name: str) -> List[Dict[str, Any]]:
        """
        Fetch drug approval information.
        
        Args:
            drug_name: Name of the drug
            
        Returns:
            List of drug approval information
        """
        try:
            url = f"{self.base_url}/drug/drugsfda.json"
            params = {
                'search': f'brand_name:"{drug_name}"',
                'api_key': self.api_key
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json().get('results', [])
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FDA drug approvals: {str(e)}")
            raise 