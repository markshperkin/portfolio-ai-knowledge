# shesh-besh — Overview

## What It Is

**shesh-besh** is a **modern Backgammon engine** built in **C++** with **Qt Quick** for cross-platform deployment (iOS, Android, and PC). Designed with clean object-oriented architecture and modular separation of concerns.

"Shesh besh" (שש בש) is the Hebrew name for backgammon — and a reflection of where I grew up culturally. Backgammon is deeply embedded in Middle Eastern culture, played in cafes, at home, by people of all ages. Building a polished modern version felt personal as well as technically interesting.

GitHub: https://github.com/markshperkin/shesh-besh

## What It Does

A complete backgammon implementation with:
- Full game-rules engine
- Cross-platform UI via Qt Quick
- Clean separation of game logic from rendering
- Test suite for the engine

The engine handles all the standard backgammon rules — bearing off, hitting, doubling, gammon detection, legal-move generation, dice rolling, and so on.

## Why C++ and Qt Quick

### Why C++
Backgammon engines benefit from compute efficiency, especially if you want to plug in AI later (minimax search over the game tree, like in my Backgammon AI paper). C++ delivers:
- Fast execution
- Tight memory control
- Modern features (C++17/20) that make code clean while still being efficient
- Direct integration with Qt's C++ APIs

### Why Qt Quick
Qt Quick (with QML for UI declarations) is one of the few mature options for **truly cross-platform native apps**:
- iOS, Android, Windows, macOS, Linux from one codebase
- Native performance
- Declarative UI syntax (similar in spirit to React Native or Flutter)
- Mature, battle-tested in industrial applications

The combination of C++ engine + QML UI is a classic Qt pattern. The engine knows nothing about the UI; the UI knows about the engine via well-defined interfaces.

## Architecture Notes

The repo organization (from what's visible) shows a clean modular structure:

```
include/backgammon/    — public header files
src/                    — implementation
tests/                  — test suite
.github/workflows/      — CI/CD configuration
```

This separation suggests:
- **Header/source split** — standard C++ practice for libraries
- **`backgammon/` namespace prefix** — keeps the public API in one well-defined place
- **Test directory** — engine tested independently of UI
- **CI workflows** — automated build/test on commit

This is the architecture of a serious software project, not a quick demo.

## Tech Stack

- **C++** (~97.2%)
- **CMake** (~2.8%) — modern C++ build system
- **Qt Quick** — UI framework
- **QML** — declarative UI markup language
- **Qt Test** (likely) — testing framework

## Why I Built It

A few motivations:

### Personal Connection
Backgammon is part of my cultural background. Building a polished version is a way to honor that.

### Technical Practice
I'd worked on Backgammon AI in Python for my reinforcement learning paper. Building a clean C++ engine is the natural next step — applying the same domain understanding to a different language stack and a different question (clean engine design vs. learning algorithms).

### Cross-Platform Mobile
Qt Quick is one of the best ways to ship to iOS and Android from one codebase without React Native or Flutter. Learning that workflow is valuable in itself.

### Testable Architecture
Many game implementations entangle engine logic and UI rendering. Building it the right way — engine completely independent of UI, with full unit tests — is itself a skill worth practicing.

## My Role

Sole author. Designed the architecture, implemented the engine, built the UI, wrote the tests, set up CI/CD.

## Connection to Other Backgammon Work

This project is my **third Backgammon-related repository**:
1. **Game-AI** (Connect Four with minimax) — earlier classical AI work
2. **BackgammonAI-backend** — the codebase from my Backgammon AI research paper, focused on RL agents
3. **shesh-besh** — clean C++ engine for the game itself, separate from AI

Each tackled the game from a different angle. shesh-besh is about the **game implementation** itself; the others are about **AI agents** that play it.

## Keywords

shesh-besh, backgammon, C++, Qt Quick, QML, cross-platform, iOS Android PC, modular architecture, OOP, OOD, object-oriented design, modern C++, CMake, Qt Test, engine architecture, game implementation, header source split, public API, namespaced libraries, CI/CD, testable code
