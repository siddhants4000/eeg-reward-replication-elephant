import numpy as np

def compute_evokeds(epochs):
    return {
        cond: epochs[cond].average()
        for cond in epochs.event_id.keys()
        if len(epochs[cond]) > 0
    }

def mean_amplitude(evoked, ch, tmin, tmax):
    ev = evoked.copy().pick(ch)
    data = ev.data[0]
    times = ev.times
    mask = (times >= tmin) & (times <= tmax)
    return float(np.mean(data[mask]))