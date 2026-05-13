# Thesis Abstract

## The Abstract (As Written)

Competitive swimming performance analysis has traditionally relied on manual video review and multi-sensor systems, both of which are resource-intensive and impractical for everyday training use. This study investigates whether a single wrist-worn inertial measurement unit (IMU) can be used to automatically segment and classify swimming activities with high accuracy. We propose a multi-task deep learning pipeline based on the MTHARS (Multi-Task Human Activity Recognition and Segmentation) architecture introduced by Duan et al. to perform stroke classification, lap segmentation, stroke count estimation, and underwater kick count estimation.

Data were collected from eleven collegiate-level swimmers wearing left-wrist-mounted IMUs, each performing five 100-yard sets per stroke (butterfly, backstroke, breaststroke, freestyle, and individual medley) in a 25-yard pool. This pipeline delivers a reliable multi-metric evaluation while significantly reducing the complexity and cost of sensor setups.

In leave-one-subject-out validation, the accelerometer-only model achieved a micro-F₁ of 0.7405 (macro-F₁ 0.5894), which improved to 0.7709 (macro-F₁ 0.6565) when gyroscope data were added. This work contributes to the growing field of wearable-based athlete monitoring and has the potential to empower coaches and athletes with real-time, fine-grained performance feedback in competitive swimming using minimal hardware.

## Plain English Translation

If you don't speak academic, here's what that abstract is really saying:

Coaches still grade swimmers using video and stopwatches. That's slow and doesn't scale. I wanted to know if a single smartwatch on one wrist could do the same job — automatically — and how well.

I took eleven college swimmers, put a watch on their left wrist, and had each of them swim five sets of every stroke. Then I trained a multi-task deep learning model (MTHARS) to do four things from that one stream of motion data: classify the stroke, find lap transitions, count strokes, and count underwater kicks.

It worked. Using just the accelerometer, the model hit a micro-F₁ of 0.74. Adding the gyroscope pushed it to 0.77. That's good enough to be useful — but more importantly, it's a proof of concept that everyday wearable hardware can replace the expensive specialty rigs coaches currently rely on.

## Keywords

abstract, thesis summary, IMU, single sensor, multi-task deep learning, MTHARS, wrist-worn, swimming analysis, stroke classification, lap segmentation, stroke count, kick count, leave-one-subject-out, micro-F1, macro-F1, accelerometer, gyroscope, wearable athlete monitoring
