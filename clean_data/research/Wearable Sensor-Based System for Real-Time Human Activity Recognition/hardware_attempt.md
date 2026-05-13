# The Wearable Hardware Attempt (and Why It Failed)

## What I Tried to Build

The original plan was a wearable motion-capture suit consisting of multiple **9-DOF IMU sensors** distributed across the body's key joints. Each sensor would stream:
- **Accelerometer** — linear acceleration in 3 axes
- **Gyroscope** — angular velocity in 3 axes
- **Magnetometer** — magnetic field heading in 3 axes

Combined, these provide enough information (in principle) to reconstruct each joint's orientation and position in 3D space.

## The Hardware

- **BNO055 sensor modules** — these are absolute orientation sensors that fuse the three sensor streams internally and output orientation as a quaternion
- **Arduino MKR IMU** boards — provided sensor interfaces and basic control
- **ESP32 boards** — for wireless transmission of sensor data to a host machine

The system was designed for real-time streaming so the user's pose could be visualized live and the data could feed into ML training.

## The Foundation in Literature

The approach was inspired by two key papers:

**Yadav and Bleakley** — proposed a novel two-stage Extended Kalman Filter (EKF) for position estimation using dual IMUs on a single rigid body:
- First stage: estimates orientation from gyroscope + accelerometer
- Second stage: refines position using fixed inter-sensor distance as a constraint
- Showed up to 30% improvement in position accuracy over dead reckoning

**Bennett et al.** — proposed a method to estimate human gait parameters and walking distance using a biomechanical model of the leg as a two-link manipulator:
- Gyroscopes on thigh and shin
- Forward kinematics + EKF tracking joint angles and displacement
- Achieved 7 cm RMSE and 97%+ walking distance accuracy

I tried to build on both — multiple IMUs at multiple joints, with EKF-based fusion and constraints from anatomical structure.

## What Went Wrong

Both EKF approaches suffer from a fundamental issue: **unbounded drift from accelerometer integration**.

To get position from acceleration, you have to integrate twice — once for velocity, once for displacement. Each integration step propagates noise. Small biases compound exponentially. Within seconds, position estimates drift unrecoverably.

Even with mitigation strategies:
- **Zero-velocity updates** — pin velocity to zero when the foot is stationary during walking, resetting accumulated error
- **Magnetometer-based heading corrections** — use the magnetic field to correct heading drift

residual bias and noise persisted. Overall drift remained unacceptably high.

## Why This Matters

The result wasn't just "less accurate than expected." Pose reconstructions were:
- **Unstable** — different runs of the same motion produced different reconstructed paths
- **Visually unreliable** — when you visualize the reconstructed skeleton, joints float to nonsensical positions within seconds
- **Not training-ready** — you can't train a classifier on data that's drifted; the network would learn the drift, not the activity

Without clean position estimates, the planned downstream pipeline collapsed. No usable dataset could be created from the suit. No real-time pose tracking was achievable.

## Lessons Learned

### 1. Twice Integration is Hard
Going from acceleration to position requires double integration. Every IMU has some bias, however small. After two integrations, that bias becomes a quadratic-growing error. This is mathematically unavoidable without external references.

### 2. Consumer-Grade IMUs Aren't Lab-Grade
The BNO055 is a great consumer sensor. It does what consumer applications need — orientation tracking for handheld devices, basic motion gestures. But for sustained 3D position tracking on a moving body, it's not enough. Lab-grade sensors with tighter calibration and lower noise characteristics would do much better — at 10-100x the cost.

### 3. EKF Implementation Details Matter
The literature describes EKF approaches with broad strokes. Reproducing them requires nailing dozens of small details:
- Tuning process and measurement noise covariances
- Initial state estimation
- Outlier handling
- Calibration sequences

Even with the literature in front of me, the gap between "described in a paper" and "running on my hardware" was enormous.

### 4. Multi-Sensor Constraints Don't Save You
Yadav and Bleakley's dual-IMU constraint helps because it gives you a second view of the same rigid body. On a human body, the rigid-body assumption breaks down — even within a single limb segment, soft tissue moves, sensors shift slightly, and the geometry isn't truly rigid.

### 5. Pivot Decisively When the Path is Blocked
After enough debugging, I had to recognize that this wasn't going to work in the project's timeframe. Pivoting to NTU RGB+D + ST-GCN was the right call. Sticking with the hardware approach for sunk-cost reasons would have wasted weeks more without producing results.

## Why I Documented the Failure

Most papers don't include their failed approaches. They write the success story as if it was the plan from day one. I included the hardware attempt because:
- **Future researchers benefit** from knowing this approach has issues
- **Honest research culture** requires reporting what didn't work, not just what did
- **Reproducibility matters** — if someone else tries to build a wearable IMU motion-capture suit, they should know the pitfalls

Hiding failures inflates the apparent ease of similar work and leads to repeated wasted effort across the community.

## What I'd Do Differently

If I were to revisit wearable HAR (which I might, in the swimming context for my thesis):
- Use a **smaller sensor set** — maybe just one wrist-worn IMU (which is what I ended up doing for my master's thesis)
- Avoid **3D position reconstruction** entirely — don't try to compute absolute coordinates; work in motion-pattern space
- Focus on **classification and segmentation** — patterns in raw IMU streams, not derived 3D pose
- Use **commercial smartwatches** rather than custom hardware — they're better-calibrated than DIY Arduino setups

That's exactly the trajectory my thesis ended up taking. The lessons from this paper directly informed that work.

## Keywords

hardware failure, wearable IMU, 9-DOF sensors, BNO055, Arduino MKR, ESP32, sensor noise, drift, double integration, Extended Kalman Filter, EKF, zero-velocity update, magnetometer correction, dead reckoning, position drift, two-stage EKF, biomechanical kinematics, research pivot, honest reporting, lessons learned, dual IMU constraint
