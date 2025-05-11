# solar_analysis.py
import numpy as np
import pandas as pd

def analyze_solar_data(df):
    df["Change"] = df["Sensor Output"].diff()

    def analyze(row, idx, data):
        if idx >= 2 and all(np.isclose(data[idx-2:idx+1], data[idx], atol=0.01)):
            return "Gain Saturated - Sun out of feed"
        if idx >= 1 and abs(row["Change"]) > 2.5:
            return "Unusual solar activity - Possible solar flare"
        if row["Change"] > 0.05:
            return "Sun entering feed"
        elif row["Change"] < -0.05:
            return "Sun leaving feed"
        else:
            return "Stable"

    df["Status"] = [analyze(row, idx, df["Sensor Output"].values) for idx, row in df.iterrows()]
    return df
