"""Main CLI entry point for the Weather App AI Agent."""
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from weather_client import get_current_weather
from ai_agent import generate_weather_explanation


def print_weather_info(weather_data: dict, ai_explanation: str):
    """Print formatted weather information and AI explanation."""
    print("\n" + "=" * 60)
    print(f"Weather for: {weather_data.get('location', weather_data.get('city', 'Unknown'))}")
    print("=" * 60)
    
    # Location Details Section
    print("\n📍 Location Details:")
    print("-" * 60)
    print(f"City:            {weather_data.get('city', 'N/A')}")
    
    state = weather_data.get('state', '') or 'N/A'
    print(f"State/Province:  {state}")
    
    print(f"Country:         {weather_data.get('country', 'N/A')}")
    if weather_data.get('country_code'):
        print(f"Country Code:    {weather_data.get('country_code', 'N/A')}")
    
    # Weather Information Section
    print("\n🌤️  Weather Information:")
    print("-" * 60)
    print(f"Temperature:     {weather_data['temp']}°C")
    print(f"Feels like:      {weather_data['feels_like']}°C")
    print(f"Condition:       {weather_data['condition'].title()}")
    print(f"Humidity:        {weather_data['humidity']}%")
    
    print("\n" + "-" * 60)
    print("🤖 AI Explanation:")
    print("-" * 60)
    print(ai_explanation)
    print("=" * 60 + "\n")


def main():
    """Main CLI loop."""
    print("🌤️  Weather App AI Agent")
    print("=" * 60)
    
    while True:
        try:
            # Get city name from user
            city = input("\nEnter city name (or 'quit' to exit): ").strip()
            
            if city.lower() in ['quit', 'exit', 'q']:
                print("Goodbye! 👋")
                break
            
            if not city:
                print("Please enter a valid city name.")
                continue
            
            # Fetch weather data
            print(f"\nFetching weather for {city}...")
            weather_data = get_current_weather(city)
            
            # Generate AI explanation
            print("Generating AI explanation...")
            ai_explanation = generate_weather_explanation(weather_data)
            
            # Display results
            print_weather_info(weather_data, ai_explanation)
            
            # Ask if user wants to check another city
            while True:
                continue_choice = input("Check another city? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("Goodbye! 👋")
                    sys.exit(0)
                else:
                    print("Please enter 'y' or 'n'.")
            
        except ValueError as e:
            print(f"\n❌ Error: {e}\n")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}\n")
            print("Please try again or check your configuration.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)

