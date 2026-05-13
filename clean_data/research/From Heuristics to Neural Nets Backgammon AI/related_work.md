# Backgammon AI — Related Work

## Neurogammon (Tesauro, 1990)

Neurogammon pioneered supervised neural-network approaches for Backgammon. The architecture:
- **Six distinct feedforward networks**, each responsible for different phases of play
- Trained via **backpropagation on large expert game databases**
- Used a "comparison" training paradigm — networks learned to compare and rank final board states

**Result**: Neurogammon 1.0 secured a flawless **5-0 victory** at the First Computer Olympiad in 1989, demonstrating the power of learned positional evaluation over handcrafted heuristics.

**Limitation**: Reliance on phase-specific networks and expert-labeled data yields a complex ensemble that's cumbersome to train and maintain. You need expert game databases, separate networks per phase, and elaborate stitching logic.

## TD-Gammon (Tesauro, 1995)

TD-Gammon advanced the field dramatically by introducing a **single multilayer perceptron trained entirely by temporal-difference learning (TD(λ)) through self-play**. No expert games needed. No phase-specific networks. Just one MLP and self-play.

The architecture:
- **Single MLP** with raw board encoding as input
- Trained with **TD(λ)** — eligibility traces enabling multi-step credit assignment
- **Pure self-play** — the network plays itself thousands of times, learning from its own outcomes

**Results**: Starting from random initialization, the network autonomously discovered elementary strategies (hitting, blocking, building primes). When augmented with Neurogammon's handcrafted features, it achieved **master-level performance** against human grandmasters — within a few hundredths of a point per game.

This was a landmark result. It showed that pure RL with self-play and function approximation could rival expert humans in a complex stochastic game. TD-Gammon influenced the entire trajectory of RL research for the next two decades.

**Limitation**: The original TD-Gammon papers omit critical hyperparameter settings:
- λ decay schedule
- Learning rate
- State representation specifics

Reproducing TD-Gammon from scratch requires extensive experimentation to recover those choices. Direct replication is hard.

## How My Work Extends the Foundation

I built on these foundations by implementing and training a **TD(0) agent** using a similar MLP architecture. The state representation is fed into the network, which outputs an approximate value function `V(s; θ)` for move selection.

In parallel, I trained a **Monte Carlo (MC) agent** under the same architecture and hyperparameter schedule. This lets me cleanly compare TD(0), TD(λ), and MC on identical footing.

In exhaustive head-to-head evaluations:
- Both TD(0) and MC surpassed all heuristic baselines
- TD(λ) outperformed both TD(0) and MC
- All deep-learning agents validated the effectiveness of function approximation for Backgammon

**The contribution**: by independently tuning the hyperparameters, my agents achieved win rates comparable to those reported in TD-Gammon — validating the robustness of deep function approximation for Backgammon value estimation and demonstrating the ability to model the game's stochastic dynamics.

## What's Different in My Approach

A few intentional design choices:

- **Unified network architecture** across TD(0), TD(λ), and MC — same hyperparameters, same network depth, same input encoding. This isolates the **algorithmic** contribution rather than confounding it with architectural differences.
- **Smaller network** (single hidden layer of 80 units, 4 output units) — TD-Gammon used larger networks but I wanted to demonstrate that simpler architectures suffice.
- **Round-robin evaluation** of 1000 games per pairing — robust statistical comparison rather than single-match evaluation.
- **Multiple training durations** (4000, 10000, 35000 episodes) — explicit study of how more data affects each algorithm.

## What I Did Not Pursue

A few directions that were out of scope due to time constraints:

- **Deep Q-Networks (DQN)** and variants (Double DQN, Dueling DQN) — value-of-action rather than value-of-state
- **Convolutional or attention-based architectures** — modern RL backbones that might further accelerate learning
- **Full minimax tournament** — the 2-ply minimax was too slow (~20 min/game) for 1000-game round-robin

These are flagged in the future work section as natural extensions.

## Why TD(λ) Was Likely to Win

Going in, my hypothesis was that **TD(λ) would beat both TD(0) and MC** because:
- TD(0) suffers from high bias (1-step bootstrapping is myopic)
- MC suffers from high variance (full-episode returns include all the noise of an entire game)
- TD(λ) interpolates between the two via the eligibility trace λ — it's the bias-variance tradeoff baked into the algorithm

The empirical results confirmed this hypothesis. TD(λ) topped the round-robin among the three RL methods.

## Keywords

related work, Neurogammon, TD-Gammon, Tesauro, Backgammon AI history, IJCNN, Computer Olympiad, supervised neural network, temporal difference learning, TD(lambda), self-play, function approximation, MLP, master level performance, Backgammon hyperparameters, deep RL agents, value approximation
