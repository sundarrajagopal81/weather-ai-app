# Weather App AI Agent

A modern weather application that fetches real-time weather data and uses a local open-source LLM to generate friendly, AI-powered weather explanations. Available as both a CLI tool and a beautiful web interface.

## Features

- 🌤️ **Real-time Weather Data**: Fetch current weather information using Open-Meteo API (free, no API key required)
- 🤖 **AI-Powered Explanations**: Generate natural language weather explanations using local LLM (Ollama)
- 🖥️ **Dual Interface**: Clean CLI interface and modern Streamlit web UI
- 📍 **Detailed Location Info**: Shows city, state/province, country, and coordinates
- 🌡️ **Comprehensive Weather Data**: Temperature, feels-like temperature, humidity, and weather conditions
- ⚙️ **Configurable**: Easy configuration via environment variables
- 🎨 **Modern UI**: Beautiful, responsive web interface with custom styling

## Tech Stack

### Backend
- **Python 3.7+**: Core programming language
- **Requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **Streamlit**: Modern web framework for building the UI
- **Custom CSS**: Styled components for enhanced user experience

### APIs & Services
- **Open-Meteo API**: Free weather data API (no API key required)
  - Geocoding API for location resolution
  - Weather Forecast API for current conditions
- **Ollama**: Local LLM server for AI explanations
  - Compatible with various models (llama3, phi3, mistral, etc.)

### Architecture
- **Modular Design**: Separated concerns (weather client, LLM client, AI agent)
- **Error Handling**: Comprehensive error handling and user-friendly messages
- **Type Hints**: Python type annotations for better code quality

## Prerequisites

- Python 3.7 or higher
- A local LLM server running (e.g., Ollama)
- Internet connection for weather API calls

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd weather-ai-app
```

### 2. Create a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
# .env file
LLM_BASE_URL=http://localhost:11434
LLM_MODEL_NAME=llama3
```

**Configuration Options:**
- `LLM_BASE_URL`: Base URL for your local LLM server (default: `http://localhost:11434`)
- `LLM_MODEL_NAME`: Model name to use (e.g., `llama3`, `phi3`, `mistral`)

**Note**: No weather API key is required! The app uses Open-Meteo API which is completely free and doesn't require authentication.

### 5. Start your local LLM server

**If using Ollama:**
```bash
# Start Ollama server (if not already running)
ollama serve

# Pull a model (if not already downloaded)
ollama pull llama3
```

**For other LLM servers:**
Make sure your server is running and accessible at the `LLM_BASE_URL` specified in `.env`. The app expects an Ollama-compatible API endpoint.

## Usage

### Web UI (Recommended)

Run the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`.

**Features:**
- 🌐 Modern, responsive web interface
- 📊 Visual weather metrics with cards
- 📍 Detailed location information
- 🤖 AI-powered weather explanations
- 🎨 Beautiful custom styling

### CLI Mode

Run the command-line interface:
```bash
python main.py
```

Enter a city name when prompted, and the app will:
1. Fetch current weather data
2. Generate an AI-powered explanation
3. Display both the raw data and the explanation

Type `quit`, `exit`, or `q` to close the application.

## Project Structure

```
weather-ai-app/
├── main.py              # CLI entry point
├── streamlit_app.py     # Streamlit web UI
├── weather_client.py    # Open-Meteo API client
├── llm_client.py        # Local LLM client (Ollama-compatible)
├── ai_agent.py          # AI agent for weather explanations
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── PROJECT_DOCUMENTATION.md  # Detailed project documentation
└── ARCHITECTURE_DIAGRAM.md   # Architecture overview
```

## How It Works

1. **Location Resolution**: User enters a city name → Geocoding API resolves to coordinates
2. **Weather Fetching**: Coordinates → Weather API returns current conditions
3. **AI Explanation**: Weather data → Local LLM generates friendly explanation
4. **Display**: All information displayed in a user-friendly format

## Data Displayed

### Location Details
- City name
- State/Province (if available)
- Country name and code
- Coordinates (latitude, longitude)

### Weather Information
- Current temperature (°C)
- Feels-like temperature (°C)
- Weather condition description
- Humidity percentage

### AI Explanation
- Natural language weather summary
- Contextual advice based on conditions
- Location-aware explanations

## Error Handling

The app handles common errors gracefully:
- ✅ Invalid city names with helpful suggestions
- ✅ Weather API failures with retry information
- ✅ LLM server connection issues with troubleshooting tips
- ✅ Missing configuration with setup guidance
- ✅ Network timeouts with user-friendly messages

## Troubleshooting

### "LLM server not reachable"
- Make sure Ollama (or your LLM server) is running
- Check that `LLM_BASE_URL` in `.env` matches your server address
- Verify the server is accessible: `curl http://localhost:11434/api/tags` (for Ollama)
- Ensure the model specified in `LLM_MODEL_NAME` is available

### "Could not find weather for that city"
- Check the city name spelling
- Try using "City, Country" format (e.g., "London, UK")
- Verify your internet connection
- The geocoding API may not recognize very small or obscure locations

### "LLM_MODEL_NAME not found"
- Make sure you've created a `.env` file
- Verify `LLM_MODEL_NAME` is set in your `.env` file
- Default model is `llama3` if not specified

### Streamlit not starting
- Ensure Streamlit is installed: `pip install streamlit`
- Check if port 8501 is already in use
- Try running with a different port: `streamlit run streamlit_app.py --server.port 8502`

## Development

### Running in Development Mode

For Streamlit with auto-reload:
```bash
streamlit run streamlit_app.py --server.runOnSave true
```

### Code Structure

- **Modular Architecture**: Each component has a single responsibility
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive exception handling
- **Documentation**: Docstrings for all functions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for free weather data
- [Ollama](https://ollama.ai/) for local LLM capabilities
- [Streamlit](https://streamlit.io/) for the web framework
