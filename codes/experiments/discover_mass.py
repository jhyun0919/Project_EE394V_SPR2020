from opf_solver import *
from dc_opf_preprocess import *
import numpy as np
import pandas as pd
import math
from tqdm import trange


def overlap_checker(new, origins):
    is_overlap = False
    for origin in origins:
        if new == origin:
            is_overlap = True
    return is_overlap


def discover_mass(alpha, epsilon, delta, gamma, mu, std_scaler, opf_data):
    # compute c amd M_low
    c = 2 * gamma / pow(epsilon, 2)
    M_low = 1 + pow(gamma / (delta * (gamma - 1)), 1 / (gamma - 1))

    # initialized
    M = 1  # num of samples
    discovered_active_sets = []  # empty set
    W = []
    
    # get constraints
    gen_constraints = get_gen_constraints(opf_data)
    flow_constraints = get_flow_constraints(opf_data)

    # iteration
    while True:
        # calculate window size Window_M
        Window_M = c * max(math.log(M_low), math.log(M))
        try:
            Window_M_1 = c * max(math.log(M_low), math.log(M - 1))
        except ValueError:
            Window_M_1 = 0

        # draw additional samples
        # solve OP for each samples; obtain new active sets
        new_active_sets = []
        additional_sample_size = int(1 + Window_M - Window_M_1)
        X = np.zeros(additional_sample_size)
        for i in trange(additional_sample_size):
            # create uncertainty realization
            w = create_w(opf_data, mu, std_scaler)
            W.append(w)
            # solve DC-OPF
            active_constraints = DC_OPF_solver(opf_data=opf_data,
                                               gen_constraints=gen_constraints,
                                               flow_constraints=None,
                                               uncertainty_w=w,
                                               verbose=False,
                                               dual=False)

            is_overlap = overlap_checker(list(active_constraints['idx_vec']),
                                         discovered_active_sets)
            if not is_overlap:
                X[i] = 1
            new_active_sets.append(list(active_constraints['idx_vec']))

        # add the newly observed active sets
        discovered_active_sets = discovered_active_sets + new_active_sets

        # compute Rate of discovery over the window size Window_M ???
        Rate_discovery = (1 / Window_M) * sum(X)
        print("Rate discovery = {}".format(Rate_discovery))
        # update M
        M = M + 1
        if Rate_discovery < alpha - epsilon:
            break

    return np.array(discovered_active_sets), np.array(W), M, Rate_discovery


def plot_active_set_dist(discovered_active_sets, filepath):
    discovered_dist = discovered_active_sets.sum(axis=0, dtype='float')
    discovered_dist = discovered_dist / sum(discovered_dist)
    
    plot_data = {}
    for i in range(len(discovered_dist)):
        plot_data[str(i+1)] = discovered_dist[i]
        
    df = pd.DataFrame({'Label':range(len(discovered_dist)), 'p.d.f.':discovered_dist})
    ax = df.plot.bar(x='Label', y='p.d.f.', figsize=(8, 6), legend=False)
    ax.set_ylabel("p.d.f.")
    
    ax.figure.savefig(filepath)