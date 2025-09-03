import math
import jax
import jax.numpy as jnp
import flax.linen as nn
from typing import Tuple

class Expert(nn.Module):
    """
    A simple Feed-Forward Network expert using Flax.
    Input -> Dense -> ReLU -> Dense -> Output
    """
    d_model: int
    d_hidden: int

    @nn.compact
    def __call__(self, x):
        # Simple FFN: Dense -> ReLU -> Dense
        x = nn.Dense(features=self.d_hidden, name="dense1")(x)
        x = nn.relu(x)
        x = nn.Dense(features=self.d_model, name="dense2")(x)
        return x

class MoELayer(nn.Module):
    """
    A Sparse Mixture of Experts layer using Flax.
    """
    d_model: int
    num_experts: int
    top_k: int
    d_hidden: int

    def setup(self):
        # Gating network: Projects input to scores for each expert
        self.gating_network = nn.Dense(features=self.num_experts, use_bias=False, name="gating")

        # List of expert networks
        # Flax handles parameters for Modules stored in lists/tuples automatically
        self.experts = [Expert(d_model=self.d_model, d_hidden=self.d_hidden, name=f"expert_{i}")
                        for i in range(self.num_experts)]

    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:
        """
        Implement the forward pass for the sparse MoE layer using JAX/Flax.

        Args:
            x: Input tensor of shape [batch_size, sequence_length, d_model]

        Returns:
            Output tensor of shape [batch_size, sequence_length, d_model]
        """
        batch_size, sequence_length, d_model = x.shape
        # Reshape input for processing each token independently
        # Shape: [batch_size * sequence_length, d_model]
        x_flat = x.reshape(-1, d_model)
        num_tokens = x_flat.shape[0]

        # --- YOUR IMPLEMENTATION STARTS HERE ---

        # 1. Compute gating logits (scores before softmax)
        # Shape: [num_tokens, num_experts]
        gating_logits = self.gating_network(x_flat)

        # 2. Select top-k experts and get their weights (via softmax)
        # Apply softmax to logits to get probabilities/weights
        gating_weights_all = jax.nn.softmax(gating_logits, axis=-1) # Shape: [num_tokens, num_experts]

        # Find the top-k weights and their corresponding expert indices
        # topk_weights shape: [num_tokens, top_k]
        # topk_indices shape: [num_tokens, top_k]
        # NOTE: jax.lax.top_k returns values first, then indices
        topk_weights, topk_indices = jax.lax.top_k(gating_weights_all, k=self.top_k)

        # 3. Normalize the top-k weights (so they sum to 1 per token)
        # Shape: [num_tokens, top_k]
        norm_topk_weights = topk_weights / jnp.sum(topk_weights, axis=-1, keepdims=True)
        # Add a small epsilon for numerical stability if needed, e.g.:
        # norm_topk_weights = topk_weights / (jnp.sum(topk_weights, axis=-1, keepdims=True) + 1e-8)

        # 4. Compute outputs from selected experts for each token
        # Initialize tensor to store the final output for each token
        final_output_flat = jnp.zeros_like(x_flat) # Shape: [num_tokens, d_model]

        # Create a flat index and token index base to efficiently gather inputs and scatter outputs
        # Shape: [num_tokens * top_k]
        flat_topk_indices = topk_indices.flatten()
        # Shape: [num_tokens * top_k] -> maps each element above to its original token index
        token_indices_flat = jnp.arange(num_tokens).repeat(self.top_k)

        # Iterate through each expert, process the tokens routed to it, and scatter-add the results
        for i in range(self.num_experts):
            # Find which flattened indices correspond to the current expert 'i'
            mask = (flat_topk_indices == i)

            # Get the indices of the tokens that should be routed to expert 'i'
            # These are indices into the original x_flat (num_tokens dimension)
            tokens_for_expert_i = token_indices_flat[mask]

            if tokens_for_expert_i.size > 0:
                # Get the input data for these tokens
                inputs_for_expert_i = x_flat[tokens_for_expert_i] # Shape: [num_tokens_for_i, d_model]

                # Compute the output of expert 'i' for these tokens
                # NOTE: In Flax, calling a Module requires access to its parameters (state)
                # In a real scenario, this call would be part of model.apply({'params': params}, x)
                # For this boilerplate, we assume self.experts[i] can be called directly
                outputs_for_expert_i = self.experts[i](inputs_for_expert_i) # Shape: [num_tokens_for_i, d_model]

                # 5. Combine expert outputs using normalized gating weights (scatter-add)
                # Get the corresponding normalized weights for these token-expert pairs
                # We need the weights corresponding to the elements selected by the mask
                weights_for_expert_i = norm_topk_weights.flatten()[mask] # Shape: [num_tokens_for_i]

                # Weight the outputs
                weighted_outputs = outputs_for_expert_i * weights_for_expert_i[:, None] # Shape: [num_tokens_for_i, d_model]

                # Add these weighted outputs to the final output tensor at the correct token positions
                # Use JAX's functional update `at[].add()`
                final_output_flat = final_output_flat.at[tokens_for_expert_i].add(weighted_outputs)

        # --- YOUR IMPLEMENTATION ENDS HERE ---

        # Reshape the flat output back to the original input shape
        final_output = final_output_flat.reshape(batch_size, sequence_length, d_model)
        return final_output


class MoELayer(nn.Module):
    """
    A Sparse Mixture of Experts layer using Flax,
    implemented with parallel expert execution via nn.vmap.
    Compatible with both .init() and .apply().
    """
    d_model: int
    num_experts: int
    top_k: int
    d_hidden: int
    capacity_factor: float = 1.25 # Factor to determine expert capacity

    def setup(self):
        # Gating network (remains the same)
        self.gating_network = nn.Dense(features=self.num_experts, use_bias=False, name="gating")

        # --- Define the vmapped Expert ---
        # We use nn.vmap to create a module that applies the Expert logic
        # in parallel across the 'num_experts' dimension.
        # Flax handles parameter stacking and RNG splitting automatically.
        VmappedExpert = nn.vmap(
            Expert,                  # The Module class to map over
            variable_axes={'params': 0}, # Stack/map the 'params' PyTree along axis 0
            split_rngs={'params': True}, # Use different RNGs for initializing each expert's params
            in_axes=0,               # Map over axis 0 of the input (expert_input_batched)
            out_axes=0,              # The output will have axis 0 corresponding to experts
            axis_size=self.num_experts # Specify the size of the mapped axis
        )

        # Instantiate the vmapped module wrapper.
        # We pass the static hyperparameters needed by the underlying Expert class.
        # This single instance will manage the parallel execution of all experts.
        # Note: Name assigned here is for the wrapper module itself.
        self.vmapped_experts = VmappedExpert(
            d_model=self.d_model,
            d_hidden=self.d_hidden,
            name="batched_experts" # Name for the vmapped module instance
            # The underlying Expert instances will be named implicitly by Flax/nn.vmap
        )

    # Using @nn.compact for implicit parameter handling
    @nn.compact
    def __call__(self, x: jnp.ndarray) -> jnp.ndarray:
        """
        Parallel MoE forward pass using nn.vmap.
        """
        batch_size, sequence_length, d_model = x.shape
        x_flat = x.reshape(-1, d_model) # Shape: [num_tokens, d_model]
        num_tokens = x_flat.shape[0]
        num_items = num_tokens * self.top_k # Total items to route

        # --- Gating and Top-k Selection (same as before) ---
        gating_logits = self.gating_network(x_flat) # Shape: [num_tokens, num_experts]
        gating_weights_all = jax.nn.softmax(gating_logits, axis=-1)
        topk_weights, topk_indices = jax.lax.top_k(gating_weights_all, k=self.top_k) # [num_tokens, top_k] each
        norm_topk_weights = topk_weights / (jnp.sum(topk_weights, axis=-1, keepdims=True) + 1e-8) # [num_tokens, top_k]

        # --- Parallel Routing Logic (mostly same as before) ---
        capacity = int(math.ceil((num_items / self.num_experts) * self.capacity_factor))

        flat_expert_indices = topk_indices.flatten() # Shape: [num_items]
        flat_token_indices = jnp.arange(num_tokens, dtype=jnp.int32).repeat(self.top_k) # Shape: [num_items]
        flat_norm_topk_weights = norm_topk_weights.flatten() # Shape: [num_items]

        def position_scan(counts_so_far, expert_idx):
            position = counts_so_far[expert_idx]
            new_counts = counts_so_far.at[expert_idx].add(1)
            return new_counts, position
        init_counts = jnp.zeros(self.num_experts, dtype=jnp.int32)
        _, position_in_expert = jax.lax.scan(position_scan, init_counts, flat_expert_indices) # Shape: [num_items]

        valid_mask = position_in_expert < capacity # Shape: [num_items]
        valid_expert_indices = flat_expert_indices[valid_mask]     # [num_valid_items]
        valid_token_indices = flat_token_indices[valid_mask]       # [num_valid_items]
        valid_position_in_expert = position_in_expert[valid_mask]  # [num_valid_items]
        valid_weights = flat_norm_topk_weights[valid_mask]         # [num_valid_items]

        expert_input_batched = jnp.zeros((self.num_experts, capacity, self.d_model), dtype=x.dtype)
        valid_token_inputs = x_flat[valid_token_indices] # Shape: [num_valid_items, d_model]
        expert_input_batched = expert_input_batched.at[valid_expert_indices, valid_position_in_expert].set(valid_token_inputs)

        # --- Apply Experts in Parallel using the nn.vmap wrapper ---
        # Call the vmapped module instance created in setup.
        # Flax handles passing the correctly stacked parameters implicitly.
        expert_output_batched = self.vmapped_experts(expert_input_batched)
        # expert_output_batched shape: [num_experts, capacity, d_model]

        # --- Gather Outputs and Combine (same as before) ---
        outputs_per_valid_item = expert_output_batched[valid_expert_indices, valid_position_in_expert] # Shape: [num_valid_items, d_model]
        weighted_outputs_per_item = outputs_per_valid_item * valid_weights[:, None] # Shape: [num_valid_items, d_model]

        final_output_flat = jnp.zeros_like(x_flat) # Shape: [num_tokens, d_model]
        final_output_flat = final_output_flat.at[valid_token_indices].add(weighted_outputs_per_item)

        # --- Reshape Output ---
        final_output = final_output_flat.reshape(batch_size, sequence_length, d_model)
        return final_output


if __name__ == "__main__":
    # --- Parameters ---
    d_model = 32
    num_experts = 8
    top_k = 2
    d_hidden = d_model * 4
    batch_size = 4
    sequence_length = 10
    capacity_factor = 1.25

    # --- Initialization ---
    key = jax.random.PRNGKey(0)
    dummy_input = jnp.ones((batch_size, sequence_length, d_model), dtype=jnp.float32)

    # Instantiate the MoELayer
    moe_layer = MoELayer(
        d_model=d_model,
        num_experts=num_experts,
        top_k=top_k,
        d_hidden=d_hidden,
        capacity_factor=capacity_factor
    )

    # Initialize parameters - This should now work correctly
    params = moe_layer.init({'params': key}, dummy_input)['params'] # Pass RNG key dict

    print("Parameter Structure (nn.vmap):")
    # Note the structure: params['batched_experts']['Expert_0']['dense1']['kernel'] will have shape [num_experts, d_model, d_hidden]
    print(jax.tree_util.tree_map(lambda x: x.shape, params))

    # --- Forward Pass ---
    # Create actual input
    input_tensor = jax.random.normal(jax.random.PRNGKey(1), (batch_size, sequence_length, d_model))

    # Apply the layer with the initialized parameters
    output_tensor = moe_layer.apply({'params': params}, input_tensor)

    # Check output shape
    print("\nInput shape:", input_tensor.shape)
    print("Output shape:", output_tensor.shape)
    # Expected Output shape: (4, 10, 32) (or whatever dimensions used)