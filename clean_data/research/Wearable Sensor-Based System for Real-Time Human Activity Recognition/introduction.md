# Introduction

## The Research Vision

This research originally aimed at building a wearable motion-capture system that would deliver real-time human activity classification — the kind of system that could one day be integrated into smart clothing, athletic gear, or medical-monitoring devices. The vision: an affordable, effective solution for biomechanical analysis that empowers athletes, coaches, and healthcare providers with precise, data-driven insights.

The proposed system used:
- A network of **9-DOF (nine-degree-of-freedom) absolute sensors** — gyroscopes, accelerometers, and magnetometers
- Sensors **strategically positioned at key joints** across the body (legs, arms, torso)
- **BNO055 sensor modules** interfaced through **Arduino MKR IMU** boards
- **ESP32 boards** for wireless data transmission

The goal was to collect detailed 3D motion data, reconstruct user pose in three dimensions, and use that data to train a classifier capable of distinguishing activities like walking, running, and jumping.

## Why Wearable IMUs in Principle

Inertial Measurement Units (IMUs) — combinations of accelerometers, gyroscopes, and magnetometers — provide a **compact, low-cost, portable solution** for capturing motion data without external reference systems. They enable continuous tracking of human pose and orientation, even in environments where optical systems (cameras, motion-capture rigs) are impractical:
- In-pool, underwater
- Outdoors, variable lighting
- Crowded spaces with occlusions
- Privacy-sensitive contexts (no video required)

These properties make IMU-based motion capture genuinely attractive for sports, healthcare, and HCI applications.

## Why Wearable IMUs in Practice (the Hard Truth)

The challenges:
- **Sensor noise** — every IMU has measurement noise that's hard to fully filter out
- **Sensor drift** — small bias errors accumulate over time, causing position estimates to drift wildly
- **Nonlinear human movement** — the dynamics aren't linear, requiring sophisticated estimation techniques

Sensor fusion algorithms like the **Extended Kalman Filter (EKF)** have improved reliability of IMU-based motion tracking by correcting noisy measurements and accommodating nonlinear dynamics. Recent studies have shown that strategically placed IMUs on the human body — particularly on key joints — can yield highly accurate estimations of joint angles, limb orientation, and displacement.

For example, dual-stage EKF models with novel sensor placement strategies have shown up to **30% improvement in position estimation** over traditional dead reckoning methods. This shows the importance of both algorithmic and hardware configuration in motion-capture systems.

## What Happened In My Experiments

In our experiments, **the prototype sensor network produced pose streams with excessive noise and drift**, rendering them unreliable for downstream model input. Even after implementing zero-velocity updates and magnetometer-based heading corrections, residual bias and noise persisted. Overall drift remained unacceptably high.

This wasn't a model-training problem. It was a sensor-data quality problem. You can't train a useful classifier on data that's drifted dozens of centimeters from ground truth within seconds of starting.

## The Pivot

Rather than continue iterating on hardware that wasn't working, I pivoted to:
- Using a **publicly available dataset** (NTU RGB+D)
- Implementing a **state-of-the-art ML architecture** (ST-GCN) for activity recognition
- Documenting the hardware failures honestly so future researchers can learn from them

## Activity Recognition with Machine Learning

In the realm of activity recognition, machine learning techniques have become increasingly essential. With the proliferation of data-driven approaches, frameworks like **spatial-temporal graph convolutional networks (ST-GCNs)** have demonstrated remarkable performance in classifying human actions from skeletal and joint data — particularly in healthcare and sports applications.

These models leverage:
- **Spatial relationships** between joints (anatomical structure)
- **Temporal dynamics** (joint movement across time)

to learn robust representations of human movement.

The capability to identify movements like walking, running, or jumping in real time enables:
- **Athletic performance monitoring**
- **Injury prevention**
- **Personalized training program design**

## Pivoted Goal

With hardware ruled out, the project's revised goal was to:
1. Implement ST-GCN from the literature
2. Train and validate on NTU RGB+D
3. Demonstrate edge-deployment feasibility through latency measurements

This delivers value despite the hardware failure: a working, validated ST-GCN implementation that's deployable on edge devices, with clear performance characteristics. The ML side delivered what the hardware couldn't.

## What This Paper Contributes

The honest contribution mix:

- **Documented hardware failure** — what doesn't work and why, useful for anyone considering similar wearable IMU projects
- **ST-GCN implementation** validated against published results (87.6% vs. paper's 92.2% on NTU RGB+D)
- **Edge-device latency benchmarks** on real hardware (RTX 4070 Super and i7-14700F) — beyond what the original ST-GCN paper measured
- **Application analysis** — concrete deployment scenarios in medical, security, sports

Even when the original goal fails, well-documented work has value. That's the spirit of this paper.

## Keywords

introduction, motion capture, wearable sensors, 9-DOF IMU, BNO055, Arduino, ESP32, joint sensors, motion tracking, sensor noise, drift, Extended Kalman Filter, EKF, dead reckoning, activity recognition, ST-GCN, NTU RGB+D, research pivot, hardware failure, ML alternative, edge deployment
