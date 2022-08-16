import numpy as np
import matplotlib.pyplot as plt
import random

def get_rand_number(max):
    return random.uniform(0, max)

def get_rand_step(min, step):
    _max = round(60./step)
    return step*random.uniform(min, _max)

def get_rand_gauss(mean, sigma):
    gauss = random.gauss(mean, sigma)
    return abs(gauss)

def get_gauss_min_cut(mean, sigma, min_cut):
    n = get_rand_gauss(5,3)
    if n > min_cut:
        return n
    else:
        while n < min_cut:
            n = get_rand_gauss(5,3)
        return n

def generate_samples(num_samples, w=None, x=None, y=None, z=None, n=None):
    """
    Generate noise n% of the time, one FE loss x% of
    the time and two FE loss y% of the time. Tune x,
    y and n to see if distibution looks like reality.
    """
    ########## Settings ##########
    if not w:
        w = 0.4
    if not x:
        x = 0.3
    if not y:
        y = 0.1
    if not z:
        z = 0.1
    if not n:
        n = 0.1 # noise

    meanw = 5 # mean for small drops
    stdw = 3 # stdev for small drops
    meanx = 18.75 # mean for one FE loss
    stdx = 3
    meany = 2*18.75 # mean for 2 FE loss
    stdy = 3
    meanz = 3*18.75
    stdz = 3
    ##############################

    samples = []
    for i in range(round(w*num_samples)):
        samples.append(get_gauss_min_cut(meanw, stdw, 5)) # cut < 5 to match real cut
    for i in range(round(x*num_samples)):
        samples.append(get_rand_gauss(meanx, stdx))
    for i in range(round(y*num_samples)):
        samples.append(get_rand_gauss(meany, stdy))
    for i in range(round(z*num_samples)):
        samples.append(get_rand_gauss(meanz, stdz))
    # let's sprinkle some noise everywhere:
    for i in range(round(n*num_samples)):
        samples.append(get_rand_step(5,2.08))
    return samples

def plot(data):
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    plt.hist(data, bins=[i for i in range(0, 65, 5)])
    ax.set_xlabel("Drop size (mA)", fontsize=18)
    ax.set_ylabel("Frequency", fontsize=18)
    ax.tick_params(axis="both", labelsize=14)
    plt.tight_layout()
    plt.show()
    plt.close()

if __name__=="__main__":
    #samples = generate_samples(20000)
    samples = generate_samples(5000)
    plot(samples)
