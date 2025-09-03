import jax
import jax.numpy as jnp
import flax.linen as nn
import optax # Typically used for loss functions like cross_entropy
from typing import Optional

class Encoder(nn.Module):
    """A simple GRU Encoder."""
    hidden_dim: int
    vocab_size: int
    embedding_dim: int

    @nn.compact
    def __call__(self, inputs: jnp.ndarray, lengths: jnp.ndarray):
        """
        Args:
            inputs: Batch of input token sequences, shape (batch_size, seq_length).
            lengths: Actual lengths of sequences before padding, shape (batch_size,).

        Returns:
            final_hidden_state: Encoder hidden state after processing sequence,
                                shape (batch_size, hidden_dim).
        """
        embed = nn.Embed(num_embeddings=self.vocab_size, features=self.embedding_dim)
        embedded_inputs = embed(inputs)
        # embedded_inputs shape: (batch_size, seq_length, embedding_dim)

        gru_cell = nn.GRUCell(features=self.hidden_dim)
        initial_state = gru_cell.initialize_carry(jax.random.PRNGKey(0), (inputs.shape[0],))

        scan_gru = nn.scan(
            gru_cell,
            variable_broadcast="params",
            split_rngs={"params": False},
            in_axes=1, # Scan over seq_length
            out_axes=1
        )
        # Note: A real implementation might use masking or pack_padded_sequence
        # Here we simplify and rely on the fact that GRU state evolves.
        # We are primarily interested in the final state.
        final_state, _ = scan_gru(initial_state, embedded_inputs, length=lengths)
        # final_state shape: (batch_size, hidden_dim)

        return final_state

class Decoder(nn.Module):
    """A simple GRU Decoder (Teacher Forcing)."""
    hidden_dim: int
    output_vocab_size: int
    embedding_dim: int

    @nn.compact
    def __call__(self, encoder_state: jnp.ndarray, targets: jnp.ndarray, train: bool = True):
        """
        Args:
            encoder_state: Final hidden state from the encoder, shape (batch_size, hidden_dim).
            targets: Batch of target token sequences (shifted right),
                     shape (batch_size, target_seq_length).
            train: Boolean indicating training mode.

        Returns:
            decoder_outputs: Logits for each position in the target sequence,
                             shape (batch_size, target_seq_length, output_vocab_size).
        """
        # Use encoder state to initialize decoder state
        decoder_initial_state = encoder_state

        # Embed the target tokens (teacher forcing)
        embed = nn.Embed(num_embeddings=self.output_vocab_size, features=self.embedding_dim)
        embedded_targets = embed(targets)
        # embedded_targets shape: (batch_size, target_seq_length, embedding_dim)

        # GRU cell for decoder
        gru_cell = nn.GRUCell(features=self.hidden_dim)

        scan_gru = nn.scan(
            gru_cell,
            variable_broadcast="params",
            split_rngs={"params": False},
            in_axes=1, # Scan over target_seq_length
            out_axes=1
        )

        _, hidden_states = scan_gru(decoder_initial_state, embedded_targets)
        # hidden_states shape: (batch_size, target_seq_length, hidden_dim)

        # Dense layer to map GRU hidden states to output vocab logits
        output_dense = nn.Dense(features=self.output_vocab_size, name="decoder_output_dense")

        # Apply dense layer to all time steps' hidden states
        # Use jax.vmap to apply the dense layer efficiently across the sequence length
        decoder_outputs = jax.vmap(output_dense)(hidden_states)
        # decoder_outputs shape: (batch_size, target_seq_length, output_vocab_size)

        return decoder_outputs


class Seq2Seq(nn.Module):
    """Combines Encoder and Decoder."""
    hidden_dim: int
    input_vocab_size: int
    output_vocab_size: int
    embedding_dim: int

    def setup(self):
        self.encoder = Encoder(
            hidden_dim=self.hidden_dim,
            vocab_size=self.input_vocab_size,
            embedding_dim=self.embedding_dim
        )
        self.decoder = Decoder(
            hidden_dim=self.hidden_dim,
            output_vocab_size=self.output_vocab_size,
            embedding_dim=self.embedding_dim
        )

    def __call__(self, encoder_inputs: jnp.ndarray, encoder_lengths: jnp.ndarray,
                 decoder_inputs: jnp.ndarray, train: bool = True):
        """
        Args:
            encoder_inputs: Shape (batch_size, enc_seq_length).
            encoder_lengths: Shape (batch_size,).
            decoder_inputs: Target sequence (shifted right for teacher forcing),
                            shape (batch_size, dec_seq_length).
            train: Training mode flag.

        Returns:
            Output logits: Shape (batch_size, dec_seq_length, output_vocab_size).
        """
        encoder_state = self.encoder(encoder_inputs, encoder_lengths)
        decoder_outputs = self.decoder(encoder_state, decoder_inputs, train=train)
        return decoder_outputs

# --- Conceptual Training Step & Loss Calculation ---

def calculate_loss(logits: jnp.ndarray, targets: jnp.ndarray, target_mask: Optional[jnp.ndarray] = None):
    """
    Calculates the cross-entropy loss for sequence generation.

    Args:
        logits: Output logits from the decoder,
                shape (batch_size, target_seq_length, output_vocab_size).
        targets: Ground truth target sequences (NOT shifted),
                 shape (batch_size, target_seq_length).
        target_mask: Boolean mask indicating valid (non-padded) target tokens.
                     Shape (batch_size, target_seq_length). Value is True for valid tokens.
                     If None, assumes all tokens are valid.

    Returns:
        Average loss per token.
    """
    # Get the number of classes from the logits
    num_classes = logits.shape[-1]

    # One-hot encode the target labels
    target_one_hot = jax.nn.one_hot(targets, num_classes=num_classes)
    # target_one_hot shape: (batch_size, target_seq_length, output_vocab_size)

    # Calculate cross-entropy loss for each token
    # optax.softmax_cross_entropy expects logits
    token_losses = optax.softmax_cross_entropy(logits=logits, labels=target_one_hot)
    # token_losses shape: (batch_size, target_seq_length)

    # *** Problem Area Candidate ***
    # How should the mask be used to calculate the final loss?

    # Sum losses across the sequence and batch
    total_loss = jnp.sum(token_losses)

    # Calculate the number of actual target tokens (ignoring padding)
    # If mask is provided, count True values, otherwise count all tokens
    if target_mask is not None:
        num_actual_tokens = jnp.sum(target_mask)
    else:
        # Assume no padding if mask is missing
        num_actual_tokens = targets.shape[0] * targets.shape[1]

    # Avoid division by zero if there are no actual tokens (e.g., empty batch/mask)
    num_actual_tokens = jnp.maximum(num_actual_tokens, 1.0)

    # Average loss per actual token
    mean_loss = total_loss / num_actual_tokens

    return mean_loss


if __name__ == "__main__":

    # --- Example Usage ---
    # Assume some dummy data
    batch_size = 4
    enc_seq_length = 12
    dec_seq_length = 15
    input_vocab_size = 100
    output_vocab_size = 120
    embedding_dim = 32
    hidden_dim = 64
    PAD_ID = 0 # Assuming 0 is the padding token ID

    key = jax.random.PRNGKey(2)
    key_enc, key_dec, key_model, key_len = jax.random.split(key, 4)

    # Dummy input sequences (padded)
    dummy_enc_inputs = jax.random.randint(key_enc, (batch_size, enc_seq_length), 1, input_vocab_size)
    # Dummy target sequences (padded) - represent the ground truth
    dummy_targets = jax.random.randint(key_dec, (batch_size, dec_seq_length), 1, output_vocab_size)

    # Create sequence lengths (example)
    dummy_enc_lengths = jnp.array([10, 8, 12, 9])
    dummy_dec_lengths = jnp.array([13, 15, 11, 14])

    # Apply padding based on lengths
    dummy_enc_inputs = jnp.where(jnp.arange(enc_seq_length) < dummy_enc_lengths[:, None], dummy_enc_inputs, PAD_ID)
    dummy_targets = jnp.where(jnp.arange(dec_seq_length) < dummy_dec_lengths[:, None], dummy_targets, PAD_ID)

    # Create decoder inputs (teacher forcing: usually BOS + target[:-1])
    # Simplified here: Use targets directly for shape, real implementation differs
    dummy_dec_inputs = dummy_targets # In practice, this should be shifted right with BOS

    # Create target mask (True for non-pad tokens)
    target_mask = (dummy_targets != PAD_ID)

    # Initialize model
    model = Seq2Seq(
        hidden_dim=hidden_dim,
        input_vocab_size=input_vocab_size,
        output_vocab_size=output_vocab_size,
        embedding_dim=embedding_dim
    )
    variables = model.init(key_model, dummy_enc_inputs, dummy_enc_lengths, dummy_dec_inputs, train=False)

    # Forward pass
    logits = model.apply(variables, dummy_enc_inputs, dummy_enc_lengths, dummy_dec_inputs, train=False)

    # Calculate loss
    loss = calculate_loss(logits, dummy_targets, target_mask)

    print("Encoder Input Shape:", dummy_enc_inputs.shape)
    print("Decoder Targets Shape:", dummy_targets.shape)
    print("Decoder Output Logits Shape:", logits.shape)
    print("Target Mask Shape:", target_mask.shape)
    print("Calculated Loss:", loss)