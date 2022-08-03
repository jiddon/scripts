import matplotlib.pyplot as plt
import matplotlib.dates
from datetime import datetime

def get_data():
    """
    fill dict
    """
    data = {
        datetime(2022,8,3):  {"thr":{"mean":1430, "std":66}, "tot":{"mean":9.97, "std":0.24}, "noise":{"mean":153, "std":14}},
        datetime(2022,7,27): {"thr":{"mean":1432, "std":48}, "tot":{"mean":10.36, "std":0.14}, "noise":{"mean":149, "std":15}},
        datetime(2022,7,12): {"thr":{"mean":1475, "std":20}, "tot":{"mean":10.35, "std":0.06}, "noise":{"mean":148, "std":16}},
        datetime(2022,6,7):  {"thr":{"mean":1477, "std":22}, "tot":{"mean":10.34, "std":0.05}, "noise":{"mean":147, "std":18}},
        datetime(2022,6,3):  {"thr":{"mean":1484, "std":16}, "tot":{"mean":10.33, "std":0.04}, "noise":{"mean":147, "std":16}},
        datetime(2022,5,25): {"thr":{"mean":1481, "std":15}, "tot":{"mean":10.32, "std":0.04}, "noise":{"mean":148, "std":17}},
        datetime(2022,5,10): {"thr":{"mean":1482, "std":16}, "tot":{"mean":10.3, "std":0.04}, "noise":{"mean":147, "std":17}},
        datetime(2022,5,2):  {"thr":{"mean":1487, "std":15}, "tot":{"mean":10.28, "std":0.04}, "noise":{"mean":148, "std":17}},
        datetime(2022,4,26): {"thr":{"mean":1489, "std":14}, "tot":{"mean":10.27, "std":0.04}, "noise":{"mean":148, "std":17}},
        datetime(2022,4,20): {"thr":{"mean":1495, "std":13}, "tot":{"mean":10.24, "std":0.04}, "noise":{"mean":148, "std":17}},
        datetime(2022,4,4):  {"thr":{"mean":1504, "std":11}, "tot":{"mean":10.17, "std":0.03}, "noise":{"mean":148, "std":17}},
        #datetime(2021,10,13):{"thr":{"mean":1522, "std":15}, "tot":{"mean":10.03, "std":0.03}, "noise":{"mean":148, "std":18}},
        #datetime(2018,12,6): {"thr":{"mean":2022, "std":70}, "tot":{"mean":, "std":}, "noise":{"mean":144, "std":13}},
    }

    return data

def plot(data, key):
    """
    plot measurable over time
    """
    key_to_label = {"thr": "Threshold ($e^{-}$)", "tot": "ToT (s)", "noise": "Average noise per normal pixel ($e^{-}$)"}
    x, y, yerr = ([] for i in range(3))
    for date in data.keys():
        x.append(date)
        y.append(data[date][key]["mean"])
        yerr.append(data[date][key]["std"])
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    plt.errorbar(x,y,yerr, fmt="xk", ecolor="r")
    ax.set_xlabel("Date of monitoring scan", fontsize=18)
    ax.set_ylabel(key_to_label[key], fontsize=18)
    ax.tick_params(axis="both", labelsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(key+".png")
    #plt.show()
    print(f"saved "+key+".png")
    plt.close()

if __name__=="__main__":
    data = get_data()
    keys = ["thr", "tot", "noise"]
    for k in keys:
        plot(data, k)
