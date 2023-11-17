from typing import Optional
import argparse
from collections import defaultdict
import zipfile
import os
import json


def load_document_mapping() -> dict:
    file_location = os.path.join(
        os.path.dirname(__file__), "grant_opportunity_to_zip_names.json"
    )
    with open(file_location, "r") as f:
        return json.load(f)


def unzip_and_map_files(
    zip_directory: str, opportunity_id_to_zip_files: Optional[dict]
) -> dict[int, list[str]]:
    zip_files = os.listdir(zip_directory)
    opportunity_id_to_files = defaultdict(list)
    doc_mapping = opportunity_id_to_zip_files or load_document_mapping()
    for grant_opp, zip_files in doc_mapping.items():
        for zip_file in zip_files:
            with zipfile.ZipFile(os.path.join(zip_directory, zip_file), "r") as zip_ref:
                zip_ref.extractall(zip_directory)

                # Iterate over the contents of the unzipped file
                for file_name in zip_ref.namelist():
                    full_path = os.path.join(zip_directory, file_name)
                    if os.path.isfile(full_path):
                        opportunity_id_to_files[grant_opp].append(full_path)
    return opportunity_id_to_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unpack and map zip files")
    parser.add_argument("--zip_directory", type=str, help="Path to check for zip files")
    args = parser.parse_args()
    opportunity_id_to_files = unzip_and_map_files(args.zip_directory)
    with open(
        os.path.join(
            os.path.dirname(__file__), "grant_opportunity_to_unzipped_fnames.json"
        ),
        "w",
    ) as f:
        json.dump(opportunity_id_to_files, f)
