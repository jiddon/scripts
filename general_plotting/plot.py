import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import fire

def read_csv(filename):
    """
    Read nicely formatted csv into pandas dataframe.
    """
    return pd.read_csv(filename)

class Plots(object):
    """
    Plotting methods.
    """
    def __init__(self, filename):
        self.filename = filename
        self._df = read_csv(filename)

    def print_headers(self):
        """
        Print csv file headers.
        """
        print("Available headers to plot: ")
        for header in self._df.columns.values:
            header.replace("'", "")
            print(f"    {header}")

    def scatter(self, x, y):
        """
        Plot scatter.
        """
        self._df.plot.scatter(x,y)
        plt.tight_layout()
        plt.show()


if __name__=="__main__":
    #    df = read_csv(filename)
    fire.Fire(Plots)
    
