import os
from datetime import date
import argparse

import openai
import xmltodict
import orjson

from embed import get_embedding


openai.api_key = os.getenv("OPENAI_API_KEY")


def create_grant_test_data(n_grants: int = 50):
    print("Reading in raw data...")
    grants_data = xmltodict.parse(open("./data/GrantsDBExtract20230926v2.xml").read())
    print("Beginning to create embeddings...")
    today = date.today()

    current_grants = sorted(
        [
            x
            for x in grants_data["Grants"]["OpportunitySynopsisDetail_1_0"]
            if "CloseDate" in x
            and x["CloseDate"][-4:] >= f"{today.month:02}{today.day:02}{today.year}"
        ],
        key=lambda x: x["CloseDate"],
        reverse=True,
    )
    small_batch = current_grants[:n_grants]
    embeddings = get_embedding([x["Description"] for x in small_batch])

    for i, item in enumerate(small_batch):
        item["embedding"] = embeddings[i]

    os.makedirs("./test_data", exist_ok=True)
    with open("./test_data/test_grants.json", "wb") as f:
        f.write(orjson.dumps(small_batch))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a small amount of test data")
    parser.add_argument(
        "--num_grants",
        type=int,
        default=50,
        help="The number of grants to create",
    )

    args = parser.parse_args()

    create_grant_test_data(args.num_grants)
