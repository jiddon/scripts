import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.ticker as ticker
from datetime import datetime

def get_lumi():
    """
    ATLAS ready recorded from:
    https://atlasop.cern.ch/page.php?page=https://atlas.web.cern.ch/Atlas/GROUPS/DATAPREPARATION/DataSummary/&height=3000
    dates refer to week start
    """
    lumi_fb = [
        [datetime(2022, 8, 22), 1.161],
        [datetime(2022, 8, 15), 2.994],
        [datetime(2022, 8, 8), 2.594],
        [datetime(2022, 8, 1), 2.266],
        [datetime(2022, 7, 25), 0.99],
        [datetime(2022, 7, 18), 334e-3],
        [datetime(2022, 7, 11), 67.04e-3],
        [datetime(2022, 7, 4), 7.91e-3],
        [datetime(2022, 6, 27), 1.963e-6],
        [datetime(2022, 6, 20), 0.917e-6],
        [datetime(2022, 6, 13), 268.8e-9],
        [datetime(2022, 6, 6), 0],
        [datetime(2022, 5, 30), 1.191e-6],
        [datetime(2022, 5, 23), 870e-9],
        [datetime(2022, 5, 16), 0],
        [datetime(2022, 5, 9), 0],
        [datetime(2022, 5, 2), 0],
        [datetime(2022, 4, 25), 0],
        [datetime(2022, 4, 18), 0],
        [datetime(2022, 4, 11), 0],
        [datetime(2022, 4, 4), 0],
        [datetime(2022, 3, 28), 0],
        ]
    ti_lumi_fb = {"date":[], "integrated lumi ($fb^{-1}$)":[]} # total integrated lumi fb
    ti_lumi_list = []
    lumi_fb.reverse()
    for n,i in enumerate(lumi_fb):
        if n == 0:
            ti_lumi_fb["date"].append(i[0])
            ti_lumi_fb["integrated lumi ($fb^{-1}$)"].append(i[-1])
            ti_lumi_list.append(i[-1])
        else:
            #ti_lumi_fb[i[0]] = i[-1] + ti_lumi_list[-1]
            ti_lumi_fb["date"].append(i[0])
            ti_lumi_fb["integrated lumi ($fb^{-1}$)"].append(i[-1] + ti_lumi_list[-1])
            ti_lumi_list.append(i[-1] + ti_lumi_list[-1])
    return ti_lumi_fb

def read_to_dict(filename):
    data = {}
    rodname = None
    with open(filename, "r") as f:
        for line in f:
            if "ATLPIX" in line:
                rodname_start = line.find("LI")
                rodname = line[rodname_start:].strip()
                print(f"found rod: {rodname}")
                assert rodname
                data[rodname] = {"date":[], "HV_I (mA)":[]}
            else:
                cols = line.split()
                date_ = cols[0].split(".")
                date = datetime(int(date_[0]), int(date_[1].lstrip("0")), int(date_[2]))
                time = cols[1]
                value = float(cols[2])
                data[rodname]["date"].append(date)
                data[rodname]["HV_I (mA)"].append(value)
    return data   

def fmt(s):
    try:
        if float(s) > 0.1:
            n = "{:.2f}".format(float(s))
        else:
            n = "{:.2e}".format(float(s))
    except:
        n = ""
    return n


if __name__=="__main__":
    lumi = get_lumi()
    df_lumi = pd.DataFrame.from_dict(lumi)
    df_lumi["date"] = df_lumi["date"].astype("datetime64")
    df_lumi_date = df_lumi["date"].dt.isocalendar()
    df_lumi["week"] = df_lumi_date["week"]
    weeks = df_lumi["week"].values
    lumis = df_lumi["integrated lumi ($fb^{-1}$)"].values
    lumi_map = {}
    for n,i in enumerate(weeks):
        lumi_map[i] = lumis[n]

    data = read_to_dict("ibl_high_leakage.txt")
    dfs = []
    rods = []
    for k in data.keys():
        df = pd.DataFrame.from_dict(data[k])
        df["date"] = df["date"].astype("datetime64")
        df_date = df["date"].dt.isocalendar()
        df["week"] = df_date["week"]
        df["day"] = df_date["day"]+ (7*df_date["week"])
        df["integrated lumi ($fb^{-1}$)"] = df["week"].map(lumi_map)
        dfs.append(df)
        rods.append(k)

    # per day
    plt.figure(figsize=(16,9))
    for n,df in enumerate(dfs):
        ax = plt.subplot(2, 2, n+1)
        ax.title.set_text(rods[n])
        ax = sns.boxplot(x="day", y="HV_I (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)
        n = 7  # Keeps every 7th label
        [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
        plt.tight_layout()
        plt.savefig("HV_I_per_day.png")

    # per week
    plt.figure(figsize=(16,9))
    for n,df in enumerate(dfs):
        ax = plt.subplot(2, 2, n+1)
        ax.title.set_text(rods[n])
        ax = sns.boxplot(x="week", y="HV_I (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)
        plt.tight_layout()
        plt.savefig("HV_I_per_week.png")

    # per weekly integrated lumi
    plt.figure(figsize=(16,9))
    for n,df in enumerate(dfs):
        ax = plt.subplot(2, 2, n+1)
        ax.title.set_text(rods[n])
        ax = sns.boxplot(x="integrated lumi ($fb^{-1}$)", y="HV_I (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)

        ax.set_xticklabels([fmt(label.get_text()) for label in ax.get_xticklabels()])

        plt.xticks(rotation=45)
    
        plt.tight_layout()
        plt.savefig("HV_I_per_weekly_lumi.png")
    plt.show()


