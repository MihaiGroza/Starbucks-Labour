import pandas
import pandas as pd
import requests

url = "https://unionelections.org/data/starbucks/"
html = requests.get(url)

tables = pandas.read_html(html.text)
union_elections = tables[1]
union_elections.to_csv("union_elections.csv",index=False)
