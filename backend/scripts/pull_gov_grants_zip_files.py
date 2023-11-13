import argparse
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from ..create_embedded_grants import get_current_grants
import time


def all_downloads_complete(driver):  # Driver is unused, but automatically passed in
    downloads = os.listdir(DOWNLOAD_PATH)
    return not any([x.endswith(".crdownload") for x in downloads])


def download_single_grant(opportunity_id: int):
    print("STARTING SINGLE GRANT DOWNLOAD")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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

    for l in zip_links:
        l.click()
        # Don't click the next link instantly or we might lose earlier ones
        time.sleep(2)

    # waits for all the files to be completed and returns the paths
    WebDriverWait(driver, 120, 1).until(all_downloads_complete)
    driver.quit()


def pull_gov_grants_zip_files():
    current_grants = get_current_grants()
    current_opportunity_ids = [x["OpportunityID"] for x in current_grants]
    for grant_opp in current_opportunity_ids[:10]:
        download_single_grant(grant_opp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download zip files for current grants"
    )
    parser.add_argument(
        "--download_path", type=str, help="Path to check for complete downloads"
    )
    args = parser.parse_args()
    DOWNLOAD_PATH = args.download_path
    pull_gov_grants_zip_files()
