# LabelingSoftware — Use Case & Workflow

## The Concrete Use Case

I built this tool specifically for annotating **swimming IMU data**, but the workflow generalizes to any sensor + video labeling scenario.

The original problem: I had eleven collegiate swimmers wearing wrist-mounted Tic Watch Pro 5 smartwatches, recording accelerometer + gyroscope at 52.63 Hz. I also had pool-deck video of every set. To train an activity recognition model, I needed every sensor sample labeled with what the swimmer was doing at that moment — freestyle stroke, butterfly stroke, turn, push-off, wall touch, etc.

## The Workflow

### 1. Data Ingestion
Drop a sensor data file (CSV with timestamps and channel readings) and a synchronized video (MP4) into the backend's data folder.

### 2. Initial Sync Calibration
Find a known sync point in both streams — typically a sharp motion the swimmer makes at the start of recording (a deliberate hand clap, a foot tap, anything detectable in both). Mark the corresponding moment in the video and in the sensor stream. Now they're aligned.

### 3. Annotation Loop
With video and sensor traces synchronized:
- Play the video at any speed (slow-motion is your friend for fast events like wall touches)
- Watch for the start of an activity in the video
- Pause at the corresponding sensor sample
- Click-and-drag on the sensor timeline to mark the segment
- Choose a class label from a dropdown
- Add notes if needed

### 4. Persistence
Annotations save to a JSON file in the data directory. Sensor data stays in its CSV. Reload the project later and your work is intact.

### 5. Export
The tool produces clean labeled CSV output that's ready to feed directly into a training pipeline.

## What Makes Annotation Faster

A few features that mattered:

### Synchronized Video Scrubbing
When you scrub the sensor timeline, the video jumps to the same moment. When you scrub the video, the sensor cursor moves. This bidirectional sync is what makes labeling fast — you're never lost between the two streams.

### Multi-Channel Display
Showing all axes (accel x/y/z, gyro x/y/z) on the same timeline lets you spot patterns that aren't visible on any single channel. A push-off might be barely visible on accel x but clear on gyro y. You need to see all of them.

### Class-Specific Coloring
Each activity class gets a distinct color. When you have 50+ segments on a timeline, color-coded labels are essential for quickly seeing the structure of the recording — and for spotting mistakes.

### Undo and Edit
You can adjust segment boundaries by dragging endpoints. You can change a class label. You can delete a segment. The tool isn't write-only — annotators inevitably need to refine their work.

## Edge Cases I Hit

A few things that came up that I had to handle:

### Frame Rate Drift
Video frame rate isn't perfectly constant, and sensor sampling rate (52.63 Hz, not a clean number) doesn't align with typical video frame rates (30 fps, 60 fps). I had to handle interpolation between video frames and sensor samples carefully so the visual sync didn't drift over a long recording.

### Multi-Recording Sessions
A single dataset session might span several files — different swimmers, different strokes, different days. The tool needs to keep track of which annotations belong to which recording without mixing them up.

### Boundary Events
Some events (like wall touches) are essentially instantaneous — a single sample. Others (like full freestyle stroke cycles) span 50+ samples. The tool handles both gracefully — segments can be a single sample or hundreds.

## Generalizability

Although built for swimming, the tool works for:
- Any wearable sensor labeling project (running, cycling, strength training)
- Sign language IMU/EMG data
- Animal motion analysis (vet research, behavior studies)
- Industrial machine telemetry vs. video records
- Anything where you have time-series data + ground-truth video

The fundamental workflow — segment + label + class — transfers cleanly.

## Lessons Learned Building It

Building user-facing tools forces clarity in ways that pure ML code doesn't:

- **UX matters as much as correctness.** A correct labeling tool that's annoying to use will get used wrong.
- **Save state aggressively.** Annotators will close their browser. Their work needs to survive.
- **Color and visual feedback are essential.** Time-series traces are abstract; humans need anchors.
- **Don't over-engineer.** I could have built a database backend, multi-user auth, role permissions, audit logs. None of that was needed for the actual use case.

## Keywords

annotation workflow, sensor labeling, video synchronization, multi-channel display, time-series annotation, swimming labeling, IMU annotation, ground truth creation, dataset construction, single-user tool, CSV export, JSON persistence, segment editing, class coloring, frame rate drift, generalizable workflow
