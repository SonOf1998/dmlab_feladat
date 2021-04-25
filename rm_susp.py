import pandas as pd
import numpy as np

df = pd.read_csv("hasznalautohu_db2.csv", encoding="ISO-8859-1")


new_df = pd.DataFrame({
                    "BRAND": pd.Series([], dtype="str"),
                    "JARMU JELLEGE": pd.Series([], dtype="str"),
                    "UZEMANYAGTIPUS": pd.Series([], dtype="str"),
                    "EVJARAT": pd.Series([], dtype="int"),
                    "HENGERURTARTALOM (CM3)": pd.Series([], dtype="int"),
                    "TELJESITMENY (LE)": pd.Series([], dtype="int"),
                    "FUTOTT KILOMETER": pd.Series([], dtype="int"),
                    "AR (HUF)": pd.Series([], dtype="int"),
                })


for i in range(len(df)):
    print(i)
    row = df.iloc[i]
    if (row["EVJARAT"] < 2019 and row["FUTOTT KILOMETER"] <= 1000) or row["EVJARAT"] < 1982 or row["FUTOTT KILOMETER"] > 1500000:
        continue

    new_df.loc[i] = row


new_df.to_csv("hasznalautohu_db.csv", encoding="ISO-8859-1", sep=",", index=False)