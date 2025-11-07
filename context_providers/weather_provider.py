"""
Weather context provider using OpenWeatherMap API
"""

import os
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
from .base_provider import BaseProvider


class WeatherProvider(BaseProvider):
    """Provider for weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("OPENWEATHER_API_KEY"))
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.cached_data: Optional[Dict[str, Any]] = None
    
    async def fetch_data(self, city: str, country: str = "GB") -> Dict[str, Any]:
        """
        Fetch weather data for a city
        
        Args:
            city: City name
            country: Country code
            
        Returns:
            Formatted weather data
        """
        # Check cache first
        if self.is_cache_valid() and self.cached_data:
            return self.format_response(self.cached_data)
        
        if not self.api_key:
            # Return mock data if API key is not available
            return self._get_mock_data(city, country)
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "q": f"{city},{country}",
                    "appid": self.api_key,
                    "units": "metric"
                }
                response = await client.get(self.base_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                
                # Format the data
                formatted_data = {
                    "city": data.get("name", city),
                    "country": data.get("sys", {}).get("country", country),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "description": data.get("weather", [{}])[0].get("description", ""),
                    "main_condition": data.get("weather", [{}])[0].get("main", ""),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "wind_direction": data.get("wind", {}).get("deg"),
                    "visibility": data.get("visibility"),
                    "cloudiness": data.get("clouds", {}).get("all"),
                }
                
                self.cached_data = formatted_data
                self.last_fetch_time = datetime.now()
                
                return self.format_response(formatted_data)
        except Exception as e:
            # Return mock data on error
            return self._get_mock_data(city, country)
    
    def _get_mock_data(self, city: str, country: str) -> Dict[str, Any]:
        """Return mock weather data when API is unavailable"""
        return self.format_response({
            "city": city,
            "country": country,
            "temperature": 15.5,
            "feels_like": 14.2,
            "humidity": 65,
            "pressure": 1013,
            "description": "partly cloudy",
            "main_condition": "Clouds",
            "wind_speed": 3.5,
            "wind_direction": 180,
            "visibility": 10000,
            "cloudiness": 40,
            "note": "Mock data - API key not configured"
        })

