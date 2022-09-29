from scipy.stats import weibull_min
from scipy.stats import poisson
import numpy as np
import random as r

def generateWeibullDis(sample_size, sys_energy, energy_required, num_sec):
    # shape = r.randint(4, 5)
    # scale = r.randint(6, 8)
    # x = weibull_min.rvs(shape, loc=0, scale=scale, size=sample_size)
    sample_size = int(sample_size)
    data = np.random.random((sample_size, 1))
    total = [int((sys_energy * energy_required)/num_sec)]
    return corrections(data, total, sample_size)

def generateNormalDis(sample_size, sys_energy, energy_required, num_sec):
    # scale = r.randint(8,10)
    # x =  np.random.normal(loc=0, scale=scale, size=sample_size)
    sample_size = int(sample_size)
    data = np.random.random((sample_size, 1))
    total = [int((sys_energy * energy_required)/num_sec)]
    return corrections(data, total, sample_size)

def generatePoissonDis(sample_size, sys_energy, energy_required, num_sec):
    # scale = r.randint(4, 5)
    # x = poisson.rvs(mu=scale, size=sample_size)
    sample_size = int(sample_size)
    data = np.random.random((sample_size, 1))
    total = [int((sys_energy * energy_required)/num_sec)]
    return corrections(data, total, sample_size)

# Here we ensure the system energy parameter is not compromised
# The Energy generated adds up to sys_energy*energy_required_by_trip_petitions
def corrections(data, total, sample_size):
    data = data/np.sum(data, axis =0) * total
    data = np.round(data)
    remainings = total - np.sum(data, axis = 0)
    for j, r in enumerate(remainings):
        step = 1 if r > 0 else -1
        while r != 0:
            i = np.random.randint(sample_size-1)
            if data[i, j] + step >= 0:
                data[i, j] += step
                r -= step
    return data