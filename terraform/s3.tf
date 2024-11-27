provider "aws" {
  region = "us-east-1"  
}

resource "aws_s3_bucket" "lambda_s3_bucket" {
  bucket = "lstm_bucket" 
}