import argparse
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
DOWNLOAD_PATH = ""  # This should be changed via running this as main.


def all_downloads_complete(driver):  # Driver is unused, but automatically passed in
    downloads = os.listdir(DOWNLOAD_PATH)
    return not any([x.endswith(".crdownload") for x in downloads])


def download_single_grant(driver, opportunity_id: int) -> list[str]:
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
    files_before = os.listdir(DOWNLOAD_PATH)

    for l in zip_links:
        l.click()
        # Don't click the next link instantly or we might lose earlier ones
        time.sleep(2)

    # waits for all the files to be completed and returns the paths
    WebDriverWait(driver, 120, 1).until(all_downloads_complete)
    files_after = os.listdir(DOWNLOAD_PATH)
    new_files = [f for f in files_after if f not in files_before]
    return new_files


def pull_gov_grants_zip_files(n_grants: int = -1) -> dict[int, list[str]]:
    chrome_options = Options()
    prefs = {"download.default_directory": DOWNLOAD_PATH}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    )

    grant_opportunity_to_fnames = {}
    current_grants = get_current_grants()
    current_opportunity_ids = [x["OpportunityID"] for x in current_grants]
    if n_grants > 0:
        current_opportunity_ids = current_opportunity_ids[:n_grants]
    for i, grant_opp in enumerate(current_opportunity_ids):
        if i % 100 == 0:
            print(f"Downloading grant {i+1} of {len(current_opportunity_ids)}")
        downloaded_files = download_single_grant(driver, grant_opp)
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
    DOWNLOAD_PATH = args.download_path
    opportunity_id_to_files = pull_gov_grants_zip_files(args.n_grants)
    with open(
        os.path.join(os.path.dirname(__file__), "grant_opportunity_to_zip_names.json"),
        "w",
    ) as f:
        json.dump(opportunity_id_to_files, f)
