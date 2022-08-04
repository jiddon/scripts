import sim_lib as sl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

def update(val):
    data = sl.generate_samples(5000, True, n=sn.val, w=sw.val, x=sx.val, y=sy.val, z=sz.val)
    ax.cla()
    ax.hist(data, bins=[i for i in range(0, 65, 5)])
    plt.draw()

def reset(event):
    sn.reset()
    sw.reset()
    sx.reset()
    sy.reset()
    sz.reset()

ax = plt.subplot(111)
plt.subplots_adjust(bottom=0.45)

# initial parameters:
w = 0.4 # small drops
x = 0.3 # one FE
y = 0.1 # two FEs
z = 0.1 # three FEs
n = 0.1 # noise

data = sl.generate_samples(5000, True, w, x, y, z, n)
plt.hist(data, bins=[i for i in range(0, 65, 5)])

#[left, bottom, width, height]
axn = plt.axes([0.25, 0.1, 0.65, 0.03])
axw = plt.axes([0.25, 0.15, 0.65, 0.03])
axx = plt.axes([0.25, 0.2, 0.65, 0.03])
axy = plt.axes([0.25, 0.25, 0.65, 0.03])
axz = plt.axes([0.25, 0.3, 0.65, 0.03])
sn = Slider(ax=axn,label='Noise (%)',valmin=0,valmax=1,valinit=n)
sw = Slider(ax=axw,label='Small drops (%)',valmin=0,valmax=1,valinit=w)
sx = Slider(ax=axx,label='1 FE loss (%)',valmin=0,valmax=1,valinit=x)
sy = Slider(ax=axy,label='2 FE loss (%)',valmin=0,valmax=1,valinit=y)
sz = Slider(ax=axz,label='3 FE loss (%)',valmin=0,valmax=1,valinit=z)

sn.on_changed(update)
sw.on_changed(update)
sx.on_changed(update)
sy.on_changed(update)
sz.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')
button.on_clicked(reset)

plt.show()
