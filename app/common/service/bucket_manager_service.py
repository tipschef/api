import os
from dataclasses import dataclass, field
from typing import IO
from typing import List, Optional

from fastapi import UploadFile
from google.cloud import storage
from google.cloud.storage import Client


@dataclass
class BucketManagerService:
    env: str
    bucket_name: str = field(init=False)
    bucket_client: Client = field(init=False)

    def __post_init__(self) -> None:
        self.bucket_name = f'tipschef-{self.env}-recipes'
        self.bucket_client = storage.Client()

    def save_file(self, path: str, content: Optional[IO]) -> str:
        bucket = self.bucket_client.get_bucket(self.bucket_name)
        blob = bucket.blob(path)
        with content as file_content:
            blob.upload_from_file(file_content)
            blob.make_public()
            return blob.public_url

    def get_list(self, path: str):
        bucket = self.bucket_client.get_bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=path)

        return blobs

    def save_files(self, paths: List[UploadFile]) -> List[str]:
        return [self.save_file(filepath.filename, filepath.file) for filepath in paths]


def get_bucket_manager_service() -> BucketManagerService:
    return BucketManagerService(os.getenv('PROJECT_ENV'))
