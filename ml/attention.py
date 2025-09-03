import numpy as np

def softmax(X, axis=-1):
    exp = np.exp(X)
    _sum = exp.sum(axis=axis)

    return exp / _sum[..., np.newaxis]

def compute_qkv(X, W_q, W_k, W_v):

	return X @ W_q, X @ W_k, X @ W_v

def self_attention(Q, K, V):
    
    A = softmax(Q @ K.T / np.sqrt(K.shape[1]))

    return A @ V


if __name__ == "__main__":
    X = np.array([[1, 0], [0, 1]])

    W_q = np.array([[1, 0], [0, 1]])
    W_k = np.array([[1, 0], [0, 1]])
    W_v = np.array([[1, 2], [3, 4]])
    Q, K, V = compute_qkv(X, W_q, W_k, W_v)
    output = self_attention(Q, K, V)
    print(output)

    # Expected Output [[1.660477, 2.660477], [2.339523, 3.339523]]