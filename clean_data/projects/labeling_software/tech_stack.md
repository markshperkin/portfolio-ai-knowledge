# LabelingSoftware — Tech Stack

## Languages

- **JavaScript** (~60.7%) — primary frontend language
- **CSS** (~17.3%) — styling
- **HTML** (~1.2%) — markup
- **Python** (~20.8%) — backend logic

## Frontend

- **React** — component-based UI framework (using `.jsx` files)
- **Node.js / npm** — package manager and dev tooling
- Custom CSS for the timeline and annotation visualizations
- HTML5 video element for synchronized playback

## Backend

- **Python** — server logic
- **Flask** — lightweight web framework, perfect for a tool that doesn't need heavy infrastructure
- **CSV / JSON** — data persistence (no database required)
- File-system-based storage in `backend/data/` directory

## Video Handling

- **FFmpeg-compatible MP4 codec** — needed for browser playback
- HTML5 `<video>` element for synchronized playback
- JavaScript event listeners coordinate between video timecodes and sensor sample indices

## Why This Stack

A few intentional choices:

### Why React
React's component model is a natural fit for an annotation tool. Each visualization (timeline, video, label list, sensor trace) is a self-contained component. State management is straightforward — the current annotation, current video time, current sensor segment all live in well-defined places.

### Why Flask (not Django, FastAPI, etc.)
Flask is the lightest viable backend for this scale of project. There's no user auth, no concurrent users, no complex business logic — it's a single-user tool that reads files and saves files. Flask gets out of the way.

### Why File-System Storage (not a database)
- **Portability** — annotators can copy the data folder anywhere
- **Inspectability** — annotators can open CSVs and inspect labels with regular tools
- **Backup-friendly** — git, rsync, or any file backup tool works
- **No setup overhead** — no database to install, configure, or migrate

For research-scale data collection (hundreds to thousands of records), the file system is plenty. If this were going to scale to thousands of annotators or millions of segments, a database would make sense.

### Why CSV + JSON
- **CSV** for sensor data (rows of timestamps, accelerometer values, gyroscope values)
- **JSON** for label metadata (segment start/end indices, class names, annotator notes)

Two formats because they fit their use cases:
- CSV is the universal language of tabular sensor data
- JSON is more flexible for structured label metadata with nested fields

## Architecture Pattern

```
Frontend (React/Node)  ←→  Backend (Python/Flask)  ←→  File System Storage
```

Three-tier separation:
- **Presentation layer** — React handles all UI logic
- **Service layer** — Flask handles business logic (load file, save annotations, sync video time)
- **Storage layer** — flat files on disk

This is over-engineered for a strictly local single-user tool, but the separation pays off if it ever needs to be deployed remotely.

## Running It

The README documents the dev workflow:
1. Open one terminal, run the Python backend (`python app.py`)
2. Open another terminal, run the Node dev server (`npm run dev`)
3. Annotate

Two-terminal workflow is mildly annoying but standard for full-stack dev environments.

## Keywords

React, JavaScript, CSS, HTML, Flask, Python, Node, npm, full stack web app, frontend backend separation, file system storage, CSV, JSON, no database, FFmpeg, MP4 codec, video synchronization, web framework choice, lightweight stack, dev environment
