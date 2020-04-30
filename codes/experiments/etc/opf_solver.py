import cvxpy as cp
import numpy as np
from dc_opf_preprocess import *


def select_active_constraints(p, gen_constraints, f, flow_constraints=None):
    """
    select active constraints
    """
    active_constraints = {'gen': [], 'flow': []}
    if gen_constraints is not None:
        active_constraints['gen_num'] = len(gen_constraints)
        for idx in gen_constraints.keys():
            low_bound = p.value[idx] <= gen_constraints[idx][0]
            upper_bound = gen_constraints[idx][1] <= p.value[idx]
            if low_bound or upper_bound:
                active_constraints['gen'].append(idx)
    else:
        active_constraints['gen_num'] = len(gen_constraints)
    if flow_constraints is not None:
        active_constraints['flow_num'] = len(flow_constraints)
        for idx in flow_constraints.keys():
            low_bound = f.value[idx] <= flow_constraints[idx][0]
            upper_bound = flow_constraints[idx][1] <= f.value[idx]
            if low_bound or upper_bound:
                active_constraints['flow'].append(idx)
    else:
        active_constraints['flow_num'] = 0

    if gen_constraints is not None:
        gen_constraint_vec = np.zeros(active_constraints['gen_num'])
        for i in range(active_constraints['gen_num']):
            if i in active_constraints['gen']:
                gen_constraint_vec[i] = 1
    if flow_constraints is not None:
        flow_constraint_vec = np.zeros(active_constraints['flow_num'])
        for i in range(active_constraints['flow_num']):
            if i in active_constraints['flow']:
                flow_constraint_vec[i] = 1
    if gen_constraints is not None:
        active_constraints['idx_vec'] = gen_constraint_vec
    if flow_constraints is not None:
        active_constraints['idx_vec'] = np.hstack(
            active_constraints['idx_vec'], flow_constraint_vec)

    return active_constraints


def DC_OPF_solver(opf_data,
                  gen_constraints,
                  flow_constraints=None,
                  uncertainty_w=None,
                  verbose=False,
                  dual=False):
    # get demand and cost function data from the dataset
    p_dim = opf_data['gen'].shape[0]
    c2 = np.diag(opf_data['gencost']['c2'])
    c1 = np.array(opf_data['gencost']['c1'])
    c0 = np.array(opf_data['gencost']['c0'])

    # set a variable and constants
    w = uncertainty_w
    d = get_d(opf_data)

    H = get_H(opf_data)
    X = get_X(opf_data)
    A_r = get_A_r(opf_data)
    B_r = get_B_r(opf_data, A_r, X)
    PTDF = get_PTDF(opf_data, X, A_r, B_r)

    p = cp.Variable(p_dim, name="p")
    if uncertainty_w is not None:
        f = PTDF @ (H @ p + w - d)
        # @ operator usage: https://www.python.org/dev/peps/pep-0465/
    else:
        f = PTDF @ (H @ p - d)

    # set constraints
    ## power balance
    if uncertainty_w is not None:
        constraints = [sum(p) == sum(d - w)]
    else:
        constraints = [sum(p) == sum(d)]
    ## gen constraints
    if gen_constraints is not None:
        for idx in gen_constraints.keys():
            p_min = gen_constraints[idx][0]
            p_max = gen_constraints[idx][1]
            constraints.append(p_min <= p[idx])
            constraints.append(p[idx] <= p_max)
    ## flow constraints
    if flow_constraints is not None:
        for idx in flow_constraints.keys():
            f_min = flow_constraints[idx][0]
            f_max = flow_constraints[idx][1]
            constraints.append(f_min <= f[idx])
            constraints.append(f[idx] <= f_max)

    # set the objective function
    Objective = cp.quad_form(p, c2) + c1.T @ p + sum(c0)

    # solve the problem
    problem = cp.Problem(cp.Minimize(Objective), constraints)
    problem.solve()

    # print result
    if problem.status not in ["infeasible", "unbounded"]:
        if verbose:
            print("Optimal value: %s" % problem.value)
        # select active constriants
        active_constraints = select_active_constraints(
            p=p,
            gen_constraints=gen_constraints,
            f=f,
            flow_constraints=flow_constraints)
    else:
        if verbose:
            print("The problem is infeasible or unbounded")
        active_constraints = None
    for variable in problem.variables():
        if verbose:
            print("Variable %s: value %s" % (variable.name(), variable.value))
    if dual:
        if verbose:
            print("A dual solution corresponding to the inequality constraints is")
            print(problem.constraints[0].dual_value)

    return active_constraints
