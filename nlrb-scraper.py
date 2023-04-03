import pandas
from bs4 import BeautifulSoup
import requests
import pandas as pd
import math
import time


def find_last_page():
    html=requests.get("https://www.nlrb.gov/search/case/%22starbucks%20corporation%22%20OR%20%22siren%20retail%22?rows=50&page=0&sort=desc")
    soup = BeautifulSoup(html.text,"lxml")
    number_results = soup.find('span', {"id":"total_results_num"})
    last_page = round(float(number_results.text.strip())/50)
    return last_page

def clean_case(case,side):
    case_left = case.find("div", class_=side).text.strip()
    case_left = case_left.replace('\n', ":")
    split_case = case_left.split(":")
    removed_labels = split_case[1::2]
    return removed_labels

def parse_page(page,storage,retries):
    try:
        html=requests.get(f"https://www.nlrb.gov/search/case/%22starbucks%20corporation%22%20OR%20%22siren%20retail%22?rows=50&page={page}&sort=desc")
        soup = BeautifulSoup(html.text,"lxml")
        cases = soup.find_all('div', class_="wrapper-main-content")
        print(len(cases))
        for case in cases:

            case_right = clean_case(case,"right-div")
            case_left = clean_case(case,"left-div")
            storage.loc[len(storage)] = case_left + case_right
        return storage
    except:
        if retries<1:
            raise ValueError("No more retries")
        time.sleep(120)
        return parse_page(page,storage,retries= retries-1)

pandas.set_option('display.max_columns',None)
nlrb_data = pd.DataFrame(columns=["Case Number","Data Filed","Status","Location", "Region Assigned"])

pages = find_last_page()

time.sleep(20)
for page in range(pages):
    time.sleep(30)
    nlrb_data = parse_page(page, nlrb_data,3)
    print(page)

print(nlrb_data.describe())
nlrb_data.to_csv("nlrb.csv",index=False)
