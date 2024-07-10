import requests
from datetime import datetime
from statistics import median
from variable import dynamodb, DYNAMODB_TABLE_NAME
import logging
from decimal import Decimal

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_historical_weather(
    lat: float, lon: float, start_date: str, end_date: str
) -> dict:
    url = f"https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "UTC",
        "hourly": "temperature_2m,relative_humidity_2m",
    }

    logger.info(f"Requesting URL: {url} with params: {params}")
    response = requests.get(url, params=params)
    response.raise_for_status()  # This will raise an error for 4xx/5xx responses
    return response.json()


def aggregate_weather_data(data: dict) -> dict:
    hourly_data = data.get("hourly", {})
    temperatures = hourly_data.get("temperature_2m", [])
    humidities = hourly_data.get("relative_humidity_2m", [])
    times = hourly_data.get("time", [])

    daily_data = {}
    for time, temp, hum in zip(times, temperatures, humidities):
        date = datetime.strptime(time, "%Y-%m-%dT%H:%M").date()
        if date not in daily_data:
            daily_data[date] = {"temperatures": [], "humidities": []}
        daily_data[date]["temperatures"].append(temp)
        daily_data[date]["humidities"].append(hum)

    aggregated_data = {}
    for date, values in daily_data.items():
        aggregated_data[date] = {
            "temperature_median": Decimal(str(median(values["temperatures"]))),
            "humidity_median": Decimal(str(median(values["humidities"]))),
        }
    return aggregated_data


def save_to_dynamodb(property_id: int, daily_data: dict):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    with table.batch_writer() as batch:
        for date, values in daily_data.items():
            item = {
                "property_id": str(property_id),
                "date": date.isoformat(),
                "temperature_median": values["temperature_median"],
                "humidity_median": values["humidity_median"],
            }
            batch.put_item(Item=item)
