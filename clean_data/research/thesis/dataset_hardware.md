# Dataset: Hardware Configuration

## The Sensor

I used a single wrist-worn smartwatch — specifically the **Tic Watch Pro 5**. One device per swimmer, mounted on the **left wrist**, just proximal to the distal wrist crease. That positioning was deliberate — putting the watch right above the wrist crease minimizes movement artifacts that come from the watch sliding around when the wrist flexes hard during a stroke.

That's it. One device. No body suit. No multi-sensor rig. The whole thesis hinges on the question: **can one wrist-worn IMU do this job?**

## Why a Smartwatch

The choice was intentional. Pretty much every competitive swimmer already wears a smartwatch — Apple Watch, Garmin, Polar, etc. If the research demonstrates feasibility on consumer-grade smartwatch hardware, the path to real-world deployment is dramatically shorter. You don't need to convince a swim team to wear specialty gear; you just leverage what they already use.

The Tic Watch Pro 5 specifically was chosen because it gave me programmatic access to the raw triaxial accelerometer and gyroscope streams at a clean sampling rate.

## What Was Recorded

Two synchronized streams from the same device:

- **Triaxial accelerometer** (x, y, z) — captures linear acceleration in three axes
- **Triaxial gyroscope** (x, y, z) — captures angular velocity in three axes

Sampling rate: **52.63 Hz**. That's the native rate the watch was streaming at.

Both streams were synchronized with **video recording**, which I used for manual annotations later. Without video ground-truth, there's no way to label segment boundaries accurately.

## Why Left Wrist Specifically

Because most swimmers prefer their right hand, and putting the watch on the non-dominant wrist gave me a few advantages:
- Less interference with the swimmer's natural feel for the water
- More consistent positioning across athletes (almost everyone could tolerate it on the left)
- Cleaner signal because the dominant hand does more of the high-velocity stroke work

The trade-off is that asynchronous strokes (freestyle, backstroke) had to be defined relative to the left-hand motion, which adds variability when athletes have unusual lead-hand preferences. I document this in the labeling section.

## Sampling Rate Notes

52.63 Hz isn't a standard nice round number — it's just whatever the watch's API was producing. After preprocessing, I down-sampled the labels to match the network's feature-level resolution by an integer reduction factor of three. The model effectively operates at ~17.5 Hz feature rate but the input data is at the native ~52.63 Hz.

## Keywords

hardware, sensor configuration, Tic Watch Pro 5, smartwatch, IMU, inertial measurement unit, triaxial accelerometer, triaxial gyroscope, 52.63 Hz, sampling rate, wrist-worn, left wrist, single sensor, video synchronization, sensor placement, wearable hardware, consumer-grade hardware
