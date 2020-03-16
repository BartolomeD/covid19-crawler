import os
import re
import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup


URL = "https://www.worldometers.info/coronavirus/"

TABLE_IDS = (
    "table3",
    "main_table_countries",
)

__DATE_FMT__ = "%Y%m%d%H%M%S"


def _fmt_column(col):
    return col.strip().lower().replace(" ", "").replace("total", "").split(",")[0]


def main(url, html=None):

    if html:
        with open(html, 'r') as f:
            html = f.read()

        date_string = re.search(r"(\d{14})", html).group()
        crawled_at = datetime.datetime.strptime(date_string, __DATE_FMT__)

    else:
        html = requests.request("GET", url).text
        crawled_at = datetime.datetime.utcnow()

    soup = BeautifulSoup(html, "lxml")

    for table_id in TABLE_IDS:
        table = soup.find("table", id=table_id)

        if table:
            break

    if not table:
        raise ValueError("table_id not found.")

    data = pd.read_html(str(table))[0]

    data.insert(
        loc=0,
        column="crawled_at",
        value=crawled_at
    )

    data = data.astype({
        "crawled_at": "datetime64[ns]"
    })

    if not os.path.isdir("data/"):
        os.mkdir("data/")

    data.columns = [_fmt_column(col) for col in data.columns]

    filename = crawled_at.strftime(__DATE_FMT__) + ".csv"
    data.to_csv(os.path.join("data/", filename), index=False)

    return None


if __name__ == "__main__":

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--html", type=str, default=None)
    args = parser.parse_args()

    main(
        url=URL,
        html=args.html
    )
