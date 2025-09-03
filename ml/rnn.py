import numpy as np


def rnn_forward(
    input_sequence: list[list[float]],
    initial_hidden_state: list[float],
    Wx: list[list[float]],
    Wh: list[list[float]],
    b: list[float],
) -> list[float]:

    # x: [3, 1]
    # Wx: [1, 1]

    h = np.array(initial_hidden_state)
    x = np.array(input_sequence)
    Wx = np.array(Wx)
    Wh = np.array(Wh)
    for t in range(x.shape[0]):
        xt = x[t, :]
        h = np.tanh(xt @ Wx.T + h @ Wh.T + b)

    # Your code here
    return h


if __name__ == "__main__":
    print(rnn_forward(
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        [0.0, 0.0],
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
        [[0.7, 0.8], [0.9, 1.0]],
        [0.1, 0.2],
    )
    )
