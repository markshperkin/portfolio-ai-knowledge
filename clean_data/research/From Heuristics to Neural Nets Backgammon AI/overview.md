# Backgammon AI Paper — Overview

## Summary

This paper is "From Heuristics to Neural Nets: Backgammon AI Agents" — a research paper I wrote as the final project for **CSCE 775: Deep Reinforcement Learning** at the University of South Carolina. Submitted May 5, 2025. I'm the sole author.

The work implements and compares a spectrum of decision-making algorithms for playing Backgammon: minimax search with α-β pruning, Monte Carlo learning, TD(0), and TD(λ) with eligibility traces. The conclusion: **TD(λ) with eligibility traces wins**, beating all other approaches in head-to-head play.

## Why Backgammon

Backgammon is one of the world's oldest two-player board games — over 5,000 years old, originating in Mesopotamia, spreading through Persia, Rome, Byzantium, and medieval Europe. It remains deeply embedded in Middle Eastern culture today.

From an AI perspective it's an ideal testbed because:
- **Vast state space** — on the order of 10²⁰ possible configurations, far exceeding chess or checkers
- **Stochastic** — dice rolls inject randomness that pure minimax can't fully handle
- **Strategic depth** — real long-term planning is required, not just tactical evaluation

This combination makes exhaustive search infeasible and forces approximation methods. Backgammon was historically one of the first games where neural-network-based RL surpassed handcrafted heuristics — Tesauro's TD-Gammon work in the 90s. My project builds on that lineage.

## What I Implemented

Five distinct agents, all evaluated under the same protocol:

1. **Minimax with α-β pruning** at 2-ply depth + chance node, with a handcrafted heuristic
2. **TD(0)** with a multilayer perceptron value network
3. **TD(λ)** with eligibility traces, same network architecture
4. **Monte Carlo (MC) learning** with same architecture, full-episode returns
5. **Three baseline heuristics** for comparison: Random, Furthest-First, Closest-First

## Headline Result

In a round-robin tournament of 1000 games per pairing among the 35,000-episode-trained variants:

| Agent | Wins | Rank |
|-------|------|------|
| TD(λ) | 2 | 1st |
| TD(0) | 1 | 2nd |
| MC | 0 | 3rd |

TD(λ) outperformed both TD(0) and Monte Carlo. This validates the bias-variance tradeoff that eligibility traces provide — multi-step credit assignment is more stable than pure 1-step bootstrapping (TD(0)) but less variance-prone than full episode returns (MC).

## Connection to Tesauro's TD-Gammon

TD-Gammon by Gerald Tesauro is the landmark prior work — a single MLP trained entirely by TD(λ) self-play, achieving master-level performance against human grandmasters in the 90s.

The original TD-Gammon paper omits critical hyperparameter details (λ schedule, learning rate, state representation specifics). Direct replication isn't possible from the paper alone. By independently tuning these, my agents achieved **win rates comparable to the original**, validating the robustness of deep function approximation for stochastic board games.

## Code

GitHub repo: https://github.com/markshperkin/BackgammonAI-backend

## Course Context

- **Course**: CSCE 775: Deep Reinforcement Learning
- **Institution**: University of South Carolina, Department of Computer Science and Engineering
- **Term**: Spring 2025
- **Date submitted**: May 5, 2025
- **Author**: Mark Shperkin (sole author)

## Keywords

Backgammon, reinforcement learning, deep reinforcement learning, CSCE 775, USC, Mark Shperkin, TD learning, TD(0), TD(lambda), TD-Gammon, eligibility traces, Monte Carlo, minimax search, alpha-beta pruning, MLP, multilayer perceptron, value function approximation, self-play, stochastic games, value network, Tesauro, Neurogammon
