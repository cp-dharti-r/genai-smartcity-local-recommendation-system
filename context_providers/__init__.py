"""
Context Providers for SmartCity Local Recommendation System
"""

from .weather_provider import WeatherProvider
from .traffic_provider import TrafficProvider
from .temperature_provider import TemperatureProvider
from .shop_offers_provider import ShopOffersProvider

__all__ = [
    'WeatherProvider',
    'TrafficProvider',
    'TemperatureProvider',
    'ShopOffersProvider',
]

