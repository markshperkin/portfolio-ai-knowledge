# Introduction & Problem Statement

## Why Sensor-Based Swimming Analysis Matters

Sensor-based activity recognition has matured a lot in the last decade. It's become a real, scalable, privacy-friendly alternative to camera-based methods. You don't need cameras everywhere; you just need a sensor on the body. That's been a huge win for fitness, healthcare, smart homes, all of it.

Competitive swimming, though, has been left behind. Coaches and analysts are still doing things the old way — they're using:
- Manual video review (slow, hard to scale)
- Expensive pool-embedded timing systems (only big programs can afford them)
- Coach-provided feedback (subjective, doesn't scale to whole teams)

These approaches are labor-intensive, non-portable, and impractical when you're trying to monitor multiple athletes at once. If you've ever sat on a pool deck trying to count strokes for ten swimmers in different lanes, you know the pain.

## The Promise and the Gap

Wrist-worn IMUs offer a way out. They're cheap, mobile, and athletes already wear them in the form of smartwatches. The hardware problem is solved.

The software problem isn't. To date, no study had demonstrated an end-to-end solution that could simultaneously:
1. Detect lap boundaries
2. Segment and classify individual stroke cycles
3. Count strokes
4. Count underwater kicks

People had done pieces of this. Lots of researchers had built stroke classifiers. Some had built lap detectors. But nobody had stitched it all together with a single sensor. That's the gap I went after.

## What I Set Out to Do

The objective of my research was to design and evaluate a multi-scale feature-extraction pipeline for single-IMU swimming data. I wanted to systematically tune the hyperparameters and figure out exactly what worked — not just claim "deep learning solves swimming" and move on.

The whole pipeline was developed and validated on a dataset I collected: eleven collegiate swimmers from USC, wrist-mounted IMUs (Tic Watch Pro 5), recording triaxial accelerometer and gyroscope data at 52.63 Hz, in a 25-yard pool.

The vision is concrete: leverage devices many athletes already wear (smartwatches), deliver data-driven insights into daily workouts, support performance improvement, and help prevent overtraining or injury — thereby raising the standard of competitive swimming overall.

## Why This Is Genuinely Hard

Wearable solutions face real technical hurdles, and I want to be honest about them:

- **Stroke cycles** are rich, high-frequency motion signals. They're actually easier than the rest.
- **Lap transitions** (turns, wall push-offs) are sparse, short, and vary wildly by stroke. They're the hard part.
- **Sensor noise** is real — water resistance, sensor drift, body rotation, and the watch shifting on the wrist all add noise.
- **Existing IMU approaches** typically either target a single task (just classification) or require multiple sensors on different body parts. That's user burden and system complexity I was actively trying to avoid.

What was missing was a lightweight, single-IMU solution that could simultaneously classify all swimming activities and count strokes and kicks across all competitive strokes with high accuracy. That's exactly what this thesis attempts.

## Keywords

introduction, problem statement, motivation, sensor-based activity recognition, IMU, wrist-worn, smartwatch, competitive swimming, stroke classification, lap detection, stroke counting, kick counting, single-sensor system, athlete monitoring, USC swimmers, Tic Watch Pro 5, 52.63 Hz, accelerometer, gyroscope, multi-scale feature extraction
