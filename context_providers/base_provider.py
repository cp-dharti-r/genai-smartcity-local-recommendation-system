"""
Base provider class for all context providers
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseProvider(ABC):
    """Base class for all context providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.last_fetch_time: Optional[datetime] = None
        self.cache_duration = 300  # 5 minutes cache
    
    @abstractmethod
    async def fetch_data(self, city: str, country: str = "GB") -> Dict[str, Any]:
        """
        Fetch data from the API
        
        Args:
            city: City name
            country: Country code (default: GB)
            
        Returns:
            Dictionary containing formatted data
        """
        pass
    
    def is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if self.last_fetch_time is None:
            return False
        
        time_diff = (datetime.now() - self.last_fetch_time).total_seconds()
        return time_diff < self.cache_duration
    
    def format_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the response with metadata
        
        Args:
            data: Raw data from API
            
        Returns:
            Formatted dictionary with metadata
        """
        return {
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "provider": self.__class__.__name__,
        }

