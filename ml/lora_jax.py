import jax
import jax.numpy as jnp
import flax.linen as nn
# Import standard initializers explicitly
from flax.linen.initializers import lecun_normal, normal, zeros

class LoRADense(nn.Module):
    """
    A Dense layer incorporating Low-Rank Adaptation (LoRA).
    """
    features: int            # Output features (dimension d_out)
    lora_rank: int           # Rank 'r' for LoRA decomposition
    lora_alpha: float        # LoRA scaling factor 'alpha'
    use_bias: bool = True    # Whether the dense layer uses a bias
    dtype: jnp.dtype = jnp.float32 # Activation dtype
    param_dtype: jnp.dtype = jnp.float32 # Parameter dtype
    precision: jax.lax.Precision = None # Precision for matrix multiplications

    # --- Initializers ---
    # Define initializers for kernel, bias, and LoRA matrices.
    # Note: In practice, kernel/bias would be loaded from pre-trained and frozen.
    kernel_init: nn.initializers.Initializer = lecun_normal()
    bias_init: nn.initializers.Initializer = zeros
    # LoRA specific initializers based on common practice: Normal/Gaussian for A, Zeros for B
    lora_A_init: nn.initializers.Initializer = normal(stddev=0.02)
    lora_B_init: nn.initializers.Initializer = zeros

    @nn.compact
    def __call__(self, inputs: jnp.ndarray) -> jnp.ndarray:
        """
        Applies a Dense layer transformation with LoRA adaptation.

        Args:
            inputs: Input data, typically shape [..., in_features].

        Returns:
            Output tensor, shape [..., features].

        ∂(xAB) / ∂A = x^T @ B
        ∂(xAB) / dB = (xA)^T
        """
        # Input features inferred from the input tensor's last dimension
        in_features = inputs.shape[-1] # dimension d_in

        # --- YOUR IMPLEMENTATION STARTS HERE ---

        # 1. Define Parameters
        # --- Original Dense Layer Parameters (W and b) ---
        # Treat these as parameters of this layer for the exercise.
        # In real LoRA, these would be frozen external weights.
        kernel = self.param('kernel',                 # Name
                            self.kernel_init,        # Initializer
                            (in_features, self.features), # Shape: [d_in, d_out]
                            self.param_dtype)        # Parameter dtype

        if self.use_bias:
            bias = self.param('bias',
                              self.bias_init,
                              (self.features,),      # Shape: [d_out]
                              self.param_dtype)
        else:
            bias = None

        # --- LoRA Parameters (A and B) ---
        # These are the parameters typically trained during LoRA fine-tuning.
        lora_A = self.param('lora_A',
                            self.lora_A_init,
                            (in_features, self.lora_rank), # Shape: [d_in, r]
                            self.param_dtype)
        lora_B = self.param('lora_B',
                            self.lora_B_init,
                            (self.lora_rank, self.features), # Shape: [r, d_out]
                            self.param_dtype)

        # 2. Implement Forward Pass Calculation
        # Ensure inputs have the correct dtype for calculations
        inputs = inputs.astype(self.dtype)

        # Calculate original Dense output (y = xW + b)
        y = inputs @ kernel
        if bias is not None:
            y = y + bias

        # Calculate LoRA delta (delta = x @ A @ B * scale)
        lora_intermediate = inputs @ lora_A # Shape: [..., r]
        lora_update = lora_intermediate @ lora_B # Shape: [..., d_out]

        # Calculate and apply scaling factor (alpha / r)
        if self.lora_rank > 0:
            scaling = self.lora_alpha / self.lora_rank
            lora_update = lora_update * scaling
        # If rank is 0, lora_update remains 0 (due to B init), so no scaling needed.

        # Add LoRA delta to original output (ensure dtype consistency)
        output = y + lora_update.astype(self.dtype)

        # --- YOUR IMPLEMENTATION ENDS HERE ---

        return output
    

if __name__ == "__main__":
    batch_size = 4
    seq_len = 10
    in_features = 128
    out_features = 256
    lora_rank = 8
    lora_alpha = 16.0 # Common practice: alpha = 2 * rank

    # --- Initialization ---
    key = jax.random.PRNGKey(0)
    dummy_input = jnp.ones((batch_size, seq_len, in_features))

    # Instantiate the layer
    lora_dense_layer = LoRADense(
        features=out_features,
        lora_rank=lora_rank,
        lora_alpha=lora_alpha
    )

    # Initialize parameters
    variables = lora_dense_layer.init(key, dummy_input) # Contains 'params' dictionary
    params = variables['params']

    print("Parameter Shapes:")
    print(jax.tree_util.tree_map(lambda x: x.shape, params))
    # Expected keys: 'kernel', 'bias', 'lora_A', 'lora_B' with correct shapes

    # --- Forward Pass ---
    # Create actual input
    input_tensor = jax.random.normal(jax.random.PRNGKey(1), (batch_size, seq_len, in_features))

    # Apply the layer
    output_tensor = lora_dense_layer.apply(variables, input_tensor)

    # Check output shape
    print("\nInput shape:", input_tensor.shape)
    print("Output shape:", output_tensor.shape)
    # Expected Output shape: (4, 10, 256)

    # Note on Training: In a real fine-tuning scenario, an optimizer (like Optax)
    # would be configured to only update params['lora_A'] and params['lora_B'],
    # keeping params['kernel'] and params['bias'] frozen.