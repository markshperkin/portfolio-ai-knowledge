# Monte Carlo Learning

## How MC Differs from TD

Monte Carlo (MC) methods estimate the state-value function `V(s)` by **averaging full-episode returns** rather than bootstrapping from intermediate predictions.

The fundamental difference from TD methods:
- **TD** updates after every step, using its own value estimate of the next state as the bootstrap target
- **MC** waits until the end of the episode and updates using the actual observed return

This means MC has:
- ✅ **No bootstrap noise** — updates use real returns, not estimated ones
- ❌ **High variance** — full-episode returns include all the noise of the entire game
- ❌ **Delayed updates** — must wait until episode end before updating

## The Architecture

I reused the **same multilayer perceptron architecture** and hyperparameters as in the TD(0)/TD(λ) implementations:
- 28-dimensional input
- 80 hidden units, sigmoid activation
- 4-dimensional output `[pW_reg, pW_gammon, pB_reg, pB_gammon]`

Using identical architecture lets me isolate the algorithmic contribution — any performance differences between MC, TD(0), and TD(λ) are attributable to the **algorithm**, not network design.

## The Return Calculation

During self-play, for an episode of length T, I record all states and rewards `(s_t, G_t)`.

Let `{r_1, r_2, ..., r_T}` denote the sequence of reward vectors:
- `r_t = 0` for `t = 0, 1, ..., T-1` (no reward at intermediate states)
- `r_T = e_k` (one-hot terminal vector at game end, k indicates win type)

The **return** at time T is just the terminal reward:
`G_T = r_T = e_k`

At time T-1, with discount factor γ:
`G_{T-1} = γ · r_T = γ · e_k`

Generally:
`G_t = Σ_{i=t+1 to T} γ^{i − (t+1)} · r_i`

For Backgammon specifically (no intermediate rewards), this simplifies to:
`G_t = γ^{T-1-t} · e_k`

## The Update Rule

For each visited state `s_t` in the episode:
`θ ← θ + α · [G_t − V(s_t; θ)] · ∇_θ V(s_t; θ)`

Note this uses `s_t` (each visited state), and the target `G_t` is the **discounted return from time t onwards**, computed from the actual terminal outcome.

## Single Backward Pass per Episode

I perform a **single backward pass per episode**. The network's outputs for all visited states `(s_t, G_t)` in the recorded episode are regressed toward their true returns.

By deferring weight updates until episode end, MC learning eliminates the bootstrap noise inherent in TD(0). The gradient signals are more stable in the sense that they're based on actually observed outcomes — not on the network's own (potentially incorrect) estimates of future value.

## The Trade-Off in Practice

In my experiments, MC underperformed both TD(0) and TD(λ) in head-to-head play:

| Agent (35K episodes) | Wins (round-robin) | Rank |
|----------------------|---------------------|------|
| TD(λ) | 2 | 1st |
| TD(0) | 1 | 2nd |
| MC | 0 | 3rd |

Why did MC lose despite having no bootstrap noise?

**Variance**. Backgammon games are long (30-60 turns) and chaotic. The full-episode return is a noisy signal because intermediate dice rolls add huge variance to the final outcome. A single dice roll can flip a game from winning to losing.

TD methods, especially TD(λ), benefit from intermediate value estimates that smooth this noise. MC is at the mercy of the full game's variance, which makes its updates less reliable.

This is exactly the bias-variance tradeoff that motivates eligibility traces. Pure MC (λ = 1 in the TD(λ) framework) is high-variance. Pure TD(0) (λ = 0) is high-bias. TD(λ = 0.8) interpolates and wins.

## Why MC Still Beat the Heuristic Baselines

Even though MC came in third among the RL methods, it still **handily beat all the heuristic baselines** (Random, Closest-First, Furthest-First). This shows that:
1. Function approximation + self-play is a powerful combination, even with a high-variance learning rule
2. Self-play exposes the network to enough state-space coverage to learn meaningful representations

MC isn't "bad" — it just isn't the best of the three RL methods I tried.

## Practical Considerations

- **MC is simpler to implement** than TD(λ) (no eligibility traces to maintain)
- **MC is simpler to debug** because the targets (actual returns) are observable, not estimated
- **MC requires more episodes** to converge in high-variance games — I found MC needed the full 35,000 episodes to reliably beat heuristic baselines, while TD methods showed gains earlier

If I were teaching RL, I'd start with MC for its conceptual clarity, then move to TD(0) for its efficiency, then TD(λ) for the right answer.

## Keywords

Monte Carlo learning, MC method, full episode return, discounted return, self-play, model-free RL, value function, MLP, no bootstrap, high variance, terminal reward, episode-end update, single backward pass, batch update, MC vs TD, Backgammon RL, function approximation
