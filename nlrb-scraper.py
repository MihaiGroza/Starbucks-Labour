import pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd
import math
import time


def number_of_records():
    html=requests.get("https://www.nlrb.gov/search/case/%22starbucks%20corporation%22%20OR%20%22siren%20retail%22?rows=50&page=3&sort=desc")
    soup = BeautifulSoup(html.text,"lxml")
    number_results = int(soup.find('span', {"id":"total_results_num"}).text.strip())
    return number_results

def clean_case(case,side):
    case_left = case.find("div", class_=side).text.strip()
    case_left = case_left.replace('\n', ":")
    split_case = case_left.split(":")
    removed_labels = split_case[1::2]
    return removed_labels

def parse_page(records,storage,retries):
    try:
        html=requests.get(f"https://www.nlrb.gov/search/case/%22starbucks%20corporation%22%20OR%20%22siren%20retail%22?rows={records}&sort=desc")
        soup = BeautifulSoup(html.text,"lxml")
        cases = soup.find_all('div', class_="wrapper-main-content")

        for case in cases:

            case_right = clean_case(case,"right-div")
            case_left = clean_case(case,"left-div")
            storage.loc[len(storage)] = case_left + case_right
        return storage
    except:
        if retries<1:
            raise ValueError("No more retries")
        time.sleep(120)
        return parse_page(records,storage,retries= retries-1)

pandas.set_option('display.max_columns',None)
nlrb_data = pd.DataFrame(columns=["Case Number","Data Filed","Status","Location", "Region Assigned"])

records = number_of_records()

time.sleep(60)
nlrb_data = parse_page(records, nlrb_data,3)
print(nlrb_data.describe())
nlrb_data.to_csv("nlrb.csv",index=False)
