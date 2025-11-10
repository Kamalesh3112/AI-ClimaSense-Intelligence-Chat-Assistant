# chains/weather_chain.py
import requests
from config.config import OPEN_METEO_BASE, DEFAULT_LAT, DEFAULT_LON

def get_weather_data(user_query: str) -> str:
    """
    Extracts current weather or forecast data based on default coordinates
    (or optionally extended later for geocoding).
    """
    try:
        # For now, static location (Chennai)
        lat, lon = DEFAULT_LAT, DEFAULT_LON
        url = f"{OPEN_METEO_BASE}?latitude={lat}&longitude={lon}&current=temperature_2m,precipitation,wind_speed_10m"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"Weather API returned status {response.status_code}"

        data = response.json()
        current = data.get("current", {})
        temperature = current.get("temperature_2m", "N/A")
        precipitation = current.get("precipitation", "N/A")
        wind_speed = current.get("wind_speed_10m", "N/A")

        return (
            f"Current weather conditions (Bengaluru):\n"
            f"• Temperature: {temperature} °C\n"
            f"• Precipitation: {precipitation} mm\n"
            f"• Wind Speed: {wind_speed} m/s\n"
        )

    except Exception as e:
        return f"[Weather API Error] {str(e)}"