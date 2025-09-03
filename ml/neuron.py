from typing import Tuple, List

import math
import numpy as np

def single_neuron_model(
    features: list[list[float]],
    labels: list[int],
    weights: list[float],
    bias: float
) -> Tuple[List[float], float]:
    
    mse = 0
    probs = [0.0] * len(features)
    for i, feature_row in enumerate(features):
        pred = sum(feature * weights[j] for j, feature in enumerate(feature_row)) + bias 
        probs[i] = (1 + math.exp(-pred)) ** -1
        mse += (labels[i] - probs[i]) ** 2
    

    return probs, mse / len(labels)


def train_neuron(
    features: np.ndarray,
	labels: np.ndarray,
	initial_weights: np.ndarray,
	initial_bias: float,
	learning_rate: float,
	epochs: int
) -> Tuple[np.ndarray, float, list[float]]:
	
    # W: [D_in, D_out]
    weights = initial_weights[..., np.newaxis]
    bias = initial_bias
    labels = labels[..., np.newaxis]
    num_samples = labels.shape[0]

    losses = []

    for _ in range(epochs):
        pred = features @ weights + bias
        act = (1 + np.exp(-pred)) ** -1

        err = (labels - act)
        loss = (err ** 2).sum() / num_samples
        losses.append(loss)
        
        act_db = act * (1 - act)
        act_dW = act_db * features
        
        loss_db = -2 * err * act_db
        loss_dW = -2 * err * act_dW

        loss_db = loss_db.sum() / num_samples
        loss_dW = loss_dW.sum(axis=0) / num_samples

        bias -= learning_rate * loss_db
        weights -= learning_rate * loss_dW[..., np.newaxis]


	# Your code here
    return weights, bias, losses


if __name__ == "__main__":
    features = np.array([
        [1.0, 2.0],
        [2.0, 1.0],
        [-1.0, -2.0]
    ])
    
    labels = np.array([1, 0, 0])
    initial_weights = np.array([0.1, -0.2])
    initial_bias = 0.0
    learning_rate = 0.1
    epochs = 2

    updated_weights, updated_bias, mse_values = train_neuron(
        features,
        labels,
        initial_weights,
        initial_bias,
        learning_rate,
        epochs,
    )