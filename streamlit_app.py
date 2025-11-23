"""Streamlit UI for Weather App AI Agent."""
import streamlit as st
from weather_client import get_current_weather
from ai_agent import generate_weather_explanation

# Page configuration
st.set_page_config(
    page_title="Weather App AI Agent",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact layout
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 500px;
    }
    .main-header {
        text-align: center;
        padding: 0.5rem 0;
        margin-top: 0;
        font-size: 1.5rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {
        padding-top: 0;
    }
    .ai-explanation {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .location-detail {
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        font-size: 0.85rem;
    }
    .stButton>button {
        background-color: #0066cc !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 0.9rem !important;
        width: auto !important;
        min-width: 150px !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #0052a3 !important;
    }
    h3 {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h2>🌤️ Weather App AI Agent</h2></div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for configuration info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app uses:
    - **Open-Meteo API** for real weather data (free, no API key required)
    - **Local LLM** (Ollama) for AI-powered explanations
    
    Enter a city name to get started!
    """)
    
    st.markdown("---")
    st.markdown("**Made with ❤️ using Streamlit**")

# Main content
city = st.text_input(
    "Enter city name:",
    placeholder="e.g., New York, London, Tokyo",
    key="city_input"
)

if st.button("Get Weather", type="primary"):
    if not city:
        st.warning("⚠️ Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city}..."):
            try:
                # Get weather data using Open-Meteo (free, no API key required)
                weather_data = get_current_weather(city)
                
                # Display detailed location information
                st.markdown("### 📍 Location Details")
                location_col1, location_col2, location_col3 = st.columns(3)
                
                with location_col1:
                    st.markdown(
                        f'<div class="location-detail">'
                        f'<strong>City:</strong><br>{weather_data.get("city", "N/A")}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                with location_col2:
                    state_display = weather_data.get('state', '') or 'N/A'
                    st.markdown(
                        f'<div class="location-detail">'
                        f'<strong>State/Province:</strong><br>{state_display}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                with location_col3:
                    country = weather_data.get('country', 'N/A')
                    country_code = weather_data.get('country_code', '')
                    country_display = f"{country}"
                    if country_code:
                        country_display += f" ({country_code})"
                    st.markdown(
                        f'<div class="location-detail">'
                        f'<strong>Country:</strong><br>{country_display}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                st.markdown("---")
                
                # Display weather information
                st.markdown("### 🌤️ Weather Information")
                
                # Create columns for metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        label="🌡️ Temperature",
                        value=f"{weather_data['temp']}°C",
                        delta=f"Feels like {weather_data['feels_like']}°C"
                    )
                
                with col2:
                    st.metric(
                        label="💧 Humidity",
                        value=f"{weather_data['humidity']}%"
                    )
                
                # Weather condition
                st.markdown(f"**Condition:** {weather_data['condition'].title()}")
                
                st.markdown("---")
                
                # Generate and display AI explanation
                with st.spinner("🤖 Generating AI explanation..."):
                    try:
                        ai_explanation = generate_weather_explanation(weather_data)
                        
                        st.markdown("### 🤖 AI Explanation")
                        st.markdown(f'<div class="ai-explanation">{ai_explanation}</div>', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error generating AI explanation: {str(e)}")
                        st.info("💡 Make sure your local LLM server (Ollama) is running.")
                
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.info("💡 Please check your configuration and try again.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Enter a city name above to get started! 🚀"
    "</div>",
    unsafe_allow_html=True
)

