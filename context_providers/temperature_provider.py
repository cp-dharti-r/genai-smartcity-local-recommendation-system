"""
Temperature context provider
Note: Temperature is usually part of weather data, but this provider
can aggregate temperature data from multiple sources or historical data
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime
from .base_provider import BaseProvider
from .weather_provider import WeatherProvider


class TemperatureProvider(BaseProvider):
    """Provider for detailed temperature data"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key or os.getenv("OPENWEATHER_API_KEY"))
        self.weather_provider = WeatherProvider(self.api_key)
        self.cached_data: Optional[Dict[str, Any]] = None
    
    async def fetch_data(self, city: str, country: str = "GB") -> Dict[str, Any]:
        """
        Fetch temperature data for a city
        
        Args:
            city: City name
            country: Country code
            
        Returns:
            Formatted temperature data with additional context
        """
        # Check cache first
        if self.is_cache_valid() and self.cached_data:
            return self.format_response(self.cached_data)
        
        # Get weather data which includes temperature
        weather_data = await self.weather_provider.fetch_data(city, country)
        weather_info = weather_data.get("data", {})
        
        # Format temperature-specific data
        temp = weather_info.get("temperature", 0)
        feels_like = weather_info.get("feels_like", temp)
        
        formatted_data = {
            "city": weather_info.get("city", city),
            "country": weather_info.get("country", country),
            "current_temperature": temp,
            "feels_like_temperature": feels_like,
            "temperature_unit": "celsius",
            "temperature_range": {
                "comfortable": 18 <= temp <= 25,
                "too_cold": temp < 10,
                "too_hot": temp > 30
            },
            "recommendation": self._get_temperature_recommendation(temp),
            "humidity": weather_info.get("humidity"),
            "wind_chill_factor": self._calculate_wind_chill(
                temp, 
                weather_info.get("wind_speed", 0)
            )
        }
        
        self.cached_data = formatted_data
        self.last_fetch_time = datetime.now()
        
        return self.format_response(formatted_data)
    
    def _get_temperature_recommendation(self, temp: float) -> str:
        """Get recommendation based on temperature"""
        if temp < 0:
            return "Very cold! Dress warmly with multiple layers."
        elif temp < 10:
            return "Cold weather. Wear a warm jacket."
        elif temp < 18:
            return "Cool weather. A light jacket would be comfortable."
        elif temp < 25:
            return "Pleasant temperature. Light clothing is recommended."
        elif temp < 30:
            return "Warm weather. Light and breathable clothing."
        else:
            return "Hot weather! Stay hydrated and wear light, loose clothing."
    
    def _calculate_wind_chill(self, temp: float, wind_speed: float) -> float:
        """Calculate wind chill effect (simplified)"""
        if wind_speed < 5:
            return temp
        # Simple wind chill approximation
        wind_chill = temp - (wind_speed * 0.5)
        return round(wind_chill, 1)

