"""
Traffic context provider
Note: This uses mock data as real traffic APIs often require paid services
"""

from typing import Dict, Any, Optional
from datetime import datetime
from .base_provider import BaseProvider


class TrafficProvider(BaseProvider):
    """Provider for traffic data"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.cached_data: Optional[Dict[str, Any]] = None
    
    async def fetch_data(self, city: str, country: str = "GB") -> Dict[str, Any]:
        """
        Fetch traffic data for a city
        
        Args:
            city: City name
            country: Country code
            
        Returns:
            Formatted traffic data
        """
        # Check cache first
        if self.is_cache_valid() and self.cached_data:
            return self.format_response(self.cached_data)
        
        # Since real traffic APIs require paid services, we'll use mock data
        # In production, you would integrate with Google Maps API, TomTom, Here, etc.
        formatted_data = self._get_mock_traffic_data(city, country)
        
        self.cached_data = formatted_data
        self.last_fetch_time = datetime.now()
        
        return self.format_response(formatted_data)
    
    def _get_mock_traffic_data(self, city: str, country: str) -> Dict[str, Any]:
        """Generate mock traffic data"""
        import random
        
        # Simulate different traffic conditions
        conditions = ["low", "moderate", "heavy", "severe"]
        current_condition = random.choice(conditions)
        
        # Generate traffic data for major routes
        routes = [
            {"name": "City Center - Airport", "status": current_condition, "delay_minutes": random.randint(5, 30)},
            {"name": "City Center - North District", "status": random.choice(conditions), "delay_minutes": random.randint(0, 20)},
            {"name": "City Center - South District", "status": random.choice(conditions), "delay_minutes": random.randint(0, 25)},
            {"name": "City Center - East District", "status": random.choice(conditions), "delay_minutes": random.randint(0, 15)},
            {"name": "City Center - West District", "status": random.choice(conditions), "delay_minutes": random.randint(0, 20)},
        ]
        
        return {
            "city": city,
            "country": country,
            "overall_traffic_level": current_condition,
            "average_delay_minutes": sum(r["delay_minutes"] for r in routes) // len(routes),
            "routes": routes,
            "recommendation": self._get_traffic_recommendation(current_condition),
            "peak_hours": {
                "morning": "07:00 - 09:00",
                "evening": "17:00 - 19:00"
            },
            "note": "Mock traffic data - integrate with real API for production use"
        }
    
    def _get_traffic_recommendation(self, condition: str) -> str:
        """Get recommendation based on traffic condition"""
        recommendations = {
            "low": "Traffic is light. Good time to travel.",
            "moderate": "Moderate traffic expected. Allow some extra time.",
            "heavy": "Heavy traffic detected. Consider alternative routes or public transport.",
            "severe": "Severe traffic congestion. Strongly recommend public transport or delay travel."
        }
        return recommendations.get(condition, "Traffic conditions unknown.")

