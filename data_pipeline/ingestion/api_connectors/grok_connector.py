from groq import Groq
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import aiohttp
import json

logger = logging.getLogger(__name__)

class GrokConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.grok.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def analyze_market(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get market analysis from Grok AI.
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "disease": disease,
                "region": region,
                "analysis_type": "market",
                "include_competitors": True,
                "include_treatment_preferences": True
            }

            async with session.post(
                f"{self.base_url}/analyze",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Grok API error: {error_text}")

                result = await response.json()
                return self._process_analysis(result)

    async def get_treatment_insights(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get treatment insights from Grok AI.
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "disease": disease,
                "region": region,
                "analysis_type": "treatment",
                "include_effectiveness": True,
                "include_side_effects": True
            }

            async with session.post(
                f"{self.base_url}/analyze",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Grok API error: {error_text}")

                result = await response.json()
                return self._process_insights(result)

    async def get_competitor_analysis(
        self,
        disease: str,
        region: str
    ) -> Dict:
        """
        Get competitor analysis from Grok AI.
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "disease": disease,
                "region": region,
                "analysis_type": "competitors",
                "include_pipeline": True,
                "include_market_share": True
            }

            async with session.post(
                f"{self.base_url}/analyze",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Grok API error: {error_text}")

                result = await response.json()
                return self._process_competitor_analysis(result)

    def _process_analysis(self, result: Dict) -> Dict:
        """
        Process and structure the market analysis results.
        """
        return {
            "market_trends": result.get("market_trends", {}),
            "competitor_analysis": result.get("competitor_analysis", {}),
            "treatment_preference": result.get("treatment_preference", 0.5),
            "market_dynamics": result.get("market_dynamics", {}),
            "regulatory_impact": result.get("regulatory_impact", {})
        }

    def _process_insights(self, result: Dict) -> Dict:
        """
        Process and structure the treatment insights.
        """
        return {
            "effectiveness": result.get("effectiveness", {}),
            "side_effects": result.get("side_effects", {}),
            "patient_preferences": result.get("patient_preferences", {}),
            "cost_effectiveness": result.get("cost_effectiveness", {})
        }

    def _process_competitor_analysis(self, result: Dict) -> Dict:
        """
        Process and structure the competitor analysis.
        """
        return {
            "competitors": result.get("competitors", []),
            "pipeline_products": result.get("pipeline_products", []),
            "market_share": result.get("market_share", {}),
            "competitive_advantages": result.get("competitive_advantages", {})
        }

    async def analyze_text(self, 
                          text: str,
                          task: str = "analysis",
                          max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Analyze text using Grok LLM.
        
        Args:
            text: Text to analyze
            task: Type of analysis to perform
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            chat_completion = Groq(api_key=self.api_key).chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a pharmaceutical industry expert. Analyze the following text for {task}."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                model="mixtral-8x7b-32768",
                max_tokens=max_tokens
            )
            
            return {
                "analysis": chat_completion.choices[0].message.content,
                "model": "mixtral-8x7b-32768"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing text with Grok: {str(e)}")
            raise

    async def extract_key_points(self, 
                               text: str,
                               max_points: int = 5) -> List[str]:
        """
        Extract key points from text.
        
        Args:
            text: Text to analyze
            max_points: Maximum number of key points to extract
            
        Returns:
            List of key points
        """
        try:
            chat_completion = Groq(api_key=self.api_key).chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"Extract the top {max_points} key points from the following text. Format as a numbered list."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                model="mixtral-8x7b-32768"
            )
            
            # Parse the response into a list
            points = chat_completion.choices[0].message.content.split('\n')
            return [point.strip() for point in points if point.strip()]
            
        except Exception as e:
            logger.error(f"Error extracting key points with Grok: {str(e)}")
            raise

    async def generate_summary(self, 
                             text: str,
                             max_length: int = 200) -> str:
        """
        Generate a concise summary of text.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of the summary
            
        Returns:
            Generated summary
        """
        try:
            chat_completion = Groq(api_key=self.api_key).chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"Generate a concise summary of the following text in {max_length} words or less."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                model="mixtral-8x7b-32768"
            )
            
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating summary with Grok: {str(e)}")
            raise 