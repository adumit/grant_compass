import argparse
from functools import partial
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from ..create_embedded_grants import get_current_grants
import time


"""

To run this script, run: 
python3 -m backend.scripts.pull_gov_grants_zip_files --download_path <PATH TO YOUR DOWNLOAD FOLDER>
This should be run from the root of the project to download locally.
Note: the method for checking for complete downloads likely does not work on windows

"""


def all_downloads_complete(
    driver, download_path
):  # Driver is unused, but automatically passed in
    downloads = os.listdir(download_path)
    return not any([x.endswith(".crdownload") for x in downloads])


def download_single_grant(driver, opportunity_id: int, download_path: str) -> list[str]:
    driver.get(f"https://www.grants.gov/search-results-detail/{opportunity_id}")

    button_text = "Related Documents"
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//button[contains(text(), '{button_text}')]")
        )
    )

    button.click()

    links = driver.find_elements(By.TAG_NAME, "a")

    # Filter for .zip file links
    zip_links = [l for l in links if ".zip" in l.text]
    files_before = os.listdir(download_path)

    for l in zip_links:
        l.click()
        # Don't click the next link instantly or we might lose earlier ones
        time.sleep(2)

    download_complete_with_path = partial(
        all_downloads_complete, download_path=download_path
    )
    # waits for all the files to be completed and returns the paths
    WebDriverWait(driver, 120, 1).until(download_complete_with_path)
    files_after = os.listdir(download_path)
    new_files = [f for f in files_after if f not in files_before]
    return new_files


def pull_gov_grants_zip_files(
    download_path: str, n_grants: int = -1
) -> dict[int, list[str]]:
    chrome_options = Options()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )

    grant_opportunity_to_fnames = {}
    current_grants = get_current_grants()
    # TODO: A little annoying that this is hard coded, b/c it maps to the same place as the
    # pull_and_embed_documents.py script
    existing_opportunity_ids = {
        str(fname.split("-")[0])
        for fname in os.listdir(
            os.path.join(os.path.dirname(__file__), "embedded_document_results")
        )
        if "embedded-related-document-chunks" in fname
    }
    current_opportunity_ids = [
        x["OpportunityID"]
        for x in current_grants
        if x["OpportunityID"] not in existing_opportunity_ids
    ]
    if n_grants > 0:
        current_opportunity_ids = current_opportunity_ids[:n_grants]
    for i, grant_opp in enumerate(current_opportunity_ids):
        if i % 100 == 0:
            print(f"Downloading grant {i+1} of {len(current_opportunity_ids)}")
        try:
            downloaded_files = download_single_grant(driver, grant_opp, download_path)
        except Exception as e:
            print(f"Error downloading grant {grant_opp}: {e}")
            continue
        grant_opportunity_to_fnames[grant_opp] = downloaded_files
    driver.quit()
    return grant_opportunity_to_fnames


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download zip files for current grants"
    )
    parser.add_argument(
        "--download_path", type=str, help="Path to check for complete downloads"
    )
    parser.add_argument(
        "--n_grants",
        type=int,
        default=-1,
        help="Number of grants to download, -1 for all",
    )

    args = parser.parse_args()
    opportunity_id_to_files = pull_gov_grants_zip_files(
        args.download_path, args.n_grants
    )
    with open(
        os.path.join(os.path.dirname(__file__), "grant_opportunity_to_zip_names.json"),
        "w",
    ) as f:
        json.dump(opportunity_id_to_files, f)
