"""Storage service module."""

from dataclasses import dataclass
from logging import info
from os import getenv
from uuid import uuid4

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

    def _create_bucket_if_not_exists(self, bucket_name: str) -> None:
        """Create bucket if it doesn't exist."""
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except Exception as e:
            info(f"Bucket {bucket_name} may already exist: {e}")

    def _generate_presigned_url(self, bucket_name: str, key: str) -> str:
        """Generate presigned URL for object."""
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=3600,
            )
            info(f"Presigned URL generated for {key}")
            return url
        except Exception as e:
            info(f"Failed to generate presigned URL: {e}")
            raise e

    def save_file(self, bucket_name: str, file: UploadFile) -> str:
        """Save an file to the specified bucket."""

        self._create_bucket_if_not_exists(bucket_name)

        try:
            file_content = file.file.read()
            self.s3.put_object(Bucket=bucket_name, Key=file.filename, Body=file_content)
            info(f"File {file.filename} saved to bucket {bucket_name}")
        except Exception as e:
            info(f"Failed to save file: {e}")
            raise e

        return self._generate_presigned_url(bucket_name, file.filename)

    def save_bytes(
        self,
        bucket_name: str,
        file_bytes: bytes,
        file_extension: str,
        file_name: str = None,
    ) -> str:
        """Save bytes to the specified bucket."""

        if not file_name:
            file_name = f"{uuid4()}.{file_extension}"
        else:
            file_name = f"{file_name}.{file_extension}"

        self._create_bucket_if_not_exists(bucket_name)

        try:
            self.s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_bytes)
            info(f"File {file_name} saved to bucket {bucket_name}")
        except Exception as e:
            info(f"Failed to save file: {e}")
            raise e

        return self._generate_presigned_url(bucket_name, file_name)
