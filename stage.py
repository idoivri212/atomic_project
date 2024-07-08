import numpy as np


class Stage:
    R = 8.314  # Universal gas constant in J/(mol·K)
    T = 300  # Temperature in K
    delta_m = 0.003  # Mass difference between the isotopes in kg/mol
    uf6_ro = 0

    def __init__(self, alpha, Q, n_centrifuges):
        self.alpha = alpha
        self.Q = Q * n_centrifuges

    def calc_alpha(self, omega, r):
        velocity = omega * r
        self.alpha = np.exp((Stage.delta_m * velocity ** 2) / (2 * Stage.R * Stage.T))

    def calc_theta(self):
        pass

    def calc_Q(self):
        pass

    def advance(self, feed, n_feed):
        """
        Given the input flow into the Stage, return its waste and product
        :param feed:
        :param n_feed:
        :return:
        """
        n_prod = (self.alpha * n_feed) / (1 + n_feed * (self.alpha - 1))  # R'=alpha*R
        n_waste = n_feed / (self.alpha*(1-n_feed) + n_feed)  # R"=R/alpha
        theta = (n_feed-n_waste)/(n_prod-n_waste)

        p = theta * feed
        w = (1-theta)*feed
        return (p, n_prod), (w, n_waste)


