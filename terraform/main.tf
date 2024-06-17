# IAM role for Lambda execution
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

data "aws_caller_identity" "current" {}
output "is_localstack" {
  value = data.aws_caller_identity.current.id == "000000000000"
}

# IAM policy for Lambda execution role
resource "aws_iam_policy" "lambda_execution_policy" {
  name        = "lambda_execution_policy"
  description = "Policy for Lambda execution role"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "arn:aws:logs:*:*:*"
      }
      {
        Effect   = "Allow",
        Action   = "s3:GetObject",
        Resource = "arn:aws:s3:::source-*/*" 
      },
      {
        Effect   = "Allow",
        Action   = "s3:PutObject",
        Resource = "arn:aws:s3:::destination-*/*" 
      }
    ]
  })
}

# Attach IAM policy to Lambda execution role
resource "aws_iam_role_policy_attachment" "lambda_execution_policy_attachment" {
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
  role       = aws_iam_role.lambda_execution_role.name
}

# Lambda function
resource "aws_lambda_function" "image_processing_lambda" {
  filename         = "${path.module}/deployment.zip"
  function_name    = "image_processing_lambda"
  role             = aws_iam_role.lambda_exec_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.8"
  timeout          = 60

  environment {
    variables = {
      SOURCE_BUCKET = aws_s3_bucket.source_bucket.id
    }
  }
}

# S3 bucket for source images
resource "aws_s3_bucket" "source_bucket" {
  bucket_prefix = "source-"
  acl           = "private"
}

# S3 bucket for processed images
resource "aws_s3_bucket" "source_bucket" {
  bucket_prefix = "destination-"
  acl           = "private"
}

data "archive_file" "lambda_deployment" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/deployment.zip"
}

# Generate list of object keys
locals {
  object_keys = [for i in range(5) : "test_object_${i}.txt"]
}

# Create objects in the source bucket
resource "aws_s3_object" "source_objects" {
  count   = length(local.object_keys)
  bucket  = aws_s3_bucket.source_bucket.bucket
  key     = local.object_keys[count.index]
  content = "This is test object ${count.index}" # Sample content for the objects
}

