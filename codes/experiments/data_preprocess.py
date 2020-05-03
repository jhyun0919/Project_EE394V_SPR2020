import matlab.engine
import os
import numpy as np
from tqdm import trange
import pickle


def get_Pb_lim(Pg_lim, GB_map):
    Pb_lim = {}

    for g_idx in range(len(GB_map)):
        b_idx = GB_map[g_idx]
        try:
            Pb_lim[b_idx][0] = Pb_lim[b_idx][0] + Pg_lim[g_idx][0]
            Pb_lim[b_idx][1] = Pb_lim[b_idx][1] + Pg_lim[g_idx][1]
        except KeyError:
            Pb_lim[b_idx] = np.zeros(2)
            Pb_lim[b_idx][0] = Pg_lim[g_idx][0]
            Pb_lim[b_idx][1] = Pg_lim[g_idx][1]
    return Pb_lim


def get_Pb(Pg, GB_map):
    Pb = {}

    for g_idx in range(len(GB_map)):
        b_idx = GB_map[g_idx]
        try:
            Pb[b_idx] = Pb[b_idx] + Pg[g_idx]
        except KeyError:
            Pb[b_idx] = Pg[g_idx]
    return Pb


def get_Pg_active_constraints(Pg, Pg_lim):
    active_constraints = np.zeros((len(Pg), 2))

    for g_idx in range(Pg_lim.shape[0]):
        if Pg[g_idx] >= Pg_lim[g_idx][0]:
            active_constraints[g_idx][0] = 1
        if Pg[g_idx] <= Pg_lim[g_idx][1]:
            active_constraints[g_idx][1] = 1

    return np.sum(active_constraints, axis=1) % 2


def get_Pb_active_constraints(Pg, Pg_lim, GB_map):
    Pb = get_Pb(Pg, GB_map)
    Pb_lim = get_Pb_lim(Pg_lim, GB_map)
    Bg_idx = list(Pb.keys())
    active_constraints = np.zeros((len(Bg_idx), 2))
    for i in range(len(Bg_idx)):
        b_idx = Bg_idx[i]
        if Pb[b_idx] >= Pb_lim[b_idx][0]:
            active_constraints[i][0] = 1
        if Pb[b_idx] <= Pb_lim[b_idx][1]:
            active_constraints[i][1] = 1
    return np.sum(active_constraints, axis=1) % 2


def get_F_active_constraints(F, F_lim):
    active_constraints = []

    for f, f_lim in zip(F, F_lim):
        if abs(f) >= abs(f_lim):
            active_constraints.append(1)
        else:
            active_constraints.append(0)

    return np.array(active_constraints)


def merge_active_constraints(Pg_active, Pb_active, F_active):
    return np.array(list(Pg_active) + list(Pb_active) + list(F_active))


def create_dataset(file_name, dataset_size, std_scaler=0.03):
    print("> creating dataset with {}".format(file_name))

    x = []
    y = []

    org_dir = os.getcwd()
    os.chdir('./matpower7.0/')

    eng = matlab.engine.start_matlab()

    data = eng.dc_opf_solver(file_name, 0.03)

    Pg = np.squeeze(np.array(data['Pg']))
    B_idx = np.squeeze(np.array(data['B_idx']))
    GB_map = np.squeeze(np.array(data['GB_map'])).astype(int)
    F = np.squeeze(np.array(data['F']))
    Pg_lim = np.array(data['Pg_lim'])
    F_lim = np.array(data['F_lim'])
    w = np.squeeze(np.array(data['w']))

    for i in trange(dataset_size):
        data = eng.dc_opf_solver(file_name, std_scaler)
        # assing x data
        x.append(np.array(data['w']))
        # assgin y data
        Pg_active = get_Pg_active_constraints(Pg, Pg_lim)
        Pb_active = get_Pb_active_constraints(Pg, Pg_lim, GB_map)
        F_active = get_F_active_constraints(F, F_lim)
        active_constraints = merge_active_constraints(Pg_active, Pb_active,
                                                      F_active)
        y.append(np.array(active_constraints))

    eng.quit()

    os.chdir(org_dir)

    return {'x': np.squeeze(np.array(x)), 'y': np.array(y)}


def save_dataset(test_case, dataset):
    file_name = test_case.split('.')[0]
    file_path = './datasets/'
    file_dir = file_path + file_name + '.pickle'
    outfile = open(file_dir, 'wb')
    pickle.dump(dataset, outfile)
    outfile.close()


def build_datasets(test_cases, dataset_size):
    for test_case in test_cases:
        # create a dataset
        dataset = create_dataset(test_case, dataset_size)
        # save the dataset
        save_dataset(test_case, dataset)
