# Conclusion & Future Work

## What This Project Demonstrated

This research started with one ambition (build a wearable motion-capture suit) and finished with another (validate ST-GCN for edge-deployable HAR). The pivot was forced by hardware reality — but it produced a useful result anyway.

### The Two Halves of the Story

**The hardware approach didn't work.** Two-stage Kalman filter applied to dual IMU streams, and an extended Kalman filter approach for leg kinematics — both failed to produce reliable position estimates. This was due to:
- High noise levels in the acquired IMU measurements
- Ambiguities and missing details in the published methodologies
- Fundamental issues with double-integrating noisy accelerometer signals

**The ML pivot worked.** The novel skeleton-based human action recognition architecture (ST-GCN) successfully captured joint dependencies directly from graph-structured data. The model achieved:
- Competitive accuracy (87.6%) against state-of-the-art baselines
- Lightweight footprint suitable for edge deployment
- Lower memory requirements than comparable methods
- Lower computational resources
- No extensive preprocessing overhead

These findings emphasize the **promise of graph-based neural networks for efficient, on-device biomechanical analysis**.

## Future Work — Application Directions

The ST-GCN architecture has several exciting extension paths.

### Medical Domain
Real-time patient monitoring in clinical and assisted-living settings:
- **Fall detection** — sudden, abnormal motion patterns trigger alerts
- **Distress gesture detection** — elderly or impaired patients signaling for help
- **Behavioral monitoring** — gait deterioration, abnormal movement patterns indicating health changes
- **Automatic caregiver alerts** — closing the loop from detection to response

This is genuinely valuable. Skeleton-based monitoring is privacy-preserving (no faces, no raw video) which makes it suitable for sensitive healthcare environments where camera surveillance would be objectionable.

### Security
Deploy ST-GCN in high-security environments:
- **Airports** — anomalous behavior detection in passenger flows
- **Stadiums** — crowd behavior monitoring, threat identification
- **Border checkpoints** — flagging unusual movement patterns
- **Critical infrastructure** — perimeter and interior monitoring

The proactive threat-interception use case is real but ethically loaded — it requires careful thought about false-positive rates, civil liberties, and oversight. The technical capability exists; how it's deployed matters.

### Sports and Performance Arts
ST-GCN's powerful spatial-temporal skeleton encoding lends itself to richer analytics across:

- **Gymnastics** — automatic skill validation, form scoring
- **Diving** — entry quality, rotation count, position assessment
- **Dance** — choreography analysis, technique feedback
- **Olympic-style judging** — augmenting or partially replacing human judges with consistent, automated evaluation

Imagine training feedback that's as detailed as a coach's eye but available 24/7 and consistent across all athletes. That's the vision.

### Industrial and Ergonomics
Beyond performance and safety:
- **Worker safety** — detect dangerous postures or motions in factories, warehouses
- **Ergonomic monitoring** — identify repetitive-strain risk patterns in manual labor
- **Process optimization** — analyze actual worker movements vs. designed workflows
- **Training validation** — confirm new employees are performing tasks correctly

By **fine-tuning to diverse joint-motion patterns**, ST-GCN can serve as a versatile skeleton-based analytics engine across many domains.

## Why I Believe in This Approach

A few reasons why ST-GCN-style architectures matter:

1. **Privacy-friendly** — skeleton data isn't visually identifying
2. **Lighting-invariant** — works in any visibility, including low-light medical settings
3. **Cross-domain transferable** — same architecture works for medical, sports, security
4. **Edge-deployable** — runs on cheap hardware
5. **Interpretable** — joint-level features are inherently meaningful

These properties make graph-based skeleton models genuinely viable for real-world deployment, not just academic benchmarks.

## What I'd Do Next If I Continued

If I were to extend this project:

### Short-term
- **Better data augmentation** — synthetic skeleton perturbations to improve robustness
- **Cross-dataset evaluation** — train on NTU, test on Kinetics-Skeleton
- **Quantization** — INT8 inference for even lower latency
- **Ablation study** — systematically remove components (Bₖ, Cₖ, residuals) to characterize their individual contributions

### Medium-term
- **Online learning** — adapt the model to a specific user's movement patterns
- **Few-shot novel-class detection** — recognize new actions from a few examples without retraining
- **Multi-modal fusion** — combine skeleton with RGB or audio for higher accuracy

### Long-term
- **Revisit wearable hardware** — with the lessons from this project, attempt a more focused IMU setup (single-sensor, no 3D position reconstruction) — which is essentially what my master's thesis ended up doing
- **Real-time continuous classification** — stream-based ST-GCN processing rather than fixed-window
- **Personalized federated training** — privacy-preserving model updates across distributed users

## Personal Reflection

This was a hard project. The hardware part was painful — weeks of debugging IMU drift, EKF tuning, calibration issues, none of which produced a working system. The temptation to brute-force through with worse data was real.

The pivot to ST-GCN was the right call. Sometimes the most productive thing you can do is recognize that your current path isn't working and find a different path that delivers the same value through different means.

The pivoted project produced:
- A working ST-GCN implementation
- Validated accuracy numbers
- Hardware benchmarks for edge deployment
- A documented failure narrative that could save someone else months

That's a useful contribution, even if it wasn't the contribution I originally set out to make.

## Authorship Note

The paper's contributions section is explicit:
> "All research, development, and implementation duties for this project were undertaken solely by Mark Shperkin, who managed every aspect — from system design and sensor integration to machine-learning model development and evaluation."

I take full responsibility for the project, including its failures. The lessons learned from this work directly informed my master's thesis on swimming activity recognition, which took the smarter approach of using a single wrist-worn IMU and skipping the 3D position reconstruction problem entirely.

## Keywords

conclusion, future work, hardware failure, ML pivot, ST-GCN deployment, medical monitoring, fall detection, distress gesture, security surveillance, threat detection, sports analytics, automated judging, industrial ergonomics, edge AI, privacy-preserving HAR, skeleton-based analytics, IoMT, biomechanical analysis, lessons learned
