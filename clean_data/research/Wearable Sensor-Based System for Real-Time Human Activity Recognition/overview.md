# Wearable Sensor-Based HAR Paper — Overview

## Summary

"Wearable Sensor-Based System for Real-Time Human Activity Recognition" is a paper I authored at the University of South Carolina. I'm the **sole author** — every aspect of the work, from sensor integration to ML model development, was done by me.

The paper has an unusual structure for academic work: it documents **a research pivot**. The original goal was a custom-built wearable motion-capture suit using 9-DOF IMU sensors. When that hardware approach failed due to noise and drift, I pivoted to implementing the **Spatio-Temporal Graph Convolutional Network (ST-GCN)** on a public benchmark dataset. The pivoted approach succeeded — achieving 87.6% classification accuracy on NTU RGB+D across 49 different activities.

I include the failed hardware attempt in the paper rather than hiding it. Honest research means documenting what didn't work too.

## The Two Halves of This Paper

### Part 1: The Hardware Attempt (Didn't Work)
Built a wearable system using:
- **9-DOF BNO055 sensors** (gyroscope + accelerometer + magnetometer)
- **Arduino MKR IMU** + **ESP32 boards** for data collection and wireless transmission
- Sensors strategically positioned at key joints (legs, arms, torso)

The plan was to capture detailed 3D motion data and use it to train an activity classifier. The reality:
- Sensor noise and drift accumulated rapidly
- Even with Extended Kalman Filter approaches and zero-velocity updates, drift remained unacceptably high
- Pose reconstructions were unstable and unusable for ML training

**Lesson learned**: Twice-integrating noisy accelerometer signals causes errors to accumulate exponentially. Wearable IMU-based 3D position tracking is fundamentally hard, and consumer-grade sensors aren't yet good enough for this without elaborate compensation.

### Part 2: The ST-GCN Pivot (Worked)
With hardware data ruled out, I shifted to:
- **NTU RGB+D dataset** — 56,880 RGB-D video samples, 60 action classes, 25 body joint coordinates per skeleton
- **ST-GCN architecture** — graph convolutional network operating on skeletal data
- Implementation in **PyTorch** with adaptive spatial graph convolutions and temporal convolutions

**Result**: 87.6% peak validation accuracy across 49 activity classes, demonstrating ST-GCN's capability for real-time HAR.

## Why ST-GCN

The architecture is specifically designed for skeleton-based action recognition. Its key innovations:
- **Adaptive graph convolutions** — combines fixed anatomical adjacency with learned and dynamic attention masks
- **Decoupled spatial-temporal streams** — process joint relationships within frames separately from temporal patterns across frames
- **Lightweight footprint** — fewer parameters and less compute than competing GCN methods

This makes ST-GCN viable for **edge-device deployment** — exactly the use case the original wearable system was meant to serve.

## Performance Numbers

| Metric | Value |
|--------|-------|
| Peak validation accuracy | 87.6% |
| NVIDIA Jetson Nano throughput (paper baseline) | 993 frames/sec |
| My measurement on NVIDIA RTX 4070 Super | 102.8 samples/sec, 0.0097s avg latency |
| My measurement on Intel i7-14700F | 6.8 samples/sec, 0.147s avg latency |

Edge-feasibility confirmed across hardware tiers.

## Code

GitHub repo: https://github.com/markshperkin/HAR-STGCN

## Why This Paper Matters

Beyond the technical results, this paper demonstrates:

1. **Honest research practice** — documenting failed approaches alongside successful ones
2. **Pivoting under constraint** — when the original plan fails, recognizing it and adapting
3. **Validating literature claims independently** — my 87.6% accuracy roughly matches published ST-GCN results, validating reproducibility
4. **Edge feasibility** — runtime measurements on actual hardware showing ST-GCN is deployable, not just a research curio

## Application Areas

The paper specifically calls out high-impact deployment domains for ST-GCN:

- **Medical monitoring** — distress-gesture detection in clinical and assisted-living environments
- **Security surveillance** — anomalous behavior detection in airports, stadiums, critical infrastructure
- **Sports performance analysis** — automated technique evaluation, skill validation in gymnastics/diving/dance
- **Industrial ergonomics** — workplace-motion analysis for safety

## Authorship Note

The paper's "Summary of Contributions" section is explicit:
> "All research, development, and implementation duties for this project were undertaken solely by Mark Shperkin, who managed every aspect — from system design and sensor integration to machine-learning model development and evaluation."

I take full responsibility for the project, including the parts that didn't work.

## Keywords

wearable sensor, human activity recognition, HAR, 9-DOF IMU, BNO055, Arduino MKR, ESP32, motion capture, sensor noise, drift, Extended Kalman Filter, EKF, ST-GCN, spatio-temporal graph convolutional network, NTU RGB+D, skeletal data, graph convolution, edge deployment, real-time inference, research pivot, USC, Mark Shperkin
