import requests
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import aiohttp
import json

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

    async def get_approval_data(
        self,
        disease: str
    ) -> Dict:
        """
        Get FDA approval data for a specific disease.
        """
        async with aiohttp.ClientSession() as session:
            endpoint = f"{self.base_url}/drug/drugsfda/drug_drugsfda.json"
            params = {
                "search": f"brand_name:{disease}",
                "limit": 10
            }

            async with session.get(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"FDA API error: {error_text}")

                result = await response.json()
                return self._process_approval_data(result)

    async def get_pricing_data(
        self,
        disease: str
    ) -> Dict:
        """
        Get pricing data for drugs treating a specific disease.
        """
        async with aiohttp.ClientSession() as session:
            endpoint = f"{self.base_url}/drug/drugsfda/drug_drugsfda.json"
            params = {
                "search": f"brand_name:{disease}",
                "limit": 10
            }

            async with session.get(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"FDA API error: {error_text}")

                result = await response.json()
                return self._process_pricing_data(result)

    async def get_safety_data(
        self,
        disease: str
    ) -> Dict:
        """
        Get safety data for drugs treating a specific disease.
        """
        async with aiohttp.ClientSession() as session:
            endpoint = f"{self.base_url}/drug/event/drugevent.json"
            params = {
                "search": f"patient.reaction.reactionmeddrapt:{disease}",
                "limit": 10
            }

            async with session.get(
                endpoint,
                headers=self.headers,
                params=params
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"FDA API error: {error_text}")

                result = await response.json()
                return self._process_safety_data(result)

    def _process_approval_data(self, result: Dict) -> Dict:
        """
        Process and structure the FDA approval data.
        """
        results = result.get("results", [])
        
        approval_data = {
            "approval_status": self._extract_approval_status(results),
            "approval_date": self._extract_approval_date(results),
            "indications": self._extract_indications(results),
            "dosage_forms": self._extract_dosage_forms(results),
            "manufacturer": self._extract_manufacturer(results)
        }
        
        return approval_data

    def _process_pricing_data(self, result: Dict) -> Dict:
        """
        Process and structure the pricing data.
        """
        results = result.get("results", [])
        
        pricing_data = {
            "price_per_patient": self._extract_price_per_patient(results),
            "reimbursement_rate": self._extract_reimbursement_rate(results),
            "price_inflation": self._extract_price_inflation(results),
            "market_access": self._extract_market_access(results)
        }
        
        return pricing_data

    def _process_safety_data(self, result: Dict) -> Dict:
        """
        Process and structure the safety data.
        """
        results = result.get("results", [])
        
        safety_data = {
            "adverse_events": self._extract_adverse_events(results),
            "safety_warnings": self._extract_safety_warnings(results),
            "risk_factors": self._extract_risk_factors(results),
            "safety_profile": self._extract_safety_profile(results)
        }
        
        return safety_data

    def _extract_approval_status(self, results: list) -> str:
        """
        Extract approval status from FDA results.
        """
        # Implementation would parse results to find approval status
        return "pending"

    def _extract_approval_date(self, results: list) -> Optional[str]:
        """
        Extract approval date from FDA results.
        """
        # Implementation would parse results to find approval date
        return None

    def _extract_indications(self, results: list) -> list:
        """
        Extract indications from FDA results.
        """
        # Implementation would parse results to find indications
        return []

    def _extract_dosage_forms(self, results: list) -> list:
        """
        Extract dosage forms from FDA results.
        """
        # Implementation would parse results to find dosage forms
        return []

    def _extract_manufacturer(self, results: list) -> Optional[str]:
        """
        Extract manufacturer from FDA results.
        """
        # Implementation would parse results to find manufacturer
        return None

    def _extract_price_per_patient(self, results: list) -> Optional[float]:
        """
        Extract price per patient from FDA results.
        """
        # Implementation would parse results to find price per patient
        return None

    def _extract_reimbursement_rate(self, results: list) -> Optional[float]:
        """
        Extract reimbursement rate from FDA results.
        """
        # Implementation would parse results to find reimbursement rate
        return None

    def _extract_price_inflation(self, results: list) -> Optional[float]:
        """
        Extract price inflation from FDA results.
        """
        # Implementation would parse results to find price inflation
        return None

    def _extract_market_access(self, results: list) -> Dict:
        """
        Extract market access information from FDA results.
        """
        # Implementation would parse results to find market access
        return {}

    def _extract_adverse_events(self, results: list) -> list:
        """
        Extract adverse events from FDA results.
        """
        # Implementation would parse results to find adverse events
        return []

    def _extract_safety_warnings(self, results: list) -> list:
        """
        Extract safety warnings from FDA results.
        """
        # Implementation would parse results to find safety warnings
        return []

    def _extract_risk_factors(self, results: list) -> list:
        """
        Extract risk factors from FDA results.
        """
        # Implementation would parse results to find risk factors
        return []

    def _extract_safety_profile(self, results: list) -> Dict:
        """
        Extract safety profile from FDA results.
        """
        # Implementation would parse results to find safety profile
        return {} 