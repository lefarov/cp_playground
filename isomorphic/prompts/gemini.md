## Debbuging
I have an upcoming ML debugging interview with DeepMind. Can you generate some sample questions for me to practice? The questions should be in Jax, but the bug should not be related to jax syntax/implementation, rather to general ML knowledge. One example of such bug could be missing LayerNorm after each FF layer in a simple transformer architecture. The questions should probably be focused around transformers/gnn/sequence modeling, etc. As the team I'm interviewing for is working on protein folding. Now, please generate first question. Please don't tell me the bugs are and don't indicate potential bug areas as comments in the code. You can introduce multiple bugs per example

Types of bugs we already considered in the previous chats:
- missing masking when computing loss
- missing positional encoding
- missing layer normalizaation for transformers
- relu activation on the last layer for MSE loss
- incorrect gradient accoumulation
- missing normalization for message aggregation in GNN


## ML scenario
I have an upcoming ML scenario interview with DeepMind. Here's the description of the interview that I got:

"Aimed to evaluate yourunderstanding and experience with various machine learning (ML) model types and their applications. During this interview, a research scenario will be provided. You are not expected to have prior knowledge of the specific domain of the scenario."

Even though they mention that that I shouldn't have prior domain knoweldge, based on my previous experience I suspect that the question will be related to Bioinformatics/computational chemistry, maybe something in direction of sequence modeling for RNAs, or something like that.

Can you play a role of my interviewer, generate a sample problem and work with me over it. It would be nice if you can come up with the problem that allow for progressive difficulty. Such that when I provide an initial answer/design, you could complicate it and I would need to rethink my approach.