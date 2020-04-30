import numpy as np
import math

def create_w(opf_data, mu=0, std_scaler=0.03):
    """
    create uncertainty realization; w vector.
    - shape = bus_v x 1
    """
    bus_v = opf_data['bus']['bus_i'].shape[0]
    d = np.array(opf_data['bus']['Pd'])
    w = []

    for i in range(bus_v):
        sigma_i = d[i] * std_scaler
        w_i = np.squeeze(np.random.normal(mu, sigma_i, 1))
        w.append(w_i)
    w = np.array(w)

    assert (bus_v, ) == w.shape
    return w


def get_d(opf_data):
    """
    loads; d vector.
    - shape = bus_v x 1
    """
    bus_v = opf_data['bus']['bus_i'].shape[0]
    d = np.array(opf_data['bus']['Pd'])
    
    assert (bus_v, ) == d.shape
    return d


def get_H(opf_data):
    """
    mapping from generators to their respective buses; H matrix.
    - shape = bus_v x gen_n 
    """
    bus_v = opf_data['bus']['bus_i'].shape[0]
    gen_n = opf_data['gen']['bus'].shape[0]

    H = np.zeros([bus_v, gen_n])
    for col_idx in range(gen_n):
        row_idx = int(opf_data['gen']['bus'][col_idx]) - 1
        H[row_idx][col_idx] = 1

    assert (bus_v, gen_n) == H.shape
    return H


def get_X(opf_data):
    """
    diagonal matrix with reactance; X matrix.
    - shape = line_m x line_m
    """
    line_m = opf_data['branch'].shape[0]

    X = np.zeros([line_m, line_m])
    for i in range(line_m):
        X[i][i] = opf_data['branch']['x'][i]

    assert (line_m, line_m) == X.shape
    return X


def get_A(opf_data):
    """
    incidence matrix; A matrix.
    - shape = line_m x bus_v
    """
    line_m = opf_data['branch'].shape[0]
    bus_v = opf_data['bus']['bus_i'].shape[0]

    A = np.zeros([line_m, bus_v])
    for i in range(line_m):
        from_bus_idx = int(opf_data['branch']['fbus'][i]) - 1
        to_bus_idx = int(opf_data['branch']['tbus'][i]) - 1
        A[i, from_bus_idx] = 1
        A[i, to_bus_idx] = -1

    assert (line_m, bus_v) == A.shape
    return A


def get_A_r(opf_data):
    """
    reduced incidence matrix; A_r matrix.
    - shape = line_m x (bus_v - 1)
    """
    line_m = opf_data['branch'].shape[0]
    bus_v = opf_data['bus']['bus_i'].shape[0]

    # get A matrix
    A = get_A(opf_data)
    # reduce the slack bus element
    A_r = A[:, 1:]

    assert (line_m, bus_v - 1) == A_r.shape
    return A_r


def get_B_r(opf_data, A_r, X):
    """
    reactance matrix;B_r matrix.
    - shape = (bus_v - 1) x (bus_v - 1)
    """
    bus_v = opf_data['bus']['bus_i'].shape[0]
    B_r = np.matmul(
        np.matmul(np.transpose(A_r), np.linalg.inv(X)),
        A_r)

    assert (bus_v - 1, bus_v - 1) == B_r.shape
    return B_r


def get_PTDF(opf_data, X, A_r, B_r):
    """
    PTDF (Injection Shift Factor); M matrix.
    - shape = line_m x bus_v
    """
    line_m = opf_data['branch'].shape[0]
    bus_v = opf_data['bus']['bus_i'].shape[0]

    # create a zero col vector
    zero_col = np.zeros([line_m, 1])
    # build PTDF
    PTDF = np.hstack(
        (zero_col, np.matmul(np.matmul(np.linalg.inv(X), A_r),
                             np.linalg.inv(B_r))))

    assert (line_m, bus_v) == PTDF.shape
    return PTDF


# def angle_assign(ang, idx, raw_angle):
#     if ang[idx] == 0:
#         ang[idx] = raw_angle
#     else:
#         if ang[idx] == raw_angle:
#             pass
#         else:
#             print("angle value not matched")
#             exit()
#     return ang

# def get_f_range_(opf_data, X, A):
#     """
#     line flow limitation range; [f_min vector, f_max vector]
#     - shape = bus_v x (1 x 2)
#     """
#     line_m = opf_data['branch'].shape[0]
#     bus_v = opf_data['bus']['bus_i'].shape[0]

#     # load angle data
#     ang_max_ = np.array(opf_data['branch']['angmax'])
#     ang_min_ = np.array(opf_data['branch']['angmin'])

#     f_bus = np.array(opf_data['branch']['fbus'])
#     t_bus = np.array(opf_data['branch']['tbus'])

#     # assigning angel value according to bus number
#     ang_max = np.zeros([bus_v, 1])
#     ang_min = np.zeros([bus_v, 1])
#     for i in range(line_m):
#         #         ang_max[int(f_bus[i]-1)] = math.radians(ang_max_[i])
#         #         ang_max = angle_assign(ang_max, int(f_bus[i]-1), math.radians(ang_max_[i]))
#         #         ang_max[int(t_bus[i]-1)] = math.radians(ang_max_[i])
#         #         ang_min[int(f_bus[i]-1)] = math.radians(ang_min_[i])
#         #         ang_min[int(t_bus[i]-1)] = math.radians(ang_min_[i])
#         ang_max = angle_assign(ang_max, int(f_bus[i] - 1),
#                                math.radians(ang_max_[i]))
#         ang_max = angle_assign(ang_max, int(t_bus[i] - 1),
#                                math.radians(ang_max_[i]))
#         ang_min = angle_assign(ang_min, int(f_bus[i] - 1),
#                                math.radians(ang_min_[i]))
#         ang_min = angle_assign(ang_min, int(t_bus[i] - 1),
#                                math.radians(ang_min_[i]))

#     # calculate f; f = X_inv * A * angle
#     print(ang_max - ang_min)
#     print(A)
#     print(np.matmul(A, ang_max - ang_min))
#     ang_mn_max = ang_max - ang_min
#     ang_mn_min = ang_min - ang_max
#     f_max = np.matmul(np.matmul(np.linalg.inv(X), A), ang_mn_max)
#     f_min = np.matmul(np.matmul(np.linalg.inv(X), A), ang_mn_min)

#     f_range = np.hstack((f_min, f_max))

#     assert (line_m, 1 * 2) == f_range.shape
#     return f_range


def get_gen_constraints(opf_data):
    """
    get all generation constraints
        - [p_min, p_max]
    -> gen constraints num = gen_num
    """
    gen_constraints = {}

    gen_k = opf_data['gen'].shape[0]
    for i in range(gen_k):
        p_min = opf_data['gen']['Pmin'][i]
        p_max = opf_data['gen']['Pmax'][i]
        gen_constraints[i] = (p_min, p_max, 'gen')

    return gen_constraints


def get_flow_constraints(opf_data):
    """
    get all flow constraints
        - [f_min, f_max]
    -> gen constraints num = line_m
    """
    flow_constraints = {}

    line_m = opf_data['branch'].shape[0]
    for i in range(line_m):
        ang_max = opf_data['branch']['angmax'][i]
        ang_min = opf_data['branch']['angmin'][i]
        x = opf_data['branch']['x'][i]

        f_min = math.radians(ang_min - ang_max) / x * 10
        f_max = math.radians(ang_max - ang_min) / x * 10
        flow_constraints[i] = (f_min, f_max, 'flow')

    return flow_constraints


# def get_constraints(opf_data):
#     """
#     get all constraints of the given system
#     """
#     gen_constraints = get_gen_constraints(opf_data)
#     flow_constraints = get_flow_constraints(opf_data)

#     constraints = {}
#     for i in range(len(gen_constraints)):
#         constraints[i] = gen_constraints[i]
#     for i in range(len(flow_constraints)):
#         constraints[i + len(gen_constraints)] = flow_constraints[i]

#     return constraints