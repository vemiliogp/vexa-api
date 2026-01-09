"""Storage service module."""

from dataclasses import dataclass
from logging import info
from os import getenv

from boto3 import client
from botocore.client import Config
from fastapi.datastructures import UploadFile


@dataclass
class StorageService:
    """Service to handle storage operations."""

    s3 = client(
        "s3",
        endpoint_url=getenv("MINIO_ENDPOINT_URL"),
        aws_access_key_id=getenv("MINIO_ROOT_USER"),
        aws_secret_access_key=getenv("MINIO_ROOT_PASSWORD"),
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    def save_file(self, bucket_name: str, file: UploadFile) -> str:
        """
        Save a file to the specified bucket.
        """
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except Exception as e:
            info(f"Bucket {bucket_name} may already exist: {e}")

        try:
            object_name = file.filename
            file_content = file.file.read()

            self.s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_content)
        except Exception as e:
            raise e

        try:
            presigned_url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_name},
                ExpiresIn=3600,
            )

            return presigned_url
        except Exception as e:
            info(f"Failed to generate presigned URL: {e}")
            raise e
