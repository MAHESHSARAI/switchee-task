import json
import logging
from typing import Any, Dict
from dataclasses import dataclass
from helper_functions import (
    get_historical_weather,
    aggregate_weather_data,
    save_to_dynamodb,
)
from variable import sqs_client, SQS_QUEUE_URL
import requests  # Ensure requests is imported

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class WeatherRequest:
    property_id: int
    lat: float
    lon: float
    start_date: str
    end_date: str


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    for record in event["Records"]:
        try:
            message = json.loads(record["body"])
            request = WeatherRequest(**message)

            logger.info(f"Processing {request}")

            weather_data = get_historical_weather(
                request.lat, request.lon, request.start_date, request.end_date
            )
            daily_data = aggregate_weather_data(weather_data)
            save_to_dynamodb(request.property_id, daily_data)
            logger.info(f"Data saved for property_id: {request.property_id}")

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {record['body']}. Error: {str(e)}")
        except KeyError as e:
            logger.error(
                f"Missing key in the message: {record['body']}. Error: {str(e)}"
            )
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
        except Exception as e:
            logger.error(f"Error processing record: {record}. Error: {str(e)}")

    return {"statusCode": 200, "body": json.dumps("Processing completed successfully")}
