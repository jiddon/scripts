import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates

def get_data():
    data = {
        "IBL": {
            datetime(2022,8,16):  {"thr":{"mean":1509, "std":9}, "tot":{"mean":10.1, "std":0.02}, "tote":{"mean":0.3, "std":0.03}, "thr-rms":{"mean":79.2, "std":10.3}, "noise":{"mean":149.9, "std":14.2}},            
            datetime(2022,8,15):  {"thr":{"mean":1404, "std":76}, "tot":{"mean":9.93, "std":0.28}, "tote":{"mean":0.81, "std":0.16}, "thr-rms":{"mean":126, "std":20}, "noise":{"mean":155, "std":15}},
            datetime(2022,8,3):  {"thr":{"mean":1430, "std":66}, "tot":{"mean":9.97, "std":0.24}, "tote":{"mean":0.63, "std":0.11}, "thr-rms":{"mean":111, "std":15}, "noise":{"mean":153, "std":14}},
            datetime(2022,7,27): {"thr":{"mean":1432, "std":48}, "tot":{"mean":10.36, "std":0.14}, "tote":{"mean":0.42, "std":0.05}, "thr-rms":{"mean":89, "std":12}, "noise":{"mean":149, "std":15}},
            datetime(2022,7,12): {"thr":{"mean":1475, "std":20}, "tot":{"mean":10.35, "std":0.06}, "tote":{"mean":0.31, "std":0.03}, "thr-rms":{"mean":74.6, "std":8}, "noise":{"mean":148, "std":16}},
            datetime(2022,6,7):  {"thr":{"mean":1477, "std":22}, "tot":{"mean":10.34, "std":0.05}, "tote":{"mean":0.3, "std":0.03}, "thr-rms":{"mean":76.3, "std":9.9}, "noise":{"mean":147, "std":18}},
            datetime(2022,6,3):  {"thr":{"mean":1484, "std":16}, "tot":{"mean":10.33, "std":0.04}, "tote":{"mean":0.29, "std":0.02}, "thr-rms":{"mean":76.1, "std":8.4}, "noise":{"mean":147, "std":16}},
            datetime(2022,5,25): {"thr":{"mean":1481, "std":15}, "tot":{"mean":10.32, "std":0.04}, "tote":{"mean":0.29, "std":0.02}, "thr-rms":{"mean":73.5, "std":9.4}, "noise":{"mean":148, "std":17}},
            datetime(2022,5,10): {"thr":{"mean":1482, "std":16}, "tot":{"mean":10.3, "std":0.04}, "tote":{"mean":0.29, "std":0.01}, "thr-rms":{"mean":75.36, "std":9.55}, "noise":{"mean":147, "std":17}},
            datetime(2022,5,2):  {"thr":{"mean":1487, "std":15}, "tot":{"mean":10.28, "std":0.04}, "tote":{"mean":0.29, "std":0.02}, "thr-rms":{"mean":73, "std":9}, "noise":{"mean":148, "std":17}},
            datetime(2022,4,26): {"thr":{"mean":1489, "std":14}, "tot":{"mean":10.27, "std":0.04}, "tote":{"mean":0.29, "std":0.02}, "thr-rms":{"mean":72, "std":8}, "noise":{"mean":148, "std":17}},
            datetime(2022,4,20): {"thr":{"mean":1495, "std":13}, "tot":{"mean":10.24, "std":0.04}, "tote":{"mean":0.28, "std":0.02}, "thr-rms":{"mean":73, "std":9}, "noise":{"mean":148, "std":17}},
            datetime(2022,4,4):  {"thr":{"mean":1504, "std":11}, "tot":{"mean":10.17, "std":0.03}, "tote":{"mean":0.27, "std":0.03}, "thr-rms":{"mean":72, "std":9}, "noise":{"mean":148, "std":17}}
            },
        "PIX":{
            }
    }

    # 2022, 4, 20: TOT is A021-552 (NOT A021-551 as in elog)
    
    return data

def get_lumi():
    """
    ATLAS ready recorded from:
    https://atlasop.cern.ch/page.php?page=https://atlas.web.cern.ch/Atlas/GROUPS/DATAPREPARATION/DataSummary/&height=3000
    """
    lumi_fb = [
        #[datetime(2022, 8, 22), 536.8e-3],
        [datetime(2022, 8, 15), 2.594],
        [datetime(2022, 8, 8), 2.266],
        [datetime(2022, 8, 1), 0.99],
        [datetime(2022, 7, 25), 334e-3],
        [datetime(2022, 7, 18), 67.04e-3],
        [datetime(2022, 7, 11), 7.91e-3],
        [datetime(2022, 7, 4), 1.963e-6],
        [datetime(2022, 6, 27), 0.917e-6],
        [datetime(2022, 6, 20), 268.8e-9],
        [datetime(2022, 6, 13), 0],
        [datetime(2022, 6, 6), 1.191e-6],
        [datetime(2022, 5, 30), 870e-9],
        [datetime(2022, 5, 23), 0],
        [datetime(2022, 5, 16), 0],
        [datetime(2022, 5, 9), 0],
        [datetime(2022, 5, 2), 0],
        [datetime(2022, 4, 25), 0],
        [datetime(2022, 4, 18), 0],
        [datetime(2022, 4, 11), 0],
        [datetime(2022, 4, 4), 0],
        ]
    ti_lumi_fb = {} # total integrated lumi fb
    ti_lumi_list = []
    lumi_fb.reverse()
    for n,i in enumerate(lumi_fb):
        if n == 0:
            ti_lumi_fb[i[0]] = i[-1]
            ti_lumi_list.append(i[-1])
        else:
            ti_lumi_fb[i[0]] = i[-1] + ti_lumi_list[-1]
            ti_lumi_list.append(ti_lumi_fb[i[0]])
    return ti_lumi_fb

def plot(data, key, layer, ax):
    """
    plot measurable over time
    """
    key_to_label = {"thr": "Threshold ($e^{-}$)", "tot": "ToT (s)", "noise": "Avg noise per pix ($e^{-}$)", "tote":"ToT error (s)", "thr-rms": "Threshold RMS ($e^{-}$)" }
    x, y, yerr = ([] for i in range(3))
    for date in data[layer].keys():
        x.append(date)
        y.append(data[layer][date][key]["mean"])
        yerr.append(data[layer][date][key]["std"])
    mean = np.mean(y)
    stdev =np.std(y)

    plt.errorbar(x, y, yerr, fmt="xk", ecolor="r", capsize=2)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(range(1,13))))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True)
    ax.set_ylabel(key_to_label[key], fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    ax.axvline(datetime(2022, 8, 16), color='b', linestyle=(0, (1, 10)))

    if key == "thr":
        ax.axhline(1500, color='k', linestyle='dotted')
        
    plt.tight_layout()

def plot_lumi(data, ax):
    """
    plot measurable over time
    """
    x, y = ([] for i in range(2))
    for date in data.keys():
        x.append(date)
        y.append(data[date])
    mean = np.mean(y)
    stdev =np.std(y)
    plt.step(x, y)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(range(1,13))))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True)
    ax.set_ylabel("Total integrated luminosity $fb^{-1}$", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)
        
    plt.tight_layout()


if __name__=="__main__":
    data = get_data()
    keys = ["thr", "tot", "tote", "thr-rms", "noise"]

    #fig, axs = plt.subplots(nrows=3, ncols=2)
    plt.figure(figsize=(12,10))
    for n,k in enumerate(keys):
        ax = plt.subplot(3, 2, n + 1)
        plot(data, k, "IBL", ax)
    ### legend ###
    lumi = get_lumi()
    ax = plt.subplot(3,2,6)
    plot_lumi(lumi, ax)
    #ax.set_axis_off()
    #ax.text(0.1,0.6, "- Blue line indicates LHC restart")
    #ax.text(0.1,0.5, "- Error bars represent standard deviation")
    #ax.text(0.1,0.4, "- Data taken from elog and ConsoleApp")
    ######
    
    plt.savefig("IBL_monitoring_scan_trends.png")
    print(f"saved IBL_monitoring_scan_trends.png")
    plt.show()
    plt.close()
