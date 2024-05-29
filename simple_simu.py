# Solving simple things for the entire cascade, using only simple parameters
import matplotlib.pyplot as plt


def find_waste(p, l, np, nl):
    return l - p, (nl*l-np*p)/(l-p)


def calc_stage(alpha, n_in, p, np):
    flow_s = ((np - n_in) * p) / ((1 - n_in) * n_in)
    R0 = n_in/(1-n_in)
    return flow_s, (alpha*R0)/(1+alpha*R0)


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
    flows, concentrations = [l], [nl]
    beta = (alpha+1)/(alpha-1)
    elements = 0
    while concentrations[-1] < np:
        elements += 1
        flow_s, n_out = calc_stage(alpha, concentrations[-1], p, np)
        flows.append(beta*flow_s)
        concentrations.append(n_out)

    print(f"The separation process used {elements} stages to reach goal ({p},{np})")
    w, nw = find_waste(p, l, np, nl)
    print(f"The final waste of the process is ({w}, {round(nw, 4)})")

    return flows, concentrations


def main():
    flows, concentrations = calc_ideal_flows(1.5, 0.9, 1, 1000, 1/140)
    stages = list(range(1, len(flows) + 1))

    # Plot the flow per stage
    plt.figure(figsize=(10, 6))
    plt.plot(stages, flows, marker='o', linestyle='-', color='b')
    plt.xlabel('Stage')
    plt.ylabel('Flow')
    plt.title('Flow(stage)')
    plt.grid(True)
    plt.show()

    # Plot the concentration per stage
    plt.figure(figsize=(10, 6))
    plt.plot(stages, concentrations, marker='o', linestyle='-', color='r')
    plt.xlabel('Stage')
    plt.ylabel('Concentration')
    plt.title('N(stage)')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
