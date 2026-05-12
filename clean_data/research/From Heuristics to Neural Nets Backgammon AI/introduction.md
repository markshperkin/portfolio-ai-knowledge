# Backgammon AI — Introduction & Problem Framing

## What Makes Backgammon Hard

Backgammon is an ancient two-player, zero-sum board game that combines deep strategic planning with stochastic dice-roll outcomes. From an AI standpoint, three properties make it a notoriously challenging RL domain:

### 1. Enormous State Space
On the order of **10²⁰ possible configurations**. For comparison:
- Tic-tac-toe: ~10³ states
- Checkers: ~10²⁰ states (similar scale, but deterministic)
- Chess: ~10⁴³ states
- Go: ~10¹⁷⁰ states

Backgammon is in checkers/chess territory but with an added curveball — randomness.

### 2. Stochastic Dynamics
Each turn begins with a dice roll. The agent doesn't choose the roll; the environment does. This means decision-making must happen **under uncertainty** — you're not picking the best deterministic move, you're picking the best move averaged over all possible next dice outcomes.

This is what kills naive minimax search: you can't just MAX over your own moves and MIN over opponent moves; you need a **CHANCE node** that averages over dice outcomes.

### 3. Strategic Depth
Backgammon rewards long-term positioning. Expert play involves blocking, hitting, building primes, and bearing-off optimization that simple heuristics miss. A two-ply lookahead can take **minutes** to evaluate in practice — and even that won't capture nuanced strategy.

## Why This Combination is RL-Native

Programming an agent to play Backgammon at a high level requires balancing:
- Long-term strategy (multi-step planning)
- Probabilistic evaluation of chance events
- Computational tractability over a 10²⁰-state space

Pure brute-force approaches, even with shallow heuristics, can't capture expert tactics. This is exactly the regime where reinforcement learning shines — the agent learns value estimates through self-play, and function approximation (neural networks) generalizes across the vast state space.

## What This Project Sets Out to Do

Develop and compare a suite of algorithms ranging from:
- **Minimax search** with α-β pruning (classical AI, handcrafted heuristic)
- **Monte Carlo (MC) simulation** (full-episode returns)
- **TD(0)** (one-step bootstrapping)
- **TD(λ)** (eligibility traces, multi-step credit assignment)

The goal is to determine **which methods best navigate Backgammon's combinatorial complexity**.

## Why It Matters Beyond Backgammon

Achieving strong performance in this domain not only advances RL in stochastic environments — it also demonstrates AI's potential to learn sophisticated strategies that rival human expertise.

The lessons generalize. Stochastic games with massive state spaces are everywhere: financial decision-making, real-time strategy games, autonomous driving in uncertain environments. Whatever works in Backgammon teaches us something about that broader class of problems.

## Framing the Decision Tree

For a backgammon move, the decision tree has three node types:

- **MAX nodes** — the agent's move; pick the highest-utility successor
- **MIN nodes** — the opponent's move; pick the lowest-utility successor (assuming optimal opponent)
- **CHANCE nodes** — dice roll; weighted average over all dice outcomes

Pure minimax handles MAX and MIN. The CHANCE node turns this into **expected minimax** — value at a chance node = `Σᵣ P(r) · h(s)` for each dice outcome r.

This expectation is what makes the search tree balloon. Each turn has 21 distinct dice combinations, each requiring its own subtree.

## Keywords

introduction, problem framing, backgammon AI, state space, 10^20, stochastic games, dice roll, expected minimax, MAX node, MIN node, chance node, decision tree, reinforcement learning, function approximation, RL motivation, combinatorial complexity
