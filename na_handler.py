import pandas as pd
import numpy as np

df = pd.read_csv("hasznaltautohu_db.csv", encoding="ISO-8859-1")

# a hianyzo futott kilometereket az adott évjaratu autok futott kilometerenek atlagaval potoltam
means = df.groupby(["EVJARAT"], as_index=False).mean()

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
    new_df.loc[i] = row
    if pd.isna(row["FUTOTT KILOMETER"]):
        new_df.loc[i, "FUTOTT KILOMETER"] = round(means[means["EVJARAT"] == row["EVJARAT"]]["FUTOTT KILOMETER"].tolist()[0])


new_df.to_csv("hasznalautohu_na_mentes_db.csv", encoding="ISO-8859-1", sep=",", index=False)





