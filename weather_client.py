"""Weather API client using Open-Meteo (free, no API key required)."""
import requests
from typing import Dict, Any


def get_current_weather(city: str) -> Dict[str, Any]:
    """
    Fetch current weather data for a given city using Open-Meteo API.

    Args:
        city: Name of the city

    Returns:
        Dictionary containing:
            - city: City name
            - state: State/Province/Administrative area
            - country: Country name
            - country_code: Country code (ISO)
            - location: Full location string (city, state, country)
            - temp: Temperature in Celsius
            - feels_like: Feels-like temperature in Celsius
            - condition: Weather condition description
            - humidity: Humidity percentage
            - latitude: Latitude coordinate
            - longitude: Longitude coordinate

    Raises:
        requests.RequestException: If the API request fails
        ValueError: If the city is not found or API returns an error
    """
    try:
        # First, get coordinates for the city using geocoding
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geocode_url, params=geocode_params, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            raise ValueError(
                f"Could not find weather for that city: {city}. Please check the spelling."
            )

        result = geo_data["results"][0]
        latitude = result["latitude"]
        longitude = result["longitude"]
        city_name = result.get("name", city)
        state = result.get("admin1", "")
        country = result.get("country", "")
        country_code = result.get("country_code", "")

        # Get weather data
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "auto"
        }

        weather_response = requests.get(
            weather_url, params=weather_params, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data.get("current", {})
        temp = current.get("temperature_2m", 0)
        humidity = current.get("relative_humidity_2m", 0)
        weather_code = current.get("weather_code", 0)

        condition = _get_weather_condition(weather_code)

        # Build location string for display
        location_parts = [city_name]
        if state:
            location_parts.append(state)
        if country:
            location_parts.append(country)
        location_display = ", ".join(location_parts)

        return {
            "city": city_name,
            "state": state,
            "country": country,
            "country_code": country_code,
            "location": location_display,
            "temp": round(temp, 1),
            "feels_like": round(temp, 1),  # Open-Meteo doesn't provide feels_like
            "condition": condition,
            "humidity": round(humidity, 0),
            "latitude": latitude,
            "longitude": longitude
        }

    except requests.exceptions.Timeout:
        raise requests.RequestException(
            "Weather API request timed out. Please try again."
        )
    except requests.exceptions.ConnectionError:
        raise requests.RequestException(
            "Could not connect to weather API. Check your internet connection."
        )
    except requests.exceptions.HTTPError as e:
        raise requests.RequestException(
            f"Weather API returned an error: {e.response.status_code}"
        )
    except ValueError:
        raise  # Re-raise ValueError as-is
    except Exception as e:
        raise requests.RequestException(
            f"Could not fetch weather data: {str(e)}"
        )


# WMO Weather interpretation codes mapping
_WEATHER_DESCRIPTIONS = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail"
}


def _get_weather_condition(weather_code: int) -> str:
    """Map weather code to human-readable description."""
    return _WEATHER_DESCRIPTIONS.get(weather_code, "unknown")
