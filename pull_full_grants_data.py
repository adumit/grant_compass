import os
import functools
import json

import boto3
from botocore.exceptions import NoCredentialsError


def _download_file_from_s3(
    bucket_name: str, s3_object_key: str, local_file_name: str
) -> None:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_DEFAULT_REGION"),
    )
    try:
        s3_client.download_file(bucket_name, s3_object_key, local_file_name)
        print(
            f"Downloaded {s3_object_key} from bucket {bucket_name} to {local_file_name}"
        )
    except NoCredentialsError:
        print("Credentials not available")


@functools.cache
def get_full_grants_data() -> dict:
    grant_data_path = "./data/full_grant_data.json"
    if not os.path.exists(grant_data_path):
        _download_file_from_s3(
            "grant-compass-public",
            "test_grants_n=1367-from-nov2-xml.json",
            grant_data_path,
        )
    with open(grant_data_path, "r") as f:
        return json.load(f)
