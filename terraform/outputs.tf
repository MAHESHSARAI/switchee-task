output "sqs_queue_url" {
  value = aws_sqs_queue.switchee_queue.url
}

output "dynamodb_table_name" {
  value = aws_dynamodb_table.switchee_table.name
}

output "lambda_function_name" {
  value = aws_lambda_function.switchee_lambda.function_name
}
