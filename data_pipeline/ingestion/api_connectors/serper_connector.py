import requests
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SerperConnector:
    def __init__(self, api_key: str, base_url: str = "https://google.serper.dev/search"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        })

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
                
            response = self.session.post(self.base_url, json=data)
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