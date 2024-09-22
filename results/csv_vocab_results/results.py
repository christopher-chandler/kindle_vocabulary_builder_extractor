import pandas as pd
from datetime import datetime

df = pd.read_csv('SC_KINDLE_OASIS.csv')

t = "June 02, 2021 06:34:11 AM"
b = "June 28, 2021 06:25:21 AM"
for i in df.head(151)["timestamp"]:
    if i > t and i < b:
        print(i)