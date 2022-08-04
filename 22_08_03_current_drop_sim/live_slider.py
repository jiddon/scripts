import sim_lib as sl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def update(val):
    data = sl.generate_samples(5000, True, n=sn.val)
    ax.cla()
    ax.hist(data, bins=[i for i in range(0, 65, 5)])
    plt.draw()

def reset(event):
    SN.reset()

ax = plt.subplot(111)
plt.subplots_adjust(left=0.25, bottom=0.25)

# initial parameters:
w = 0.4 # small drops
x = 0.3 # one FE
y = 0.1 # two FEs
z = 0.1 # three FEs
n = 0.1 # noise

data = sl.generate_samples(5000, True, w, x, y, z, n)
plt.hist(data, bins=[i for i in range(0, 65, 5)])

axn = plt.axes([0.25, 0.1, 0.65, 0.03])
sn = Slider(ax=axn,label='Noise (%)',valmin=0,valmax=1,valinit=n)

sn.on_changed(update)

plt.show()
