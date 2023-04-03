from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import scrapelib
import time
import tqdm

options = Options()
options.add_experimental_option("detach", True)

options.add_argument("--window-size=1920,1080")


driver = webdriver.Chrome(options=options)


driver.get("https://www.nlrb.gov/search/case")



wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.ID, 'edit-search-term--4')))
driver.find_element(By.ID,'edit-search-term--4').send_keys("\"siren retail\" OR \"starbucks corporation\"")
driver.find_element(By.ID,"edit-submit--4").click()

wait.until(EC.element_to_be_clickable((By.ID, 'download-button')))
download_link = driver.find_element(By.ID,'download-button')

download_token = driver.get_cookie("nlrb-dl-sessid")["value"]

cache_id=download_link.get_attribute("data-cacheid")
type_of_report=download_link.get_attribute("data-typeofreport")

download_link = (
            "https://www.nlrb.gov"
            + f"/nlrb-downloads/start-download/{type_of_report}/{cache_id}/{download_token}")

bum = scrapelib.Scraper()
response = bum.get(download_link, verify=False)
result = response.json()["data"]

base_url = "https://www.nlrb.gov"

previous = 0
with tqdm.tqdm(
        total=result["total"], desc="NLRB.gov preparing download"
) as pbar:
    while not result["finished"]:
        response = bum.get(
            base_url + "/nlrb-downloads/progress/" + str(result["id"]),
            verify=False,
        )

        result = response.json()["data"]
        print(result["id"])
        # update progress bar
        current = result["processed"]
        print(current)
        pbar.update(current - previous)
        previous = current

driver.get(base_url + result["filename"])