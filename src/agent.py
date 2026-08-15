import logging
import time
from pathlib import Path

import requests


# ============================================================
# LOGGING SETUP
# ============================================================

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "agent.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ============================================================
# API CONFIGURATION
# ============================================================

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

MAX_RETRIES = 3


# ============================================================
# CITY LOOKUP
# ============================================================

def get_coordinates(city):
    """Find latitude and longitude for an Indian city."""
    logger.info("Looking up location for city: %s", city)

    city_aliases = {
        "bangalore": "Bengaluru",
        "bengaluru": "Bengaluru",
        "mangalore": "Mangaluru",
        "mangaluru": "Mangaluru"
    }

    search_city = city_aliases.get(city.lower(), city)

    params = {
        "name": search_city,
        "count": 10,
        "language": "en",
        "format": "json",
        "countryCode": "IN"
    }

    response = requests.get(
        GEOCODING_API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"City not found in India: {city}")

    location = data["results"][0]

    if "latitude" not in location or "longitude" not in location:
        raise ValueError("Location coordinates are missing.")

    latitude = location["latitude"]
    longitude = location["longitude"]

    logger.info(
        "Location found: %s, %s, %s (%.4f, %.4f)",
        location.get("name", search_city),
        location.get("admin1", "Unknown"),
        location.get("country", "Unknown"),
        latitude,
        longitude
    )

    return latitude, longitude

# ============================================================
# WEATHER DATA
# ============================================================

def get_weather(latitude, longitude):
    """Fetch current weather data."""
    logger.info("Fetching weather data.")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,weather_code"
    }

    response = requests.get(
        WEATHER_API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "current" not in data:
        raise ValueError("Weather response does not contain current data.")

    current_data = data["current"]

    if "temperature_2m" not in current_data:
        raise ValueError("Temperature data is missing.")

    if "weather_code" not in current_data:
        raise ValueError("Weather code is missing.")

    temperature = current_data["temperature_2m"]
    weather_code = current_data["weather_code"]

    logger.info("Weather data received successfully.")

    return temperature, weather_code


# ============================================================
# WEATHER DECISION
# ============================================================

def make_weather_decision(temperature):
    """Make a simple decision based on temperature."""
    if temperature >= 20:
        decision = "Good weather for outdoor activities."
    else:
        decision = "It may be better to stay indoors."

    logger.info("Weather decision: %s", decision)

    return decision


# ============================================================
# MAIN AGENT
# ============================================================

def main():
    """Run the weather information agent."""
    logger.info("Weather agent started.")

    city = input("Enter city name: ").strip()

    if not city:
        logger.error("City name cannot be empty.")
        print("Error: City name cannot be empty.")
        logger.info("Weather agent stopped.")
        return

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            latitude, longitude = get_coordinates(city)

            temperature, weather_code = get_weather(
                latitude,
                longitude
            )

            decision = make_weather_decision(temperature)

            print("\n========== WEATHER RESULT ==========")
            print(f"City: {city}")
            print(f"Temperature: {temperature}°C")
            print(f"Weather Code: {weather_code}")
            print(f"Decision: {decision}")
            print("====================================")

            logger.info("Weather agent completed successfully.")
            break

        except (requests.RequestException, ValueError, KeyError) as error:
            logger.error(
                "Attempt %d failed: %s",
                attempt,
                error
            )

            if attempt < MAX_RETRIES:
                delay = 2 ** (attempt - 1)

                logger.info(
                    "Retrying in %d seconds...",
                    delay
                )

                time.sleep(delay)

            else:
                logger.error(
                    "Weather request failed after %d attempts.",
                    MAX_RETRIES
                )

                print(
                    "\nUnable to retrieve weather information. "
                    "Please try again later."
                )

    logger.info("Weather agent stopped.")


if __name__ == "__main__":
    main()