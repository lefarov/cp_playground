import jax
import jax.numpy as jnp
from jax import random

# --- Helper Functions ---
def sigmoid(x):
  """Numerically stable sigmoid function."""
  # Using jax.nn.sigmoid directly is also fine for most cases
  return 0.5 * (jnp.tanh(x / 2.0) + 1)

# --- Loss Functions for a Single Pair ---

def ns_loss_single_pair_fn(center_embedding,
                           context_embedding,
                           label,
                           epsilon=1e-10):
  """
  Calculates the Negative Sampling (NS) loss component for a single
  (center, context) pair based on its label.

  Args:
    center_embedding: Embedding vector for the center word (shape: [embed_dim]).
    context_embedding: Embedding vector for the context word (shape: [embed_dim]).
    label: Binary label (1 if true context, 0 if negative sample).
    epsilon: Small value for numerical stability in logs.

  Returns:
    Scalar loss value for this single pair.
  """
  # Calculate the score (logit) for this pair
  score = jnp.dot(center_embedding, context_embedding)

  # Calculate binary cross-entropy loss based on the label
  # log_loss = -label * log(sigmoid(score)) - (1 - label) * log(1 - sigmoid(score))
  # log_loss = -label * log(sigmoid(score)) - (1 - label) * log(sigmoid(-score))

  # Using jnp.where for clarity or potential slight performance difference
  loss = jnp.where(
      label == 1,
      -jnp.log(sigmoid(score) + epsilon),      # Loss for positive pair
      -jnp.log(sigmoid(-score) + epsilon)     # Loss for negative pair
  )
  # Alternative arithmetic implementation:
  # loss = -(label * jnp.log(sigmoid(score) + epsilon) + \
  #          (1 - label) * jnp.log(sigmoid(-score) + epsilon))

  return loss


def nce_loss_single_pair_fn(center_embedding,
                            context_embedding,
                            label,
                            log_noise_prob_context,
                            num_neg_samples,
                            epsilon=1e-10):
  """
  Calculates the Noise Contrastive Estimation (NCE) loss component for a
  single (center, context) pair based on its label.

  Args:
    center_embedding: Embedding vector for the center word (shape: [embed_dim]).
    context_embedding: Embedding vector for the context word (shape: [embed_dim]).
    label: Binary label (1 if true context, 0 if negative sample).
    log_noise_prob_context: Log probability of sampling the context word from
                              the noise distribution P_noise (scalar).
    num_neg_samples: The number k of negative samples used per positive sample
                     in the overall training setup.
    epsilon: Small value for numerical stability in logs.

  Returns:
    Scalar NCE loss value for this single pair.
  """
  # Calculate the raw score (logit) for this pair
  score = jnp.dot(center_embedding, context_embedding)

  # Calculate the NCE correction term: log(k * P_noise(w)) = log(k) + log(P_noise(w))
  log_k = jnp.log(float(num_neg_samples))
  correction = log_k + log_noise_prob_context

  # Calculate the corrected score used in NCE: s'(c, w) = s(c, w) - correction
  score_corrected = score - correction

  # Calculate binary cross-entropy loss using the *corrected* score
  loss = jnp.where(
      label == 1,
      -jnp.log(sigmoid(score_corrected) + epsilon),      # Loss for positive pair
      -jnp.log(sigmoid(-score_corrected) + epsilon)     # Loss for negative pair
  )
  # Alternative arithmetic implementation:
  # loss = -(label * jnp.log(sigmoid(score_corrected) + epsilon) + \
  #          (1 - label) * jnp.log(sigmoid(-score_corrected) + epsilon))

  return loss

# --- Example Usage ---
key = random.PRNGKey(1)
embed_dim = 10
num_neg_samples_k = 5 # Example value for k

# Dummy Embeddings
key, subkey1, subkey2, subkey3 = random.split(key, 4)
center_emb = random.normal(subkey1, (embed_dim,))
positive_context_emb = random.normal(subkey2, (embed_dim,))
negative_context_emb = random.normal(subkey3, (embed_dim,)) # Just one negative example here

# Dummy Noise Probabilities (Log scale)
log_noise_prob_pos = -jnp.log(1000.0) # Log P_noise for the positive context word
log_noise_prob_neg = -jnp.log(50.0)   # Log P_noise for the negative context word

print("--- Calculating Loss Components for Individual Pairs ---")

# --- NS Example ---
# Loss for the positive pair (label=1)
ns_loss_pos = ns_loss_single_pair_fn(center_emb, positive_context_emb, label=1)
print(f"NS Loss (Positive Pair, Label=1): {ns_loss_pos:.4f}")

# Loss for a negative pair (label=0)
ns_loss_neg = ns_loss_single_pair_fn(center_emb, negative_context_emb, label=0)
print(f"NS Loss (Negative Pair, Label=0): {ns_loss_neg:.4f}")

# In training, total NS loss for one center word = ns_loss_pos + sum(ns_loss_neg_i for i=1..k)

print("\n" + "---" * 10 + "\n")

# --- NCE Example ---
# Loss for the positive pair (label=1)
nce_loss_pos = nce_loss_single_pair_fn(center_emb, positive_context_emb, label=1,
                                       log_noise_prob_context=log_noise_prob_pos,
                                       num_neg_samples=num_neg_samples_k)
print(f"NCE Loss (Positive Pair, Label=1): {nce_loss_pos:.4f}")

# Loss for a negative pair (label=0)
nce_loss_neg = nce_loss_single_pair_fn(center_emb, negative_context_emb, label=0,
                                        log_noise_prob_context=log_noise_prob_neg,
                                        num_neg_samples=num_neg_samples_k)
print(f"NCE Loss (Negative Pair, Label=0): {nce_loss_neg:.4f}")

# In training, total NCE loss for one center word = nce_loss_pos + sum(nce_loss_neg_i for i=1..k)