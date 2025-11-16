from typing import List, Dict, Optional, Tuple

import boto3
from botocore.config import Config
import os
import re
import uuid

from app.core.config import settings


class StorageService:
    """
    Thin wrapper around S3 storage operations.

    This service abstracts away direct boto3 usage so that routers and other
    services can depend on a simple interface.
    """

    def __init__(self) -> None:
        if not settings.S3_BUCKET_NAME:
            raise ValueError("S3_BUCKET_NAME is not configured")
        if not settings.AWS_REGION:
            raise ValueError("AWS_REGION must be set")

        self._bucket = settings.S3_BUCKET_NAME
        prefix = settings.S3_PREFIX or ""
        self._prefix = prefix if prefix.endswith("/") or prefix == "" else f"{prefix}/"

        self._s3 = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
        )

    @property
    def bucket(self) -> str:
        return self._bucket

    @property
    def prefix(self) -> str:
        return self._prefix

    def upload_file_bytes(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        """
        Upload a file to S3 and return its object key.
        """
        # Preserve the original filename in the object key (with a UUID suffix to avoid collisions)
        base_name = os.path.basename(filename)
        name_without_ext, ext = os.path.splitext(base_name)
        # Sanitize to avoid problematic characters in S3 keys
        safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", name_without_ext) or "file"
        object_key = f"{self._prefix}{safe_name}-{uuid.uuid4().hex}{ext}"

        self._s3.put_object(
            Bucket=self._bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
            Metadata={"original_filename": filename},
        )
        return object_key

    def list_files(self) -> List[Dict[str, Optional[str]]]:
        """
        List all files stored under the configured prefix.
        """
        kwargs = {
            "Bucket": self._bucket,
            "Prefix": self._prefix,
        }
        files: List[Dict[str, Optional[str]]] = []

        while True:
            resp = self._s3.list_objects_v2(**kwargs)
            contents = resp.get("Contents", [])
            for obj in contents:
                key = obj["Key"]

                # Generate a signed URL for preview/download
                signed_url = self._s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket, "Key": key},
                    ExpiresIn=3600,  # 1 hour
                )

                # Try to fetch original filename from object metadata
                # (If this fails for any reason, fall back gracefully)
                original_filename: Optional[str] = None
                try:
                    head = self._s3.head_object(Bucket=self._bucket, Key=key)
                    metadata = head.get("Metadata") or {}
                    original_filename = metadata.get("original_filename")
                except Exception:
                    original_filename = None

                files.append(
                    {
                        "key": key,
                        "size": str(obj["Size"]),
                        "last_modified": obj["LastModified"].isoformat()
                        if obj.get("LastModified")
                        else None,
                        "original_filename": original_filename,
                        "signed_url": signed_url,
                    }
                )
            if resp.get("IsTruncated"):
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            else:
                break

        return files

    def get_file_bytes(self, object_key: str) -> Tuple[bytes, Optional[str], Dict[str, str]]:
        """
        Download a file from S3 and return its bytes, content-type and metadata.
        """
        resp = self._s3.get_object(Bucket=self._bucket, Key=object_key)
        body = resp["Body"].read()
        content_type = resp.get("ContentType")
        metadata = resp.get("Metadata", {}) or {}
        return body, content_type, metadata

