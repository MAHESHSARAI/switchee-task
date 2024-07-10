provider "aws" {
  region = var.aws_region
}

resource "aws_sqs_queue" "switchee_queue" {
  name = "switchee-sqs-${var.aws_region}"
}

resource "aws_dynamodb_table" "switchee_table" {
  name         = "switchee-dynamodb-${var.aws_region}"
  billing_mode = "PAY_PER_REQUEST"

  hash_key  = "property_id"
  range_key = "date"

  attribute {
    name = "property_id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  tags = {
    Name = "switchee-dynamodb-${var.aws_region}"
  }
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/lambda_package"
  output_path = "${path.module}/lambda/lambda_function.zip"
}

resource "aws_lambda_function" "switchee_lambda" {
  function_name = "switchee-lambda-${var.aws_region}"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.8"

  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256

  environment {
    variables = {
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.switchee_table.name
      SQS_QUEUE_URL       = aws_sqs_queue.switchee_queue.url
    }
  }
}

resource "aws_lambda_event_source_mapping" "sqs_mapping" {
  event_source_arn = aws_sqs_queue.switchee_queue.arn
  function_name    = aws_lambda_function.switchee_lambda.arn
  batch_size       = 10
  enabled          = true
}
