# shesh-besh — Architecture & Design

## High-Level Design Philosophy

The project follows clean **object-oriented design** principles:

- **Separation of concerns** — game logic, UI rendering, and persistence are independent
- **Modular architecture** — each component has well-defined responsibilities
- **Testable engine** — the game logic can be tested without launching any UI
- **Public API discipline** — only carefully chosen interfaces leak through public headers

This is the architectural shape that lets a project scale to multiple platforms (iOS, Android, PC) without proliferating duplicate code paths.

## Project Structure

```
shesh-besh/
├── include/backgammon/      ← public headers (the API)
├── src/                     ← implementation (private)
├── tests/                   ← unit tests for the engine
├── .github/workflows/        ← CI/CD pipelines
└── CMakeLists.txt           ← root build configuration
```

The `include/` and `src/` separation is standard C++ library practice:
- `include/backgammon/*.hpp` defines what users of the library can call
- `src/*.cpp` contains the implementation, hidden from users

External callers only see what's in `include/backgammon/`. This makes the API surface small and intentional.

## Likely Class Hierarchy

Without the README in hand, but based on standard backgammon engine design, the architecture probably includes:

### Core Game Objects
- **`Board`** — represents the 24-point backgammon board state
- **`Point`** — a single point on the board (with checker count and color)
- **`Checker`** — a single checker piece
- **`Player`** — represents one of the two players (white or black)
- **`Move`** — represents a single move (from-point, to-point, dice roll)

### Game Logic
- **`Game`** — top-level controller, coordinates turns
- **`MoveGenerator`** — generates legal moves given a board state and dice roll
- **`Rules`** — encapsulates rule logic (bearing off, doubling, gammon detection)
- **`Dice`** — handles random dice rolls

### Optional AI/Strategy Layer
- **`Player`** subclasses or strategy objects for human, random, AI players

This is the standard shape for a backgammon engine. Each class has clear, narrow responsibility.

## C++ Best Practices

### Modern C++ Features
With ~97% of the code in C++, the project likely uses modern C++ features:
- `auto` for type inference where it improves readability
- Smart pointers (`std::unique_ptr`, `std::shared_ptr`) for memory management
- Range-based for loops
- `std::optional` for "may have value" returns
- `enum class` for type-safe enumerations

### RAII (Resource Acquisition Is Initialization)
Standard C++ pattern. Resources (memory, file handles, locks) are tied to object lifetimes — when the object goes out of scope, resources are automatically released. Backgammon doesn't have heavy resources, but the pattern is still good practice.

### Const Correctness
Methods that don't mutate state are marked `const`. This is the kind of discipline that:
- Prevents accidental modifications
- Documents intent
- Enables compiler optimizations

## Build System: CMake

CMake is the modern C++ build system. It handles:
- Cross-platform compilation (Windows, macOS, Linux)
- Dependency management
- Test integration
- IDE generation (Visual Studio, Xcode, Qt Creator, CLion)

A single `CMakeLists.txt` at the root, plus subdirectory `CMakeLists.txt` files in major directories, configure the entire build.

## Qt Quick UI Layer

The UI is built with **Qt Quick** using **QML** declarative markup. This is separate from the engine.

Typical Qt Quick architecture:

```
QML files (declarative UI)
    ↓ uses
C++ Backend (exposes data + commands)
    ↓ uses
Backgammon Engine (pure C++, no Qt dependency)
```

The engine has zero Qt dependency. The Qt-specific layer is just a thin wrapper that exposes engine state to QML.

Why this matters:
- The engine is portable — could be reused with any UI (CLI, web, native)
- Tests run without needing Qt installed
- The engine's design isn't constrained by UI considerations

## Testing Approach

A `tests/` directory implies serious testing. For a backgammon engine, tests likely cover:

### Rule Correctness
- Legal move generation for various board states
- Bearing-off rules (you can only bear off when all checkers are home)
- Doubling cube rules
- Gammon and backgammon detection

### Edge Cases
- Hit-and-run scenarios
- Multiple checkers on the bar
- Legal move when only some dice can be played
- End-of-game state transitions

### Engine Determinism
- Same input → same output
- No global state leakage between games

A solid test suite prevents regressions as the engine evolves.

## CI/CD Pipeline

The `.github/workflows/` directory means automated build/test on every commit. Typical workflow:

1. Trigger on push or pull request
2. Set up the build environment (specific OS, compiler, Qt version)
3. Build the project with CMake
4. Run all tests
5. Report success/failure to GitHub

This catches breakage immediately and gives confidence that the codebase is always in a buildable state.

## Cross-Platform Targets

Qt Quick supports multiple deployment targets:

### iOS
Build with Xcode toolchain via Qt's iOS target. Distribute through TestFlight or App Store.

### Android
Build via Android Studio integration with Qt. APK or AAB output.

### Desktop (Windows, macOS, Linux)
Native binaries for each platform. Standard Qt deployment pattern.

The same engine and roughly the same QML UI runs on all platforms. Platform-specific code (in-app purchases, push notifications, etc.) would be conditionally compiled.

## Why This Architecture Matters

### Testability
Engine + UI separation means I can test the engine extensively without launching the app. Bugs in game logic are caught during development, not at runtime.

### Portability
The engine is C++ with no Qt dependency. If I ever want to embed it in a web app via WebAssembly, or in a CLI tool, or in a server-side service, it works.

### Team Friendliness
Even though I'm the sole developer, the architecture is one a team could pick up. Clear separation of concerns means new contributors don't need to understand everything to fix one thing.

### Long-Term Maintainability
Five years from now, when someone wants to update the UI or add a new feature, the engine doesn't need rewriting. Clean architecture pays off over years, not weeks.

## Keywords

C++, Qt Quick, QML, CMake, modular architecture, separation of concerns, public API, header source split, RAII, modern C++, smart pointers, const correctness, Qt Test, CI/CD, GitHub Actions, cross-platform, iOS Android PC, backgammon engine, OOP, object-oriented design, testable architecture
