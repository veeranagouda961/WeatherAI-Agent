# 🌦️ WeatherAI-Agent

An intelligent, lightweight CLI-based weather assistant built in Python. Given an Indian city name, the agent automatically resolves geolocation coordinates, retrieves current weather data using the Open-Meteo API, logs operations, and provides outdoor activity recommendations.

---

## 🚀 Features

- **📍 Geolocation Lookup**: Automatically resolves latitude and longitude coordinates for Indian cities using Open-Meteo Geocoding API.
- **🏷️ City Alias Mapping**: Built-in support for alternate spellings and historical city names (e.g. Bangalore $\to$ Bengaluru, Mangalore $\to$ Mangaluru).
- **🌡️ Live Weather Fetching**: Retrieves real-time temperature and WMO weather condition codes via Open-Meteo Forecast API without requiring API keys.
- **🎯 Decision Engine**: Evaluates weather conditions to offer practical recommendations on outdoor vs. indoor activities.
- **🔄 Retry Mechanism**: Employs exponential backoff retry logic (up to 3 attempts) for network resilience.
- **📝 Comprehensive Logging**: Dual logging to console and persistent timestamped log files in `logs/agent.log`.

---

## 📂 Project Structure

```
WeatherAI-Agent/
├── .venv/                 # Python Virtual Environment
├── logs/
│   ├── .gitkeep           # Keeps directory in Git
│   └── agent.log          # Detailed runtime logs
├── src/
│   └── agent.py           # Core agent logic and CLI entry point
├── .gitignore             # Git ignored files & patterns
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```

---

## 🛠️ Prerequisites & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/veeranagouda961/WeatherAI-Agent.git
cd WeatherAI-Agent
```

### 2. Create and Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

Run the agent from the project root:

```bash
python src/agent.py
```

### Example Interactive Session

```
2026-08-15 16:54:02,249 - INFO - Weather agent started.
Enter city name: Bangalore
2026-08-15 16:54:10,449 - INFO - Looking up location for city: Bangalore
2026-08-15 16:54:11,605 - INFO - Location found: Bengaluru, Karnataka, India (12.9719, 77.5937)
2026-08-15 16:54:11,610 - INFO - Fetching weather data.
2026-08-15 16:54:12,950 - INFO - Weather data received successfully.
2026-08-15 16:54:12,955 - INFO - Weather decision: Good weather for outdoor activities.

========== WEATHER RESULT ==========
City: Bangalore
Temperature: 28.2°C
Weather Code: 3
Decision: Good weather for outdoor activities.
====================================
2026-08-15 16:54:12,958 - INFO - Weather agent completed successfully.
2026-08-15 16:54:12,959 - INFO - Weather agent stopped.
```

---

## 🌐 APIs Used

- **Geocoding API**: [Open-Meteo Geocoding Search](https://geocoding-api.open-meteo.com/v1/search)
- **Weather API**: [Open-Meteo Forecast](https://api.open-meteo.com/v1/forecast)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).