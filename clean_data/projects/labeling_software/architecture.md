# LabelingSoftware — Architecture

## Overall Shape

A simple two-tier architecture:

```
┌────────────────────────────┐
│  React Frontend (Browser)  │
│  - Sensor plot rendering    │
│  - Video synchronization    │
│  - Segment UI              │
└──────────────┬──────────────┘
               │  HTTP (JSON)
               ↓
┌────────────────────────────┐
│  Python Flask Backend       │
│  - Endpoint routing         │
│  - File I/O                 │
│  - Annotation persistence   │
└──────────────┬──────────────┘
               │
               ↓
┌────────────────────────────┐
│  File System Storage         │
│  - backend/data/raw/         │
│  - backend/data/videos/      │
│  - backend/data/labels/      │
└────────────────────────────┘
```

No database, no auth layer, no cloud. Local-first by design.

## Frontend Component Structure

The React app is organized around the labeling workflow:

- **App shell** — overall layout, state management
- **Plot component** — renders accelerometer and gyroscope time-series plots
- **Video component** — synchronized video player
- **Segment list component** — shows existing labeled segments
- **Class picker component** — assigns activity labels to selected segments
- **Toolbar** — load/save actions, undo/redo

Each component is responsible for a specific concern. State that needs to be shared (e.g., the current selected segment) lives in the parent component or in a context provider.

## Sync Between Plot and Video

The trickiest part of the architecture is keeping the sensor plot and video in sync.

The approach:
- Both have a "current time" position (sensor sample index ↔ video frame)
- Convert between them via the known sampling rates (sensor at ~52.63 Hz, video at 30 FPS)
- When the user clicks anywhere in the plot or scrubs the video, both update simultaneously
- A debounce on rapid updates prevents UI jank

This sync is what makes the tool usable. Without it, you'd have to mentally translate between sensor sample and video frame — which is exactly the friction the tool exists to remove.

## Backend Endpoint Layout

The Flask backend exposes a small REST API:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/sessions` | GET | List all available labeling sessions |
| `/sessions/<id>/sensors` | GET | Stream raw IMU data for a session |
| `/sessions/<id>/video` | GET | Serve video file |
| `/sessions/<id>/labels` | GET/POST | Read or write annotations |

Each endpoint is intentionally simple — it just reads or writes files in the structured directory. No business logic.

## Data Flow

A typical labeling session:

1. User opens the app, sees list of sessions
2. User selects a session → frontend fetches sensors + video metadata
3. User watches video, sees synchronized sensor plot
4. User identifies an activity → drags on the plot to select a temporal segment
5. User picks a class label from the dropdown
6. Frontend sends the new annotation to the backend
7. Backend persists it to the labels file
8. Frontend updates the segment list

This loop repeats for every annotation in the session.

## Deliberate Architectural Choices

### Stateless Backend
The backend doesn't track sessions or user state. Every request is self-contained. This makes the architecture trivial to reason about and easy to restart without losing data.

### Explicit File Layout
The structured data directory is part of the API. Anyone can drop new sessions in by following the directory convention — no API call to "register a session" needed.

### Frontend-Driven Logic
Most of the actual labeling logic (segment selection, class assignment, sync) lives on the frontend. The backend is dumb file storage. This makes hot-reloading the UI fast and lets the backend stay minimal.

## Limitations

- **Single user** — there's no concurrent editing protection. If two people open the same session, last write wins
- **No undo across sessions** — closing the browser loses undo history
- **Performance ceiling on long sessions** — the frontend loads all sensor data into memory, which gets sluggish past ~100K samples

For a single-user research tool, these limitations are acceptable.

## Keywords

architecture, two-tier, frontend backend, REST API, Flask endpoints, React state management, plot video sync, sample-to-frame conversion, file system storage, session structure, data directory layout, stateless backend, single user
