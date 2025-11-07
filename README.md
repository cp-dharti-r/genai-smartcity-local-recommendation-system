# SmartCity Local Recommendation System

A Python application that uses the Model Context Protocol (MCP) to provide citizens with real-time information about their city, including weather, traffic, temperature, and shop offers.

## 🎯 Project Goals

- **Learn Model Context Protocol (MCP)**: Implement MCP server and client architecture
- **Context Provider**: Gather city data from public APIs and format it for MCP servers
- **MCP Server**: Retrieve data from context providers, store temporarily, and answer user queries
- **MCP Client**: Provide a user-friendly UI interface for querying city conditions

## 📁 Project Structure

```
genai-smartcity-local-recommendation-system/
├── context_providers/          # Data providers for city information
│   ├── __init__.py
│   ├── base_provider.py        # Base class for all providers
│   ├── weather_provider.py     # Weather data from OpenWeatherMap
│   ├── temperature_provider.py # Temperature data and recommendations
│   ├── traffic_provider.py     # Traffic conditions
│   └── shop_offers_provider.py # Shop offers and deals
├── mcp_server/                 # MCP Server implementation
│   ├── __init__.py
│   └── server.py              # Main server logic
├── mcp_client/                 # MCP Client UI
│   ├── __init__.py
│   └── app.py                 # Streamlit web interface
├── run_server.py              # Standalone server runner
├── run_client.py              # Streamlit client runner
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd genai-smartcity-local-recommendation-system
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

   **Note**: The application works with mock data if API keys are not provided. For production use:
   - Get OpenWeatherMap API key from: https://openweathermap.org/api
   - Get Google Maps API key from: https://developers.google.com/maps/documentation (for traffic data)

## 🏃 Running the Application

### Option 1: Run the Web UI (Recommended)

The Streamlit web interface provides the best user experience:

```bash
python run_client.py
```

Or directly with Streamlit:

```bash
streamlit run mcp_client/app.py
or
streamlit run mcp_client/app.py --server.port=8501 --server.address=localhost --server.headless=true
```

The UI will open in your browser at `http://localhost:8501`

### Option 2: Run the Standalone Server

For a command-line interface:

```bash
python run_server.py
```

This will start an interactive session where you can ask questions about city conditions.

## 💡 Usage Examples

### Web UI Usage

1. **Start the client**: Run `python run_client.py`
2. **Configure city**: Use the sidebar to set your city and country code
3. **Ask questions**: Type questions like:
   - "What's the weather like?"
   - "How's the traffic?"
   - "What shop offers are available?"
   - "What's the temperature?"
4. **Quick actions**: Use the quick action buttons for common queries

### Example Queries

- Weather: "What's the weather like today?"
- Temperature: "Is it hot or cold outside?"
- Traffic: "How's the traffic to the airport?"
- Shop Offers: "What deals are available near me?"
- General: "Tell me about city conditions"

## 🏗️ Architecture

### Context Providers

Context providers fetch data from external APIs and format it for use by the MCP server:

- **WeatherProvider**: Fetches weather data from OpenWeatherMap API
- **TemperatureProvider**: Provides temperature data with recommendations
- **TrafficProvider**: Provides traffic conditions (uses mock data; can be integrated with real APIs)
- **ShopOffersProvider**: Provides shop offers and deals (uses mock data)

All providers:
- Support caching to reduce API calls
- Return formatted, consistent data structures
- Include fallback mock data when APIs are unavailable

### MCP Server

The `SmartCityMCPServer`:
- Retrieves data from all context providers
- Stores data temporarily in cache (5-minute TTL)
- Answers user queries by analyzing the question and retrieving relevant data
- Supports multiple cities and countries

### MCP Client

The Streamlit-based client provides:
- Interactive chat interface
- City configuration
- Real-time data refresh
- Context summary display
- Quick action buttons

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENWEATHER_API_KEY=your_api_key_here
GOOGLE_MAPS_API_KEY=your_api_key_here
DEFAULT_CITY=London
DEFAULT_COUNTRY=GB
```

### API Keys

- **OpenWeatherMap**: Free tier available at https://openweathermap.org/api
- **Google Maps**: Requires billing account for traffic data

## 📊 Data Flow

1. **User Query** → MCP Client (Streamlit UI)
2. **Query Processing** → MCP Server
3. **Data Retrieval** → Context Providers (Weather, Traffic, Temperature, Shop Offers)
4. **API Calls** → Public APIs (OpenWeatherMap, etc.)
5. **Data Formatting** → Context Providers format data
6. **Caching** → MCP Server stores data temporarily
7. **Query Answering** → MCP Server analyzes query and returns relevant data
8. **Response Display** → MCP Client shows answer to user

## 🧪 Testing

The application includes mock data fallbacks, so you can test without API keys:

1. Run without `.env` file - will use mock data
2. Test with different cities
3. Try various query types

## 🔮 Future Enhancements

- Integration with real traffic APIs (Google Maps, TomTom, Here)
- Integration with real shop offer APIs
- Historical data analysis
- Multi-language support
- Mobile app version
- Real-time notifications
- Advanced recommendation algorithms

## 📝 Notes

- **Mock Data**: The application uses mock data for traffic and shop offers as these typically require paid API services. Weather and temperature use OpenWeatherMap (free tier available).
- **Caching**: Data is cached for 5 minutes to reduce API calls and improve performance.
- **Error Handling**: The application gracefully handles API failures and falls back to mock data.

## 🤝 Contributing

Feel free to extend this project by:
- Adding more context providers
- Integrating additional APIs
- Improving the UI/UX
- Adding more sophisticated query understanding
- Implementing persistent storage

## 📄 License

This project is for educational purposes to learn Model Context Protocol (MCP).

---

**Built with ❤️ for learning MCP and smart city applications**
