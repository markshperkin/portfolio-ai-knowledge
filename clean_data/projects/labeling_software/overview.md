# LabelingSoftware — Overview

## What It Is

A **web-based annotation tool** I built for labeling accelerometer and gyroscope time-series data with **video synchronization**. Originally developed for swimming motion analysis with USC's Division I Swim & Dive team, but the tool generalizes to any IMU sensor dataset that needs temporal labeling.

GitHub: https://github.com/markshperkin/LabelingSoftware

## Why I Built It

For my master's thesis on swimming activity recognition, I needed labeled IMU data — accelerometer and gyroscope streams aligned with what the swimmer was actually doing at each moment. There's no public underwater swimming IMU dataset, so I had to collect and annotate one myself.

Manual annotation of time-series sensor data is brutal. You're staring at squiggly lines trying to match them to events you saw on video. Existing tools either:
- Don't support video synchronization
- Don't handle multi-channel time-series cleanly
- Are research-grade scripts with no UI

I needed something faster and more usable, so I built it.

## What It Does

The tool addresses the labor-intensive task of manually annotating sensor streams by providing:

- **Intuitive segmentation interface** for creating class-specific time-series labels
- **Video synchronization** — frame-by-frame ground-truth alignment between sensor data and video footage
- **File-system based data management** within a structured `backend/data/` directory
- **CSV/JSON persistence** without traditional database dependencies (chosen for simplicity and portability)

Annotators can play the video, scrub through the sensor traces, and create labeled segments by dragging across the timeline. The video and sensor stream stay synchronized so you always know which frame of video corresponds to which sample of sensor data.

## Why This Matters

Without this tool, my thesis dataset wouldn't exist. Eleven swimmers, multiple strokes, hundreds of segments per athlete — that's thousands of annotations. Doing them in a spreadsheet or with Audacity-style audio tools would have taken months.

The tool also generalizes. Anyone working with IMU + video for human motion analysis can use it. That includes other swim researchers, fitness app builders, sports scientists, and anyone doing wearable-sensor data collection where ground truth comes from video.

## My Role

Sole developer. I designed the UX, picked the tech stack, built both the frontend and backend, and used it to label my own thesis dataset.

## Keywords

annotation tool, data labeling, IMU labeling, accelerometer labeling, gyroscope labeling, time-series annotation, video synchronization, ground truth labeling, swimming dataset, web-based tool, React, Python, Flask, JSON, CSV, frame-by-frame alignment, USC, master's thesis support tool
