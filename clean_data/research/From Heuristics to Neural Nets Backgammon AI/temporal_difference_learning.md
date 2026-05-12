# Temporal-Difference Learning (TD(0) and TD(λ))

## What TD Methods Do

Temporal-difference (TD) methods are a class of model-free reinforcement-learning algorithms that learn value estimates by **bootstrapping** — updating predictions based partly on other learned predictions, rather than waiting for final outcomes.

This is the key trick that distinguishes TD from Monte Carlo: TD doesn't need to wait until the end of an episode to update. It updates after every single step, using its own current value estimate of the next state as a target.

## The Value Network Architecture

To leverage function approximation's generalization capacity, I parameterize V(s) with a **multilayer perceptron**.

### Input Encoding
Each board state is encoded as a **28-dimensional input vector**:
- Each entry corresponds to a point on the Backgammon board
- The signed checker count: positive for White, negative for Black
- Normalized by dividing by 15 (the maximum checkers per point)

This compact representation is enough for the network to learn meaningful value estimates.

### Network Topology
- **Input layer**: 28 units (board state)
- **Hidden layer**: single hidden layer of **80 units**
- **Output layer**: 4 units, all sigmoid activation

### Output Interpretation
The output is a 4-dimensional vector:
`[pW_reg, pW_gammon, pB_reg, pB_gammon]`

Where:
- `pW_reg` — probability of regular White win
- `pW_gammon` — probability of White gammon (White bears off all checkers, Black bears off none)
- `pB_reg` — probability of regular Black win
- `pB_gammon` — probability of Black gammon

All outputs lie in [0, 1] via sigmoid normalization. This dual-class encoding (regular vs. gammon) lets the network distinguish ordinary wins from doubled-stakes wins, which matters for value estimation.

### Terminal Encoding
Terminal outcomes are encoded as **one-hot vectors**:
- Regular White win: `[1, 0, 0, 0]`
- White gammon: `[0, 1, 0, 0]`
- Regular Black win: `[0, 0, 1, 0]`
- Black gammon: `[0, 0, 0, 1]`

These vectors serve as the target `r_{t+1}` at the terminal state.

## TD(0) Implementation

### The Update Rule
At every step, the value network is updated via **one-step temporal-difference bootstrapping**.

For each transition `(s_t, r_{t+1}, s_{t+1})`:
1. Forward `s_t` and `s_{t+1}` through the network to get `V(s_t)` and `V(s_{t+1})`
2. Set `r_{t+1} = 0` for nonterminal moves; use the one-hot terminal vector at game end
3. Compute the TD error:
   `δ_t = r_{t+1} + γ V(s_{t+1}) − V(s_t)`
4. Update weights:
   `θ ← θ + α · δ_t · ∇_θ V(s_t; θ)`

### Hyperparameters
- Learning rate `α = 0.001`
- Discount factor `γ = 0.99`
- ε-greedy policy: `ε = 0.1` initially, reduced to `ε = 0.01` at episode 4000

Because TD(0) doesn't use eligibility traces, each weight update depends solely on the most recent transition. The error signal only propagates one step backward.

### What TD(0) Trains
Iterating this process over thousands of self-play episodes drives the network toward accurate value predictions across the Backgammon state space. The network learns by playing itself — there's no external teacher.

## TD(λ) Implementation

### The Idea
TD(λ) extends TD(0) by incorporating **eligibility traces** to distribute credit across multiple preceding states. Instead of only updating the most recent state, TD(λ) updates earlier states too — in proportion to their recent influence.

### The Update Rule
Compute the same TD error as TD(0):
`δ_t = r_{t+1} + γ V(s_{t+1}) − V(s_t)`

But use an accumulating eligibility trace `e_t`:
`e_t = γλ · e_{t-1} + ∇_θ V(s_t; θ)`

Where `λ ∈ [0, 1]` is the trace-decay parameter.

The weight update becomes:
`θ ← θ + α · δ_t · e_t`

### Hyperparameters
- Same `α = 0.001` and `γ = 0.99` as TD(0)
- `λ = 0.8` — chosen to balance bias and variance in trace accumulation
- Same ε-greedy schedule

### Why Eligibility Traces Help
Eligibility traces enable **multi-step credit assignment**, allowing a single TD error to adjust:
- The current state's estimate (as in TD(0))
- AND earlier states in the trajectory, in proportion to their recent influence

This mechanism:
- **Accelerates learning** because gradient signal reaches earlier states faster
- **Reduces variance** compared to MC (still bootstraps somewhat)
- **Reduces bias** compared to TD(0) (uses more than 1-step information)

It's the bias-variance tradeoff baked into the algorithm. λ = 0 reduces to TD(0) (high bias, low variance). λ = 1 approximates Monte Carlo (low bias, high variance). λ = 0.8 sits in the sweet spot — biased enough to be stable, unbiased enough to learn quickly.

## Why This Worked

The combination of:
- A small but capable MLP (80 hidden units)
- Self-play training over 35,000 episodes
- TD(λ) with carefully tuned hyperparameters

was enough to produce an agent that beat both TD(0) and Monte Carlo learners head-to-head. This validates Tesauro's original TD-Gammon insight: **temporal-difference learning with function approximation is a powerful combination for stochastic board games**.

## Implementation Notes

A few things that mattered in practice:
- **Sigmoid output activation** is important because the network is predicting probabilities (must be in [0, 1])
- **Normalizing the input** by dividing by 15 keeps the input space bounded and helps gradient flow
- **One-hot terminal encoding** with separate regular/gammon outputs is a Tesauro-style trick that helps the network handle the doubled-stakes case
- **ε decay at episode 4000** balances early exploration with later exploitation

## Keywords

temporal difference learning, TD(0), TD(lambda), eligibility traces, value network, MLP, multilayer perceptron, board encoding, sigmoid activation, one-hot terminal, gammon, regular win, learning rate, discount factor, epsilon-greedy, self-play, bootstrapping, model-free RL, function approximation, Tesauro
