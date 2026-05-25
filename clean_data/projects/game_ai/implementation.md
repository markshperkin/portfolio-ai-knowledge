# Game-AI — Implementation

## Connect Four Game Logic

### The Board
A standard Connect Four board: 7 columns × 6 rows. Pieces drop from the top of a column and stack on previous pieces (or the bottom). Each cell holds either:
- Empty
- Player 1's piece
- Player 2's piece

The board can be represented as a 2D array, a list of column stacks, or a bitboard. Each has tradeoffs (memory vs. speed). For a course project, a clean 2D array is most readable.

### The Rules
- Players alternate placing pieces in columns
- A piece falls to the lowest empty cell in the chosen column
- First to four in a row (horizontally, vertically, or diagonally) wins
- If the board fills with no winner, it's a draw

### Win Detection
Check all 4-in-a-row possibilities after each move:
- Horizontal lines (4 across)
- Vertical lines (4 up)
- Diagonal lines (4 on each diagonal direction)

This is O(board_size) per move check, which is fast enough.

## Minimax with Alpha-Beta

The core AI algorithm. Pseudocode:

```python
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over(board):
        return heuristic(board)
    
    if maximizing_player:
        best_value = -infinity
        for move in legal_moves(board):
            new_board = apply_move(board, move)
            value = minimax(new_board, depth-1, alpha, beta, False)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # beta cutoff
        return best_value
    else:
        best_value = +infinity
        for move in legal_moves(board):
            new_board = apply_move(board, move)
            value = minimax(new_board, depth-1, alpha, beta, True)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # alpha cutoff
        return best_value
```

The pruning happens at the `if beta <= alpha: break` lines. When the search realizes a branch can't improve the current best, it abandons it.

## Heuristic Function

For Connect Four specifically, the heuristic typically scores:

### Pattern-Based Scoring
- Three-in-a-row with an empty fourth space: high positive (one move from win)
- Two-in-a-row with two empty: moderate positive
- Block opponent's three-in-a-row: high positive (defense matters)
- Center column control: moderate positive (more 4-in-a-row possibilities go through center)

### Aggregate
Sum the scores across all 4-in-a-row windows. Subtract the opponent's equivalent score. The net is the position value from the agent's perspective.

A good heuristic gives the AI strong play even at modest search depths. A bad heuristic combined with deep search still plays poorly because the leaf evaluations are misleading.

## Search Depth Trade-Off

Deeper search = stronger play but exponentially slower. Connect Four's branching factor is roughly 7 (one per column). At depth `d`, you're looking at roughly `7^d` positions:

| Depth | Approx positions |
|-------|------------------|
| 4 | ~2,400 |
| 5 | ~17,000 |
| 6 | ~117,000 |
| 8 | ~5.7M |

With alpha-beta pruning, effective branching factor drops significantly — maybe to 3-4. So depth 6-8 is often interactive at human speed.

## Project Architecture

The repo splits cleanly into three modules:

### `engine`
Contains the AI agent code. The minimax search, alpha-beta pruning, and heuristic evaluation live here. This is the part that does the "thinking."

### `environments`
Game state representation. Methods to check legal moves, apply moves, detect wins, and serialize/deserialize boards. The engine uses environments — it doesn't know about visualization.

### `visualizer`
Pure rendering — takes a board state and shows it. Doesn't know about game rules or AI. Just visualizes whatever it's handed.

This separation matters because:
- You can swap the visualizer for a different UI (CLI, web, GUI) without touching AI logic
- You can run AI vs. random moves without launching the visualizer (faster for testing)
- You can run AI vs. AI for self-play evaluation

## Modes

### Human vs. AI
Human clicks a column; the AI responds. Standard play mode.

### AI vs. Random Moves
The AI plays against an opponent that picks moves uniformly at random. Useful for:
- Stress-testing the AI's win rate
- Quickly running many games for evaluation
- Debugging the AI's decision-making

If your AI loses regularly to random moves, something is broken.

## Lessons Learned

### Alpha-Beta Cuts the Tree, Not the Logic
The pruning is just an optimization — it doesn't change which move the AI picks. The output is identical to plain minimax; alpha-beta just gets there faster.

### Heuristic Quality Dominates Search Depth
A great heuristic at depth 4 beats a mediocre one at depth 8. Tuning the heuristic was higher-leverage than pushing search deeper.

### Move Ordering Affects Pruning
Alpha-beta prunes more when the best moves are evaluated first. Ordering moves by some quick heuristic (e.g., center first) before recursive search dramatically improves pruning effectiveness.

### Game Engines Need Clean Abstractions
The engine/environment/visualizer separation made debugging much easier. When something went wrong, I could isolate whether it was AI logic, rule enforcement, or rendering.

## Connection to Later Work

This project was the foundation for my Backgammon AI paper. The minimax + alpha-beta core was reused — extended with CHANCE nodes for Backgammon's dice rolls. Connect Four was the simpler deterministic case; Backgammon was the harder stochastic generalization.

## Keywords

Connect Four, minimax, alpha-beta pruning, game tree search, MAX node, MIN node, heuristic evaluation, search depth, branching factor, pattern-based scoring, center control, three-in-a-row, win detection, engine environment visualizer, AI vs random, move ordering, game engine architecture, numpy
