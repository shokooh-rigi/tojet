import logging
from datetime import timedelta
from typing import IO
from minio import Minio
from minio.error import S3Error

from tojet import settings

logger = logging.getLogger(__name__)


class MinioHandler:
    def __init__(self, bucket_name: str, file_path: str):
        """
        Initialize the Minio client and bucket configuration.

        :param bucket_name: Name of the MinIO bucket.
        :param file_path: Base file path for objects in the bucket.
        """
        self.bucket_name = bucket_name
        self.file_path = file_path
        self.minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=True,
        )

        # Ensure the bucket exists
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """
        Ensure the bucket exists in MinIO. Create it if it doesn't exist.
        """
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
        except S3Error as e:
            logger.error(f"Failed to ensure bucket: {self.bucket_name}, Exception: {e}")
            raise

    def upload_file(self, file_id: str, file: IO[bytes]) -> str:
        """
        Upload or update a file in MinIO.

        :param file_id: Unique ID for the file.
        :param file: File object to upload.
        :return: The file path in MinIO.
        """
        object_path = f"{self.file_path}{file_id}"
        try:
            self.minio_client.put_object(
                self.bucket_name, object_path, file, length=-1, part_size=10 * 1024 * 1024
            )
            return object_path
        except Exception as e:
            logger.error(f"Failed to upload file: {file_id}, Exception: {e}")
            raise

    def delete_file(self, file_id: str):
        """
        Delete a file from MinIO.

        :param file_id: Unique ID of the file to delete.
        """
        object_path = f"{self.file_path}{file_id}"
        try:
            self.minio_client.remove_object(self.bucket_name, object_path)
        except Exception as e:
            logger.error(f"Failed to delete file: {file_id}, Exception: {e}")
            raise

    def generate_presigned_url(self, file_id: str, expires_in: int = 3600) -> str:
        """
        Generate a presigned URL for a file in MinIO.

        :param file_id: Unique ID of the file.
        :param expires_in: Expiration time for the URL in seconds (default: 1 hour).
        :return: Presigned URL for accessing the file.
        """
        object_path = f"{self.file_path}{file_id}"
        try:
            url = self.minio_client.presigned_get_object(
                self.bucket_name, object_path, expires=timedelta(expires_in)
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for file: {file_id}, Exception: {e}")
            raise

    def list_files(self, prefix: str = ""):
        """
        List all files in a specific directory in MinIO.

        :param prefix: Directory path to list files under.
        :return: List of file objects.
        """
        try:
            objects = self.minio_client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            return [obj.object_name for obj in objects]
        except Exception as e:
            logger.error(f"Failed to list files in prefix: {prefix}, Exception: {e}")
            raise
