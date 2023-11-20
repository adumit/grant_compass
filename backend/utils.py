import os

import boto3
from botocore.exceptions import NoCredentialsError, DataNotFoundError, ClientError


def download_file_from_s3(
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
    except ClientError:
        print(f"File {s3_object_key} not found in bucket {bucket_name}")
