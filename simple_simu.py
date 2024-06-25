import math
# Solving simple things for the entire cascade, using only simple parameters
import matplotlib.pyplot as plt
import stage

def check_input(alpha, p, l, np, nl):
    if nl * l < np * p:
        print("Not enough U-235 in the input stream, enrichment goal can't be achieved!")
        return 0
    r0 = nl / (1 - nl)
    rp = np / (1 - np)
    stages = math.log(rp/r0)/math.log(alpha) - 1
    print(f"The final waste of the process is ({l - p}, {round((nl * l - np * p) / (l - p), 4)})")
    return stages


def flow_calcs(alpha, p, np, nl, n_stages):
    # Number of elements is given, find the right flows
    flows = []
    beta = (alpha+1)/(alpha-1)
    factor = beta * p * np
    r0 = nl / (1 - nl)
    for s in range(round(n_stages)+1):
        ls = 1 - alpha**(s-n_stages-1)+(alpha**(-s)-alpha**(-n_stages-1))/r0
        flows.append(factor*ls)

    return flows


def calc_stage(alpha, n_in, p, np):
    flow_s = ((np - n_in) * p) / ((1 - n_in) * n_in)
    beta = (alpha+1)/(alpha-1)
    R0 = n_in/(1-n_in)
    return beta*flow_s, (alpha*R0)/(1+alpha*R0)


def calc_ideal_flows(alpha, np, p, l, nl, **mode):
    """
    Calculations for ideal cascade, with different modes for different questions
    :param alpha: A constant alpha value for all stages
    :param np: The desired final product concentration
    :param p: The desired final product amount (KG)
    :param l: The input flow of material (Kg/Day)
    :param nl: The input material concentration of the desired isotope
    :param mode: TODO: add different modes which differ in the input parameters
    :return: Flows and concentrations through the cascade
    """

    flows, concentrations = [], []
    elements = 1
    n_stages = check_input(alpha, p, l, np, nl)
    if n_stages:
        flows, concentrations = [l], [nl]
        while concentrations[-1] < np:
            elements += 1
            flow_s, n_out = calc_stage(alpha, concentrations[-1], p, np)
            flows.append(flow_s)
            concentrations.append(n_out)

        print(f"The separation process used {elements} stages to reach goal ({p},{np}). Theoretical N_stages: {n_stages}")

    return flows[1:], concentrations[1:]


def main():
    flows, concentrations = calc_ideal_flows(1.5, 0.9, 1, 1000, 1/140)


if __name__ == '__main__':
    main()
