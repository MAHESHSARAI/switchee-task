import os
import boto3

# Initialize boto3 clients
sqs_client = boto3.client("sqs")
dynamodb = boto3.resource("dynamodb")

DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
