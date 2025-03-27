from groq import Groq
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GrokConnector:
    def __init__(self, api_key: str, base_url: str = "https://api.grok.ai/v1"):
        self.client = Groq(api_key=api_key)
        self.base_url = base_url

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
            chat_completion = self.client.chat.completions.create(
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
            chat_completion = self.client.chat.completions.create(
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
            chat_completion = self.client.chat.completions.create(
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