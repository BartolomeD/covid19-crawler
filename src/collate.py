import os
import datetime
import pandas as pd

DATA_PATH = "data/"
USE_COLUMNS = [
    "crawled_at",
    "country",
    "cases",
    "deaths",
    "recovered",
    "serious"
]

data = []

for file in os.listdir(DATA_PATH):

    df = pd.read_csv(os.path.join(DATA_PATH, file))

    try:
        data.append(df[USE_COLUMNS])

    except KeyError:
        print("Error for '{0}'.".format(file))

data = pd.concat(
    objs=data,
    axis=0,
    sort=False,
    ignore_index=True
).set_index(
    keys=['country', 'crawled_at']
).sort_index().fillna(0)

d["active"] = d['cases'] - d['deaths'] - d['recovered']

d["recovery_rate"] = d["recovered"] / (d["recovered"] + d["deaths"])
d["death_rate"] = d["deaths"] / (d["recovered"] + d["deaths"])

key_metrics = ["active", "cases", "deaths", "recovered"]

for metric in key_metrics:
    d[f"log_{metric}"] = np.log1p(d[metric])

data.to_csv(os.path.join(DATA_PATH, 'covid19.csv'))
