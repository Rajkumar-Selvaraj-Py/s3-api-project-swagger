import boto3
import logging
from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
            endpoint_url=S3_ENDPOINT
        )
        self.bucket_name = "test-bucket"
        self.create_bucket_if_not_exists()

    def create_bucket_if_not_exists(self):
        try:
            buckets = self.s3.list_buckets()
            existing = [b["Name"] for b in buckets.get("Buckets", [])]

            if self.bucket_name not in existing:
                self.s3.create_bucket(Bucket=self.bucket_name)
                logging.info(f"Bucket created: {self.bucket_name}")
            else:
                logging.info(f"Bucket already exists: {self.bucket_name}")
        except Exception as e:
            logging.error(f"Error creating bucket: {e}")

    def upload_file(self, file):
        try:
            self.s3.upload_fileobj(file, self.bucket_name, file.filename)
            logging.info(f"Uploaded {file.filename}")
            return True
        except Exception as e:
            logging.error(f"Upload failed: {e}")
            return False

    def download_file(self, filename):
        try:
            return self.s3.get_object(Bucket=self.bucket_name, Key=filename)
        except Exception as e:
            logging.error(f"Download failed: {e}")
            return None
