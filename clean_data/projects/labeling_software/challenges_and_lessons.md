# LabelingSoftware — Challenges & Lessons

## What Was Hard

### Plot Performance with Long Sensor Streams

A typical swimming session produces ~30,000 samples of accelerometer and gyroscope data. Plotting all of those points naively in the browser was slow — scrolling lagged, zooming felt sticky, the UI froze when loading new sessions.

**Solution**: Down-sampled the plot rendering to ~5,000 visible points per axis at any zoom level, computed by stride-based subsampling. This kept the visual fidelity high enough for accurate annotation while making the UI responsive.

### Synchronizing Two Different Time Bases

Sensor data was at 52.63 Hz (a non-standard rate from the smartwatch API). Video was at 30 FPS. Synchronizing scrubbing across both required careful conversion math:
- Sample index → seconds → video frame
- Video frame → seconds → sample index

**Solution**: Built a single time conversion utility used everywhere. All plot ↔ video sync goes through it. Bug-free conversion was critical because sync drift would make annotations inaccurate.

### Class Label Schema

Initially I had a fixed set of labels for swimming, but realized the tool should generalize. So I made the class label set configurable per-dataset. That meant:
- Each session has a `classes.json` defining its label set
- The class picker UI dynamically renders based on this file
- Annotations reference class IDs that map to the dataset's label set

**Solution**: Treating labels as data, not code. The tool itself knows nothing about "freestyle" or "wall touch" — the dataset configuration provides those.

### Annotation Boundary Snapping

Users would try to set segment boundaries at exact sample indices but the click position is in pixels. Slight misclicks led to boundaries 5-10 samples off from where the user intended.

**Solution**: Implemented snap-to-feature behavior. When a user releases a drag, the boundary snaps to the nearest local maxima/minima in the signal, or to the nearest existing annotation boundary. Made annotation noticeably more precise.

## What I Learned

### Build Tools That Make Your Own Work Easier
The tool only existed because annotation was a real bottleneck for my thesis. Tools built to scratch your own itch tend to be sharper than tools built speculatively. I knew exactly what was painful and could fix it directly.

### Local-First is Underrated
A web app that runs locally with file-system storage has many advantages over cloud-based equivalents:
- No auth complexity
- No network latency
- No data exfiltration concerns (research data often has privacy or IP constraints)
- No infrastructure cost

For research tools, local-first should be the default unless there's a clear collaboration need.

### React's State Model Pays Off for Stateful UIs
The labeling UI is intrinsically stateful — current position, selected segment, undo history, edit mode. Building this in vanilla JS would have been miserable. React's component + state model made it tractable.

### The 90% Solution Beats the 100% Solution
Many features I considered didn't get built:
- Multi-user collaboration
- Cloud sync
- Custom plot styling
- Auto-suggest label predictions

None of them were necessary. The simple, focused tool got the labels done. Adding features for hypothetical needs would have delayed the actual research.

### Visual Affordances Matter More Than Features
The single biggest UX improvement I made was adding **drag handles on segment boundaries**. They didn't add new features — they made it visually obvious where users could click to resize a segment. This kind of small affordance change often has bigger UX impact than a whole new capability.

## What I'd Do Differently

If I were rebuilding this:
- **TypeScript end-to-end** — would have caught several silent state bugs
- **WebAssembly for plot rendering** — would handle longer sessions without down-sampling
- **Built-in dataset templates** — making it even faster to bootstrap new label sets
- **Auto-save with versioning** — no risk of losing work, with the ability to revert mistaken edits
- **Open-source it cleanly** — the current repo is research-grade; a polished release could help others

## When This Tool Doesn't Apply

I want to be honest about scope:
- It's not a substitute for commercial annotation platforms (CVAT, Labelbox) for big team workflows
- It doesn't handle non-time-series data (images, raw audio without sync)
- It's optimized for single-researcher use, not enterprise

For its actual use case (research-grade IMU+video annotation), it's good. For other contexts, use other tools.

## Keywords

challenges, lessons learned, plot performance, time synchronization, sampling rate conversion, class label configuration, snap-to-feature, React state management, local-first, file-system storage, scratch your own itch, 90 percent solution, visual affordances, drag handles, research tools
