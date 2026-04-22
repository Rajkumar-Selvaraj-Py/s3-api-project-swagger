import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "test")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localstack:4566")
