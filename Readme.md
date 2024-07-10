# Historical Weather Data Retrieval with AWS Lambda

## Project Overview

This project implements an AWS Lambda function to retrieve historical temperature and humidity data for specific geographic coordinates associated with a property ID. The data is sourced from the Open Meteo API. Upon receiving requests from an SQS queue, the Lambda function processes the data and stores the aggregated results in a DynamoDB table.

## Major Files

- **main.py**: Entry point for the Lambda function.
- **helper_functions.py**: Contains helper functions for data retrieval, aggregation, and storage.
- **variable.py**: Manages AWS resource configurations and initializes AWS clients.
- **main.tf**: Terraform configuration file to deploy the SQS queue, DynamoDB table, and Lambda function.
- **iam.tf**: Terraform configuration file to set up the necessary IAM roles and policies.

## AWS Lambda Function

### Overview

The Lambda function is responsible for:
- Consuming messages from an SQS queue.
- Downloading historical weather data from the Open Meteo API.
- Aggregating the temperature and humidity data on a daily basis (using median values).
- Storing the aggregated data in a DynamoDB table.

### Helper Functions

- **get_historical_weather**: Fetches historical weather data from the Open Meteo API.
- **aggregate_weather_data**: Aggregates the temperature and humidity data to their median values on a daily basis.
- **save_to_dynamodb**: Saves the aggregated data into a DynamoDB table.

## Terraform Configuration

### main.tf

This file contains the main resources required for the project, including:
- SQS Queue
- DynamoDB Table
- Lambda Function
- Lambda Event Source Mapping

### iam.tf

This file sets up the IAM roles and policies necessary for the Lambda function to interact with SQS and DynamoDB.

## Deployment Instructions

1. **Initialize Terraform**:
   ```sh
   terraform init
   ```

2. **Review the Plan**:
   ```sh
   terraform plan
   ```

3. **Apply the Changes**:
   ```sh
   terraform apply
   ```

## Testing the Setup

### Send a Test Message to SQS

Use the AWS CLI to send a test message to the SQS queue:
```sh
aws sqs send-message --queue-url "https://sqs.us-west-2.amazonaws.com/975049981009/switchee-sqs-us-west-2" --message-body '{
  "property_id": 1234567890,
  "lat": 51.5047324,
  "lon": -0.0978885,
  "start_date": "2023-12-01",
  "end_date": "2023-12-31"
}'
```

### Verify the Results

1. **Check CloudWatch Logs**:
   - Ensure the Lambda function executed without errors and logged the expected output.

2. **Verify DynamoDB Entries**:
   - Navigate to the DynamoDB console.
   - Check for new entries in the table with the property ID and aggregated weather data.

### Screenshots

#### Lambda Function Deployment
![Lambda Function](lambda.png)

#### SQS Queue
![SQS Queue](sqs.png)

#### DynamoDB Table
![DynamoDB Table](DynamoDB.png)

#### Test Verification
![Test Verification](test_verification.png)

## Conclusion

This project demonstrates the use of AWS Lambda to process and store weather data from the Open Meteo API, leveraging SQS for message queuing and DynamoDB for storage. The infrastructure is managed using Terraform, ensuring a deployable and scalable solution.

---

### Notes and Observations

- The Lambda function uses Python's `requests` library to interact with the Open Meteo API.
- Data aggregation is performed using the `median` function from Python's `statistics` module.
- DynamoDB requires the use of `Decimal` types for numeric data, which necessitated converting float values to `Decimal` before storage.
- Terraform was instrumental in setting up and managing the necessary AWS resources, ensuring consistent and repeatable deployments.

### Potential Improvements

- Implement additional error handling and retries for API requests.
- Optimize the data aggregation process for performance improvements.
- Expand the solution to support other types of weather data or additional geographic locations.
