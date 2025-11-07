"""
MCP Server implementation
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from contextlib import asynccontextmanager

from context_providers import (
    WeatherProvider,
    TrafficProvider,
    TemperatureProvider,
    ShopOffersProvider
)


class SmartCityMCPServer:
    """
    MCP Server that retrieves data from context providers,
    stores them temporarily, and answers user queries
    """
    
    def __init__(self):
        self.weather_provider = WeatherProvider()
        self.traffic_provider = TrafficProvider()
        self.temperature_provider = TemperatureProvider()
        self.shop_offers_provider = ShopOffersProvider()
        
        # Temporary storage for data
        self.data_cache: Dict[str, Any] = {}
        self.cache_timestamp: Optional[datetime] = None
        self.cache_duration = 300  # 5 minutes
        
        # Current city context
        self.current_city = "London"
        self.current_country = "GB"
    
    async def fetch_all_data(self, city: str = None, country: str = None) -> Dict[str, Any]:
        """
        Fetch all data from context providers
        
        Args:
            city: City name (default: current city)
            country: Country code (default: current country)
            
        Returns:
            Dictionary containing all city data
        """
        city = city or self.current_city
        country = country or self.current_country
        
        # Update current context
        self.current_city = city
        self.current_country = country
        
        # Fetch all data in parallel
        weather_task = self.weather_provider.fetch_data(city, country)
        traffic_task = self.traffic_provider.fetch_data(city, country)
        temperature_task = self.temperature_provider.fetch_data(city, country)
        shop_offers_task = self.shop_offers_provider.fetch_data(city, country)
        
        weather_data, traffic_data, temperature_data, shop_offers_data = await asyncio.gather(
            weather_task, traffic_task, temperature_task, shop_offers_task
        )
        
        # Store in cache
        self.data_cache = {
            "weather": weather_data.get("data", {}),
            "traffic": traffic_data.get("data", {}),
            "temperature": temperature_data.get("data", {}),
            "shop_offers": shop_offers_data.get("data", {}),
            "metadata": {
                "city": city,
                "country": country,
                "fetched_at": datetime.now().isoformat()
            }
        }
        self.cache_timestamp = datetime.now()
        
        return self.data_cache
    
    def is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if self.cache_timestamp is None:
            return False
        
        time_diff = (datetime.now() - self.cache_timestamp).total_seconds()
        return time_diff < self.cache_duration and len(self.data_cache) > 0
    
    async def get_city_data(self, city: str = None, country: str = None, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get city data, using cache if available and valid
        
        Args:
            city: City name
            country: Country code
            force_refresh: Force refresh even if cache is valid
            
        Returns:
            Dictionary containing all city data
        """
        city = city or self.current_city
        country = country or self.current_country
        
        # Check if we need to fetch new data
        if force_refresh or not self.is_cache_valid() or \
           self.data_cache.get("metadata", {}).get("city") != city:
            await self.fetch_all_data(city, country)
        
        return self.data_cache
    
    async def answer_query(self, query: str, city: str = None, country: str = None) -> Dict[str, Any]:
        """
        Answer a user query about city conditions
        
        Args:
            query: User's question
            city: City name (optional)
            country: Country code (optional)
            
        Returns:
            Dictionary with answer and relevant data
        """
        # Get city data
        city_data = await self.get_city_data(city, country)
        
        query_lower = query.lower()
        
        # Determine which data is relevant
        relevant_data = {}
        answer_parts = []
        
        # Weather-related queries
        weather_keywords = ["weather", "rain", "sunny", "cloudy", "wind", "humidity", "pressure"]
        if any(keyword in query_lower for keyword in weather_keywords):
            weather = city_data.get("weather", {})
            relevant_data["weather"] = weather
            answer_parts.append(
                f"Weather in {weather.get('city', city)}: {weather.get('description', 'N/A')}, "
                f"Temperature: {weather.get('temperature', 'N/A')}°C, "
                f"Humidity: {weather.get('humidity', 'N/A')}%"
            )
        
        # Temperature-related queries
        temp_keywords = ["temperature", "temp", "hot", "cold", "warm", "cool"]
        if any(keyword in query_lower for keyword in temp_keywords):
            temp = city_data.get("temperature", {})
            relevant_data["temperature"] = temp
            answer_parts.append(
                f"Current temperature: {temp.get('current_temperature', 'N/A')}°C. "
                f"{temp.get('recommendation', '')}"
            )
        
        # Traffic-related queries
        traffic_keywords = ["traffic", "road", "route", "congestion", "delay", "commute"]
        if any(keyword in query_lower for keyword in traffic_keywords):
            traffic = city_data.get("traffic", {})
            relevant_data["traffic"] = traffic
            answer_parts.append(
                f"Traffic level: {traffic.get('overall_traffic_level', 'N/A')}. "
                f"{traffic.get('recommendation', '')}"
            )
        
        # Shop offers queries
        shop_keywords = ["shop", "store", "offer", "deal", "discount", "sale", "buy", "shopping"]
        if any(keyword in query_lower for keyword in shop_keywords):
            offers = city_data.get("shop_offers", {})
            relevant_data["shop_offers"] = offers
            best_deals = offers.get("best_deals", [])
            if best_deals:
                deal_strings = [f"{deal['store']} - {deal['offer']}" for deal in best_deals[:3]]
                answer_parts.append(f"Best deals available: {', '.join(deal_strings)}")
            else:
                answer_parts.append(f"Found {offers.get('total_offers', 0)} offers available in the city.")
        
        # General queries - return summary
        if not answer_parts:
            weather = city_data.get("weather", {})
            traffic = city_data.get("traffic", {})
            temp = city_data.get("temperature", {})
            offers = city_data.get("shop_offers", {})
            
            answer_parts.append(
                f"City conditions for {city_data.get('metadata', {}).get('city', city)}: "
                f"Weather: {weather.get('description', 'N/A')}, "
                f"Temperature: {temp.get('current_temperature', 'N/A')}°C, "
                f"Traffic: {traffic.get('overall_traffic_level', 'N/A')}, "
                f"Available offers: {offers.get('total_offers', 0)}"
            )
            relevant_data = city_data
        
        # Construct response
        answer = " ".join(answer_parts) if answer_parts else "I couldn't find specific information for your query."
        
        return {
            "query": query,
            "answer": answer,
            "relevant_data": relevant_data,
            "timestamp": datetime.now().isoformat(),
            "city": city_data.get("metadata", {}).get("city", city),
            "country": city_data.get("metadata", {}).get("country", country)
        }
    
    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get a summary of available context data
        
        Returns:
            Dictionary with summary of cached data
        """
        if not self.data_cache:
            return {
                "status": "no_data",
                "message": "No city data has been fetched yet."
            }
        
        metadata = self.data_cache.get("metadata", {})
        return {
            "status": "data_available",
            "city": metadata.get("city"),
            "country": metadata.get("country"),
            "fetched_at": metadata.get("fetched_at"),
            "cache_valid": self.is_cache_valid(),
            "available_data": {
                "weather": "weather" in self.data_cache,
                "traffic": "traffic" in self.data_cache,
                "temperature": "temperature" in self.data_cache,
                "shop_offers": "shop_offers" in self.data_cache
            }
        }

