# Experimental Results

## Evaluation Protocol

The experimental evaluation followed a **round-robin format**: each agent played **1000 games against every other agent**. This design ensures broad coverage of opponent behaviors and mitigates the impact of stochastic outcomes on any single pairing.

1000 games per pairing is enough to statistically distinguish meaningful win-rate differences. Backgammon outcomes have substantial randomness from dice, so anything less would be vulnerable to small-sample noise.

## Baseline Agents

I implemented three heuristic baselines for comparison:

- **Random Agent** — selects a uniformly random action `a` in state `s`
- **Furthest-First Agent (FFA)** — selects the action that has the largest distance from bearing off
- **Closest-First Agent (CFA)** — selects the action that has the smallest distance from bearing off

### Baseline Tournament Results

| Agent | vs. Random | vs. CFA | vs. FFA | Wins | Rank |
|-------|------------|---------|---------|------|------|
| Random | — | 393 | 431 | 0 | 3rd |
| CFA | 607 | — | 368 | 1 | 2nd |
| FFA | 659 | 632 | — | 2 | 1st |

**FFA outperformed all baselines.** Closest-First placed last. This is intuitive — pushing checkers forward aggressively dominates over keeping them back. FFA serves as the strongest baseline for the RL methods to beat.

## Network Architecture Comparison

I tested two MLP architectures:
- **V1** — single hidden layer with 80 units (the primary architecture)
- **V2** — two hidden layers (60 and 30 units, respectively)

Both were trained using TD(0).

| Architecture | Wins (sum across all variants) | Rank |
|--------------|-------------------------------|------|
| V1 | 4565 | 1st |
| V2 | 4435 | 2nd |

**The single hidden layer V1 outperformed the deeper V2.** Backgammon's value function might just not need a deep representation — the linear separability of board features after a single hidden layer's nonlinearity is sufficient.

This is a useful finding. Deeper isn't always better, especially for problems with limited training data (35,000 episodes is decent but not massive by deep RL standards).

## Training Duration Effects

To evaluate the effect of training duration, each algorithmic variant was trained for **4000, 10000, and 35000 self-play episodes**.

This range was selected to determine whether extended exposure to Backgammon's enormous 10²⁰ state space yields consistent policy improvement.

### TD(0) v1 e Variants

| | vs. FFA | vs. 4000 | vs. 10000 | vs. 35000 | Wins | Rank |
|---|---------|----------|-----------|-----------|------|------|
| FFA | — | 477 | 489 | 349 | 0 | 4th |
| E=4000 | 523 | — | 504 | 343 | 2 | 2nd |
| E=10000 | 511 | 496 | — | 372 | 1 | 3rd |
| E=35000 | **651** | **657** | **628** | — | **3** | **1st** |

### TD(λ=0.8) v1 e Variants

| | vs. FFA | vs. 4000 | vs. 10000 | vs. 35000 | Wins | Rank |
|---|---------|----------|-----------|-----------|------|------|
| FFA | — | 338 | 397 | 376 | 0 | 4th |
| E=4000 | **662** | — | 546 | 476 | 2 | 2nd |
| E=10000 | 603 | 454 | — | 427 | 1 | 3rd |
| E=35000 | 624 | 524 | **573** | — | **3** | **1st** |

### MC v1 e Variants

| | vs. FFA | vs. 4000 | vs. 10000 | vs. 35000 | Wins | Rank |
|---|---------|----------|-----------|-----------|------|------|
| FFA | — | 515 | 530 | 456 | 2 | 2nd |
| E=4000 | 485 | — | 460 | 348 | 0 | 4th |
| E=10000 | 470 | 540 | — | 432 | 1 | 3rd |
| E=35000 | **544** | **652** | **568** | — | **3** | **1st** |

### Patterns Across All Three

**Universal**: The 35,000-episode variant consistently ranks first across all three algorithms. More episodes → better play.

**Algorithm-specific oddities**:
- **TD(0)**: 10K-episode model **underperforms** the 4K-episode version. Hints at transient instability during mid-training.
- **TD(λ)**: A similar dip occurs at 10K episodes before recovering at 35K.
- **MC**: Must run the full 35K games to even eclipse the FFA heuristic. MC needs more data.

These trends confirm that **more episodes generally refine policy quality**, but the **shape of the learning curve** differs by algorithm. The point of diminishing returns varies with each algorithm's use of bootstrapping, eligibility traces, and exploration-exploitation balance.

## The Final Tournament

After extensive evaluation, I selected the **35,000-episode variants** from each algorithmic family and put them in a final head-to-head round-robin.

| Agent | vs. TD(0) | vs. TD(λ) | vs. MC | Wins | Rank |
|-------|-----------|-----------|--------|------|------|
| TD(0) | — | 455 | 614 | 1 | 2nd |
| **TD(λ)** | **545** | — | **616** | **2** | **1st** |
| MC | 386 | 384 | — | 0 | 3rd |

**TD(λ) outperforms both TD(0) and MC.**

This validates the central hypothesis: eligibility traces provide an effective tradeoff between bias and variance in value estimation. TD(λ) is the most capable of navigating Backgammon's enormous state space and capturing its subtle strategic nuances.

## What These Results Mean

A few takeaways:

1. **Deep RL with self-play meaningfully beats heuristic baselines.** All three RL methods (when adequately trained) surpassed the strongest baseline (FFA).

2. **TD(λ) is the right algorithm for stochastic games with long horizons.** The bias-variance balance from eligibility traces is exactly what high-variance environments like Backgammon need.

3. **More training matters, but with caveats.** The non-monotonic improvement (4K → dip at 10K → strong at 35K) shows that RL training isn't smooth. You can't just look at one checkpoint and trust it.

4. **Simpler architectures can win.** A single hidden layer of 80 units beat a deeper two-layer network. Don't reach for complexity unless you need it.

5. **Network architecture choices interact with algorithm choices.** I only tested V1 and V2 with TD(0). If I'd tested deeper networks with TD(λ), maybe the deeper one would have won. That's a known limitation of one-at-a-time hyperparameter studies.

## Keywords

experimental results, round robin, 1000 games, baseline agents, random agent, furthest first, closest first, network architecture comparison, V1 V2, training duration, episodes, 4000 10000 35000, learning curve, head to head tournament, TD lambda wins, bias variance tradeoff, Backgammon evaluation, numpy
