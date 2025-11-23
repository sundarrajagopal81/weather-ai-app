"""AI agent that generates natural language weather explanations."""
from typing import Dict, Any
from llm_client import generate_chat_response


def generate_weather_explanation(weather_data: Dict[str, Any]) -> str:
    """
    Generate a friendly weather explanation using the local LLM.

    Args:
        weather_data: Dictionary containing weather information
                     (city, temp, feels_like, condition, humidity)

    Returns:
        Natural language weather explanation
    """
    system_prompt = (
        "You are a friendly weather assistant. Given the raw weather data, "
        "explain the current weather in 3-5 sentences, in simple language. "
        "Include one short advice line (e.g., 'carry an umbrella', 'stay hydrated', etc.)."
    )

    # Build location string for the prompt
    city = weather_data.get('city', 'the city')
    state = weather_data.get('state', '')
    country = weather_data.get('country', '')

    location_parts = [part for part in [city, state, country] if part]
    location_str = ", ".join(location_parts) if location_parts else city

    user_prompt = (
        f"Here is the current weather data for {location_str}:\n"
        f"- Location: {location_str}\n"
        f"  - City: {city}\n"
    )

    if state:
        user_prompt += f"  - State/Province: {state}\n"
    if country:
        user_prompt += f"  - Country: {country}\n"

    user_prompt += (
        f"- Temperature: {weather_data.get('temp')}°C\n"
        f"- Feels like: {weather_data.get('feels_like')}°C\n"
        f"- Condition: {weather_data.get('condition')}\n"
        f"- Humidity: {weather_data.get('humidity')}%\n\n"
        f"Please provide a friendly weather explanation based on this data. "
        f"Make sure to mention the location (city, state if available, and country) in your explanation."
    )

    try:
        explanation = generate_chat_response(system_prompt, user_prompt)
        return explanation
    except Exception as e:
        # If LLM fails, return a fallback message
        return (
            f"Current weather in {weather_data.get('city')}: "
            f"{weather_data.get('temp')}°C (feels like {weather_data.get('feels_like')}°C), "
            f"{weather_data.get('condition')}, with {weather_data.get('humidity')}% humidity. "
            f"[LLM explanation unavailable: {str(e)}]"
        )
