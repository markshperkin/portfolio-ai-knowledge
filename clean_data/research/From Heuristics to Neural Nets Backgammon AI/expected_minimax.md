# Expected Minimax with α-β Pruning

## The Formulation

I model Backgammon move selection as an **expected minimax search problem** augmented with α-β pruning. The search tree alternates between three node types:

### MAX Nodes (Agent's Move)
The agent picks the highest-utility successor:
`V(s) = max{a ∈ Moves(s)} h(s')`

### MIN Nodes (Opponent's Move)
The opponent picks the lowest-utility successor (assuming optimal play):
`V(s) = min{a ∈ Moves(s)} h(s')`

### CHANCE Nodes (Dice Roll)
Computed weighted average over all dice outcomes:
`V(s) = Σᵣ P(r) · h(s')`

This third node type is what makes Backgammon's search tree larger than chess's at equivalent depth — each turn has 21 distinct dice combinations to enumerate.

## α-β Pruning for Tractability

To reduce computation cost and curb tree explosion, α and β bounds are propagated down through MAX and MIN nodes. Branches whose potential values cannot influence the final decision are **pruned** — never evaluated.

α-β pruning preserves optimality (it never prunes a branch that could change the result) but dramatically reduces the number of evaluated positions. For a typical chess-like game, α-β can reduce the effective branching factor by an order of magnitude.

## The Heuristic Function

I designed a handcrafted heuristic `h(s)` that approximates strategic value:

For each player p, define:
- **Dₚ** — sum of pip-distances remaining to bear off
- **P̄ₚ** — count of checkers on the bar (sent there by being hit)
- **Bₚ** — count of borne-off checkers
- **Sₚ** — number of locations occupied by 2+ checkers (board control)

Then:
`hₚ(s) = Dₚ + 30·P̄ₚ − 30·Bₚ − 3·Sₚ`

And the overall value:
- `h(s) = h_black(s) − h_white(s)` if black to move
- `h(s) = h_white(s) − h_black(s)` if white to move

The signs work out so that **higher values favor the side currently moving**. The 30× weight on bar checkers and borne-off checkers reflects that those are big positional factors. The 3× on board control reflects its smaller but real impact.

## What the Heuristic Captures

The h(s) function captures two key strategic dimensions:
- **Progress toward bearing off** (the Dₚ and Bₚ terms)
- **Board control** (the Sₚ term — making points)

This is far from optimal play, but it gives the minimax search a meaningful evaluation signal at the leaves of the truncated tree.

## Search Depth

I restrict the expected minimax search to **two plies (one move per player) plus a subsequent CHANCE node**.

This shallow-depth strategy, combined with α-β pruning, brings per-move computation from tens of minutes down to **just a few minutes**. As the game advances and the branching factor shrinks (fewer pieces in play), computation time decreases further. Complete games run in roughly **20 minutes**.

## The Real Trade-Off

Why only 2-ply? Because the chance node massively expands the tree. Going to 3-ply with chance nodes between each ply means the branching factor explodes by 21 at every transition. The numbers stop being computationally feasible.

This is the fundamental issue with classical minimax for stochastic games: the chance nodes make depth expensive. Deep RL avoids this entirely by learning a value function that doesn't require explicit search at inference time — the network captures the long-horizon evaluation implicitly.

## What This Approach Achieves

By balancing:
- Selective deepening (2-ply with chance node)
- A robust heuristic
- Stochastic sampling at chance nodes
- α-β pruning

This produces a **tractable yet strategically informed agent** for Backgammon play.

## Why I Excluded It from the Main Tournament

Despite implementing it, I did not include the minimax agent in the full round-robin tournament. The reason was practical:
- 2-ply minimax with α-β pruning required ~20 minutes per game
- A 1000-game tournament against each of 4 other agents would have taken ~14 days of compute
- Time constraints forced me to skip it

This is a real limitation, and I document it in the conclusion. The minimax agent works; I just couldn't afford to run it at scale alongside the RL methods.

## Keywords

expected minimax, alpha beta pruning, MAX node, MIN node, CHANCE node, dice outcomes, weighted average, search tree, two-ply search, ply depth, handcrafted heuristic, pip count, bar checkers, borne off, board control, search complexity, stochastic minimax, classical AI, game tree
