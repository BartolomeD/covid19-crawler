import io
import os
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://www.worldometers.info/coronavirus/"

if os.path.isdir("../data/"):
    os.mkdir("../data/")

resp = requests.request("GET", URL)
soup = BeautifulSoup(resp.text, "lxml")

table = soup.find("table", id="main_table_countries")

data = pd.read_html(str(table))[0].iloc[:-1, :]

dtypes = {
    "area": str,
    "crawled_at": "datetime64[D]",
    "total_cases": int,
    "new_cases": float,
    "total_deaths": float,
    "new_deaths": float,
    "total_recovered": float,
    "active_cases": float,
    "critical_cases": float,
    "cases_per_1m_pop": float,
}

data.insert(
    loc=1,
    column="crawled_at",
    value=datetime.datetime.utcnow()
)

data.columns = dtypes.keys()
data = data.astype(dtypes)

filename = str(data.loc[0, "crawled_at"])[:10] + ".csv"
data.to_csv(os.path.join("../data", filename), index=False)
