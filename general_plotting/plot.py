import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
import pandas as pd
import numpy as np
import fire

def read_csv(filename):
    """
    Read nicely formatted csv into pandas dataframe.
    """
    print(pd.read_csv(filename))
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

    def plot(self, x, y):
        """
        Line plot.
        """
        self._df.plot(x,y)
        plt.tight_layout()
        plt.show()

    def correlation(self):
        """
        Correlation matrix.
        """
        corr = self._df.corr()
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        plt.figure()
        ax = plt.subplot()
        sns.heatmap(corr, cmap=cmap, square=True, annot=True)
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom + 0.5, top - 0.5)
        plt.tight_layout()
        plt.show()

    def regression(self, x, y):
        """
        Linear regression.
        """
        g = sns.jointplot(x=x, y=y, data=self._df, kind='reg')
        r, p = stats.pearsonr(self._df[x], self._df[y])
        g.ax_joint.annotate(f'$\\rho = {r:.3f}$',
                           xy=(0.1, 0.9), xycoords='axes fraction',
                           ha='left', va='center',
                           bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
        plt.show()


if __name__=="__main__":
    fire.Fire(Plots)
    
