import requests
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import aiohttp
import json

logger = logging.getLogger(__name__)

class SerperConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

    async def get_market_research(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get market research data from Serper.
        """
        query = f"market size {disease} {region} pharmaceutical"
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "q": query,
                "type": "news",
                "num": 10
            }

            async with session.post(
                self.base_url,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Serper API error: {error_text}")

                result = await response.json()
                return self._process_market_data(result)

    async def get_competitor_info(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get competitor information from Serper.
        """
        query = f"pharmaceutical companies {disease} {region} market share"
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "q": query,
                "type": "news",
                "num": 10
            }

            async with session.post(
                self.base_url,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Serper API error: {error_text}")

                result = await response.json()
                return self._process_competitor_data(result)

    async def get_regulatory_info(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get regulatory information from Serper.
        """
        query = f"FDA EMA approval {disease} {region} pharmaceutical"
        
        async with aiohttp.ClientSession() as session:
            payload = {
                "q": query,
                "type": "news",
                "num": 10
            }

            async with session.post(
                self.base_url,
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Serper API error: {error_text}")

                result = await response.json()
                return self._process_regulatory_data(result)

    def _process_market_data(self, result: Dict) -> Dict:
        """
        Process and structure the market research data.
        """
        news_items = result.get("news", [])
        
        # Extract market size and trends
        market_data = {
            "market_size": self._extract_market_size(news_items),
            "market_trend": self._extract_market_trend(news_items),
            "growth_rate": self._extract_growth_rate(news_items),
            "key_drivers": self._extract_key_drivers(news_items)
        }
        
        return market_data

    def _process_competitor_data(self, result: Dict) -> Dict:
        """
        Process and structure the competitor information.
        """
        news_items = result.get("news", [])
        
        # Extract competitor information
        competitor_data = {
            "market_share": self._extract_market_share(news_items),
            "key_players": self._extract_key_players(news_items),
            "pipeline_products": self._extract_pipeline_products(news_items),
            "competitive_landscape": self._extract_competitive_landscape(news_items)
        }
        
        return competitor_data

    def _process_regulatory_data(self, result: Dict) -> Dict:
        """
        Process and structure the regulatory information.
        """
        news_items = result.get("news", [])
        
        # Extract regulatory information
        regulatory_data = {
            "approval_status": self._extract_approval_status(news_items),
            "regulatory_timeline": self._extract_regulatory_timeline(news_items),
            "compliance_requirements": self._extract_compliance_requirements(news_items),
            "regulatory_risks": self._extract_regulatory_risks(news_items)
        }
        
        return regulatory_data

    def _extract_market_size(self, news_items: list) -> Optional[float]:
        """
        Extract market size from news items.
        """
        # Implementation would parse news items to find market size
        return None

    def _extract_market_trend(self, news_items: list) -> Optional[float]:
        """
        Extract market trend from news items.
        """
        # Implementation would parse news items to find market trend
        return None

    def _extract_growth_rate(self, news_items: list) -> Optional[float]:
        """
        Extract growth rate from news items.
        """
        # Implementation would parse news items to find growth rate
        return None

    def _extract_key_drivers(self, news_items: list) -> list:
        """
        Extract key market drivers from news items.
        """
        # Implementation would parse news items to find key drivers
        return []

    def _extract_market_share(self, news_items: list) -> Dict:
        """
        Extract market share information from news items.
        """
        # Implementation would parse news items to find market share
        return {}

    def _extract_key_players(self, news_items: list) -> list:
        """
        Extract key players from news items.
        """
        # Implementation would parse news items to find key players
        return []

    def _extract_pipeline_products(self, news_items: list) -> list:
        """
        Extract pipeline products from news items.
        """
        # Implementation would parse news items to find pipeline products
        return []

    def _extract_competitive_landscape(self, news_items: list) -> Dict:
        """
        Extract competitive landscape from news items.
        """
        # Implementation would parse news items to find competitive landscape
        return {}

    def _extract_approval_status(self, news_items: list) -> str:
        """
        Extract approval status from news items.
        """
        # Implementation would parse news items to find approval status
        return "pending"

    def _extract_regulatory_timeline(self, news_items: list) -> Dict:
        """
        Extract regulatory timeline from news items.
        """
        # Implementation would parse news items to find regulatory timeline
        return {}

    def _extract_compliance_requirements(self, news_items: list) -> list:
        """
        Extract compliance requirements from news items.
        """
        # Implementation would parse news items to find compliance requirements
        return []

    def _extract_regulatory_risks(self, news_items: list) -> list:
        """
        Extract regulatory risks from news items.
        """
        # Implementation would parse news items to find regulatory risks
        return []

    def search_google(self, 
                     query: str, 
                     num_results: int = 10,
                     country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform a Google search using Serper API.
        
        Args:
            query: Search query
            num_results: Number of results to return
            country_code: Optional country code for localized results
            
        Returns:
            Dictionary containing search results
        """
        try:
            data = {
                "q": query,
                "num": num_results
            }
            
            if country_code:
                data["gl"] = country_code
                
            response = requests.post(self.base_url, json=data)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error performing Serper search: {str(e)}")
            raise

    def search_news(self, 
                   query: str, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Search for news articles related to a query.
        
        Args:
            query: Search query
            start_date: Optional start date for news articles
            end_date: Optional end date for news articles
            
        Returns:
            List of news articles
        """
        try:
            # Add date range to query if provided
            if start_date and end_date:
                query += f" after:{start_date.strftime('%Y-%m-%d')} before:{end_date.strftime('%Y-%m-%d')}"
            
            results = self.search_google(query + " news", num_results=20)
            return results.get('news', [])
            
        except Exception as e:
            logger.error(f"Error searching news: {str(e)}")
            raise

    def search_scientific_papers(self, 
                               query: str,
                               num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for scientific papers related to a query.
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of scientific papers
        """
        try:
            # Add site: operator to focus on scientific sources
            query += " (site:pubmed.ncbi.nlm.nih.gov OR site:scholar.google.com OR site:researchgate.net)"
            results = self.search_google(query, num_results=num_results)
            return results.get('organic', [])
            
        except Exception as e:
            logger.error(f"Error searching scientific papers: {str(e)}")
            raise 