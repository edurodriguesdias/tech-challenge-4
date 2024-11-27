provider "aws" {
  region = "us-east-1"  
}

resource "aws_ecr_repository" "lambda_repository" {
  name = "lambda-repo"
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function.function_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_s3_bucket.bucket
}
