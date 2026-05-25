# Game-AI — Overview

## What It Is

A **Connect Four game with an AI opponent** built using the **minimax algorithm with alpha-beta pruning**. Created as a coursework project for an Artificial Intelligence class at the University of South Carolina.

GitHub: https://github.com/markshperkin/Game-AI

## What It Does

Implements a playable Connect Four environment where users compete against an AI agent. Supports multiple game modes:
- **Human vs. AI** — the main play mode
- **AI vs. random moves** — testing/debugging mode where the AI plays against a random-move opponent (useful for evaluating AI strength)

It also includes:
- **Visualization of gameplay** — see the board state, see moves animate
- **Heuristic evaluation** for AI decision-making — the AI doesn't search to game end (which would be too slow); it uses heuristics to evaluate intermediate positions

## Why Connect Four

Connect Four is a perfect AI testbed:
- Small enough to be playable and beatable
- Big enough that brute-force search isn't trivial
- Has a clear goal (four in a row)
- Has well-understood AI strategies (control the center, block threats)
- Solved game (perfect play forces a first-player win) — so you can validate your AI's quality

It's the classic minimax demonstration domain. If you can build a Connect Four AI, you understand the bones of game-tree search.

## The AI Approach

### Minimax
The agent considers all possible moves up to some depth, alternating between:
- **MAX nodes** — the agent picks the highest-utility move
- **MIN nodes** — the opponent picks the lowest-utility move (worst for the agent)

At a fixed depth, evaluate the board with a heuristic. Propagate values back up the tree to find the best agent move.

### Alpha-Beta Pruning
Optimization that dramatically reduces the search space. Tracks two bounds:
- **Alpha** — best value MAX can guarantee so far
- **Beta** — best value MIN can guarantee so far

When MIN is considering a move that's already worse than what MAX can guarantee elsewhere, we don't have to explore the rest of MIN's options for that branch. Same in reverse for MAX. This often cuts the search tree by an order of magnitude without losing optimality.

### Heuristic Evaluation
At the depth limit, the AI can't search further but needs to evaluate the board. Connect Four heuristics typically reward:
- Center column control
- Two-in-a-row, three-in-a-row patterns
- Threats (positions one move from winning)
- Blocking the opponent's threats

The exact heuristic balances these factors. A poorly tuned heuristic at low depth produces a weak AI; a well-tuned one is genuinely tough.

## Project Structure

The repo is organized into three main components:

| Component | Purpose |
|-----------|---------|
| `engine` | Core game logic and AI implementation |
| `environments` | Game state representation and rule enforcement |
| `visualizer` | Gameplay visualization tools |

This separation of concerns mirrors how real game AI systems are structured.

## Tech Stack

**Language**: Python (100%)

**Core algorithm**: Minimax with alpha-beta pruning

**Evaluation**: Heuristic-based static board evaluation

## How to Run

`python3 run_connect_four.py`

Simple, one-command execution. The visualizer pops up; you click columns to drop your piece; the AI responds.

## Connection to Backgammon AI Project

This was foundational work for my later Backgammon AI paper (CSCE 775: Deep Reinforcement Learning). The minimax + alpha-beta pruning core was the same idea, extended to Backgammon's stochastic CHANCE nodes. Connect Four was the warmup.

## My Role

Sole author. Built the game environment, AI agent, heuristic, and visualizer.

## Keywords

Game AI, Connect Four, minimax, alpha-beta pruning, game tree search, heuristic evaluation, adversarial search, AI agent, Python, USC, AI course, classical AI, two-player games, deterministic games, perfect information games, numpy
