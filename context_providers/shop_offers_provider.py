"""
Shop offers context provider
Note: This uses mock data as real shop offer APIs are typically proprietary
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_provider import BaseProvider


class ShopOffersProvider(BaseProvider):
    """Provider for shop offers and deals"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.cached_data: Optional[Dict[str, Any]] = None
    
    async def fetch_data(self, city: str, country: str = "GB") -> Dict[str, Any]:
        """
        Fetch shop offers for a city
        
        Args:
            city: City name
            country: Country code
            
        Returns:
            Formatted shop offers data
        """
        # Check cache first
        if self.is_cache_valid() and self.cached_data:
            return self.format_response(self.cached_data)
        
        # Generate mock shop offers
        formatted_data = self._get_mock_shop_offers(city, country)
        
        self.cached_data = formatted_data
        self.last_fetch_time = datetime.now()
        
        return self.format_response(formatted_data)
    
    def _get_mock_shop_offers(self, city: str, country: str) -> Dict[str, Any]:
        """Generate mock shop offers data"""
        import random
        
        categories = ["Groceries", "Electronics", "Fashion", "Restaurants", "Entertainment"]
        
        offers = []
        for category in categories:
            discount = random.randint(10, 50)
            offers.append({
                "category": category,
                "store": f"{category} Store {random.randint(1, 5)}",
                "offer": f"{discount}% OFF",
                "description": f"Special {discount}% discount on selected items",
                "valid_until": (datetime.now().replace(day=datetime.now().day + random.randint(1, 7))).strftime("%Y-%m-%d"),
                "location": f"{city} City Center",
                "distance_km": round(random.uniform(0.5, 5.0), 1)
            })
        
        # Add some featured offers
        featured_offers = [
            {
                "category": "Restaurants",
                "store": "City Bistro",
                "offer": "Buy 1 Get 1 Free",
                "description": "Lunch special - Buy one main course, get one free",
                "valid_until": (datetime.now().replace(day=datetime.now().day + 3)).strftime("%Y-%m-%d"),
                "location": f"{city} Downtown",
                "distance_km": 1.2
            },
            {
                "category": "Groceries",
                "store": "SuperMart",
                "offer": "20% OFF",
                "description": "Weekly grocery special - 20% off on all fresh produce",
                "valid_until": (datetime.now().replace(day=datetime.now().day + 2)).strftime("%Y-%m-%d"),
                "location": f"{city} Shopping District",
                "distance_km": 2.5
            }
        ]
        
        return {
            "city": city,
            "country": country,
            "total_offers": len(offers) + len(featured_offers),
            "featured_offers": featured_offers,
            "category_offers": offers,
            "all_offers": featured_offers + offers,
            "best_deals": sorted(
                featured_offers + offers,
                key=lambda x: float(x["offer"].replace("% OFF", "").replace("Buy 1 Get 1 Free", "50")),
                reverse=True
            )[:3],
            "note": "Mock shop offers data - integrate with real APIs for production use"
        }

