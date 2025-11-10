"""
Service layer for climate APIs. Uses utils/data_utils under the hood.
"""
from utils.data_utils import get_realtime_weather, get_realtime_weather_summary
from utils.logger import get_logger

logger = get_logger("climate_api_service")

def fetch_weather(lat: float, lon: float):
    try:
        return get_realtime_weather(lat, lon)
    except Exception as e:
        logger.error("Failed to fetch weather: %s", e)
        return None

def fetch_weather_summary(lat: float, lon: float):
    try:
        return get_realtime_weather_summary(lat, lon)
    except Exception as e:
        logger.error("Failed to build weather summary: %s", e)
        return "Weather summary unavailable."