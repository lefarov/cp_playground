import numpy as np


def adam_optimizer(
	grad,
	x0,
	learning_rate=0.001,
	beta1=0.9,
	beta2=0.999,
	epsilon=1e-8,
	num_iterations=10
):
	m = np.zeros_like(x0)
	v = np.zeros_like(x0)

	x = x0
	for t in range(0, num_iterations + 1):
		df = grad(x)

		m = beta1 * m + (1 - beta1) * df
		v = beta2 * v + (1 - beta2) * df ** 2

		m_hat = m / (1 - beta1 ** t)
		v_hat = v / (1 - beta2 ** t)

		x = x - learning_rate * m_hat / (v_hat ** 0.5 + epsilon)

	return x


def objective_function(x):
	return x[0]**2 + x[1]**2


def gradient(x):
	return np.array([2*x[0], 2*x[1]])


if __name__ == "__main__":
	x0 = np.array([1.0, 1.0])
	x_opt = adam_optimizer(gradient, x0, num_iterations=1)
	print(x_opt)