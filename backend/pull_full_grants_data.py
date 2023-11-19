import os
import functools
import json

from backend.utils import download_file_from_s3

INPUT_DIR = f"{os.path.dirname(__file__)}/data"


@functools.cache
def get_full_grants_data() -> dict:
    os.makedirs(INPUT_DIR, exist_ok=True)
    grant_data_path = f"{INPUT_DIR}/full_grant_data.json"
    if not os.path.exists(grant_data_path):
        download_file_from_s3(
            "grant-compass-public",
            "test_grants_n=1367-from-nov2-xml.json",
            grant_data_path,
        )
    with open(grant_data_path, "r") as f:
        return json.load(f)
