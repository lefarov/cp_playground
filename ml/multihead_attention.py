from typing import Tuple

import numpy as np


# reference from PyTorch: https://discuss.pytorch.org/t/which-multihead-attention-implementation-is-correct/198996/2


def softmax(X, axis=-1):
    _max = np.max(X, axis=axis, keepdims=True)
    _exp = np.exp(X - _max)
    _sum = np.sum(_exp, axis=axis, keepdims=True)

    return _exp / _sum

def compute_qkv(X, W_q, W_k, W_v):
	return X @ W_q, X @ W_k, X @ W_v

def self_attention(Q, K, V):
    # Q, K, V: [N, E]
    # A = Q @ K.T: [N, N]
    # A @ V: [N, E]
    A = softmax(Q @ K.T / np.sqrt(K.shape[1]))
    return A @ V

def multi_head_attention(Q, K, V, n_heads):
    n_tokens = Q.shape[0]
    head_dim = Q.shape[-1] // n_heads

    Q = Q.reshape(-1, n_heads, head_dim).transpose(1, 0, 2)
    K = K.reshape(-1, n_heads, head_dim).transpose(1, 0, 2)
    V = V.reshape(-1, n_heads, head_dim).transpose(1, 0, 2)

    # Q, K, V: [H, N, E]
    # K.T: [H, E, N]
    # A: [H, N, N]
    A = softmax(Q @ K.transpose(0, 2, 1) / np.sqrt(head_dim))

    # reshaping
    # A @ V: [H, N, N] @ H[H, N, E] -> [H, N, E]
    return (A @ V).transpose(1, 0, 2).reshape(n_tokens, -1)


def compute_qkv_sol(
    X: np.ndarray,
    W_q: np.ndarray,
    W_k: np.ndarray,
    W_v: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute the Query (Q), Key (K), and Value (V) matrices.
    
    Args:
    X: numpy array of shape (seq_len, d_model), input sequence
    W_q, W_k, W_v: numpy arrays of shape (d_model, d_model), weight matrices for Q, K, and V
    
    Returns:
    Q, K, V: numpy arrays of shape (seq_len, d_model)
    """
    Q = np.dot(X, W_q)  # Compute the Query matrix Q
    K = np.dot(X, W_k)  # Compute the Key matrix K
    V = np.dot(X, W_v)  # Compute the Value matrix V
    return Q, K, V

def self_attention_sol(Q: np.ndarray, K: np.ndarray, V: np.ndarray) -> np.ndarray:
    """
    Compute self-attention for a single head.
    
    Args:
    Q: numpy array of shape (seq_len, d_k), Query matrix
    K: numpy array of shape (seq_len, d_k), Key matrix
    V: numpy array of shape (seq_len, d_k), Value matrix
    
    Returns:
    attention_output: numpy array of shape (seq_len, d_k), output of the self-attention mechanism
    """
    d_k = Q.shape[1]  # Get the dimension of the keys
    scores = np.matmul(Q, K.T) / np.sqrt(d_k)  # Compute scaled dot-product attention scores
    score_max = np.max(scores, axis=1, keepdims=True)  # Find the maximum score for numerical stability
    attention_weights = np.exp(scores - score_max) / np.sum(np.exp(scores - score_max), axis=1, keepdims=True)  # Compute softmax to get attention weights
    attention_output = np.matmul(attention_weights, V)  # Compute the final attention output
    return attention_output

def multi_head_attention_sol(Q: np.ndarray, K: np.ndarray, V: np.ndarray, n_heads: int) -> np.ndarray:
    """
    Compute multi-head attention.
    
    Args:
    Q, K, V: numpy arrays of shape (seq_len, d_model), Query, Key, and Value matrices
    n_heads: int, number of attention heads
    
    Returns:
    attention_output: numpy array of shape (seq_len, d_model), final attention output
    """
    d_model = Q.shape[1]  # Get the model dimension
    assert d_model % n_heads == 0  # Ensure d_model is divisible by n_heads
    d_k = d_model // n_heads  # Dimension for each head

    # Reshape Q, K, V to separate heads
    Q_reshaped = Q.reshape(Q.shape[0], n_heads, d_k).transpose(1, 0, 2)  # Reshape and transpose to (n_heads, seq_len, d_k)
    K_reshaped = K.reshape(K.shape[0], n_heads, d_k).transpose(1, 0, 2)  # Reshape and transpose to (n_heads, seq_len, d_k)
    V_reshaped = V.reshape(V.shape[0], n_heads, d_k).transpose(1, 0, 2)  # Reshape and transpose to (n_heads, seq_len, d_k)

    # Compute attention scores for each head
    attentions = []  # Store attention outputs for each head

    for i in range(n_heads):
        attn = self_attention(Q_reshaped[i], K_reshaped[i], V_reshaped[i])  # Compute attention for the i-th head
        attentions.append(attn)  # Collect attention output

    # Concatenate all head outputs
    attention_output = np.concatenate(attentions, axis=-1)  # Concatenate along the last axis (columns)
    return attention_output  # Return the final attention output


if __name__ == "__main__":
    m, n = 6, 8
    n_heads = 4
    np.random.seed(42)
    X = np.arange(m*n).reshape(m,n)
    X = np.random.permutation(X.flatten()).reshape(m, n)
    
    W_q = np.random.randint(0,4,size=(n, n))  # out dim of attention is 2
    W_k = np.random.randint(0,5,size=(n, n))
    W_v = np.random.randint(0,6,size=(n, n))

    Q, K, V = compute_qkv(X, W_q, W_k, W_v)
    A = multi_head_attention(Q, K, V, n_heads)
    print(A)