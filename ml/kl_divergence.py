import numpy as np


def kl_divergence_normal(mu_p, sigma_p, mu_q, sigma_q):
    num = sigma_p**2 + (mu_p - mu_q) ** 2
    denom = 2 * sigma_q**2

    return np.log(sigma_q / sigma_p) + num / denom - 0.5


if __name__ == "__main__":
    print(kl_divergence_normal(-0.2, 0.4, 1.0, 3.0))