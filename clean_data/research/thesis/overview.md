# Thesis Overview

## Summary

My master's thesis is titled "Multi-Task Deep Learning Approach for Segmenting and Classifying Competitive Swimming Activities Using a Single IMU." I'm the primary and sole author. It was completed in Summer 2025 at the University of South Carolina under research advisor Professor Homayoun Valafar, and it's published open-access in USC's Scholar Commons.

In short — I built a deep learning pipeline that takes raw motion data from a single wrist-worn smartwatch and figures out what a swimmer is doing in the pool. It can tell you which stroke they're swimming, when they're turning, when they're pushing off the wall, and how many strokes and underwater kicks they took. All from one sensor.

## Why I Did It

Competitive swimming analysis today is stuck in a frustrating place. Coaches still rely on manual video review, expensive pool-embedded timing systems, or pure observation to track split times, stroke counts, and effort. That works fine for a single elite athlete with a full coaching staff, but it doesn't scale. You can't monitor a whole team in real time, you can't get day-to-day workout insights, and most of those tools cost a fortune.

A wrist-worn IMU — basically what's already in any modern smartwatch — could solve this. The hardware is cheap, athletes already wear them, and the sensor data is rich. The problem is that nobody had built an end-to-end solution that could simultaneously detect lap boundaries, classify stroke cycles, and count strokes and kicks across all four competitive strokes. That's the gap I wanted to close.

## What I Built

I adapted the MTHARS (Multi-Task Human Activity Recognition and Segmentation) architecture from Duan et al. and tuned it specifically for swimming. The pipeline does four things at once:
- **Stroke classification** — butterfly, backstroke, breaststroke, freestyle
- **Lap segmentation** — detecting turns, push-offs, wall touches
- **Stroke count estimation**
- **Underwater kick count estimation**

It runs on data from a single smartwatch on the left wrist. No multi-sensor body suit. No video. Just one device.

## Contribution

The contribution is twofold. First, I demonstrated that one wrist-mounted IMU is enough to do all four tasks at once with respectable accuracy — something nobody had shown end-to-end. Second, I systematically tuned every key hyperparameter (IoU threshold, hard negative mining ratio, loss weights, scale factors, sensor modality) so future researchers can pick up the work and not have to re-do that grid search from scratch.

## Results in One Line

Leave-one-subject-out validation: micro-F₁ of 0.7405 with accelerometer-only, jumping to 0.7709 when I added gyroscope data. Macro-F₁ went from 0.5894 to 0.6565 with the gyroscope. Stroke count MAE around 3.5, kick count MAE around 4.2.

## Where to Find It

- Google Scholar: https://scholar.google.com/citations?view_op=view_citation&hl=en&user=6T9vxTcAAAAJ&citation_for_view=6T9vxTcAAAAJ:u5HHmVD_uO8C
- Citation: Shperkin, M. (2025). *Multi-Task Deep Learning Approach for Segmenting and Classifying Competitive Swimming Activities Using a Single IMU.* Master's thesis, University of South Carolina.

## Committee

- Homayoun Valafar — Major Professor (research advisor)
- Ramtin Zand — Examination Chair
- Vignesh Narayanan — Committee Member
- Forest Agostinelli — Committee Member
- Marco Valtorta — Academic advisor

## Keywords

thesis, master's thesis, USC, University of South Carolina, deep learning, multi-task learning, MTHARS, IMU, inertial measurement unit, wearable sensors, competitive swimming, stroke classification, swimming activity recognition, segmentation, single sensor, smartwatch, accelerometer, gyroscope, leave-one-subject-out validation, Mark Shperkin, Homayoun Valafar, numpy, pandas
