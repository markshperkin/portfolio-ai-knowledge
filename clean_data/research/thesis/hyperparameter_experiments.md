# Hyperparameter Tuning Experiments

## The Approach

I ran systematic tuning experiments — each experiment trained on **5 epochs** to keep the search tractable. After all parameters were chosen, the final model was trained for 50 epochs with the winning configuration.

Five-epoch training is short enough to evaluate dozens of configurations in a reasonable time, but long enough that the relative ranking of hyperparameter settings is stable. It's a common compromise in deep learning research.

## What I Tuned

Four hyperparameters, in order:

1. **IoU threshold (τ)** — for anchor-to-label assignment
2. **Hard negative ratio (R)** — for negative mining
3. **Loss weights (α, β)** — classification vs. localization balance
4. **Multi-scale generator scales (s)** — temporal scale set

Plus one final input study comparing accelerometer-only vs. accelerometer+gyroscope.

I treated each experiment as a one-at-a-time grid search, holding others at reasonable defaults while varying the parameter under study. This isn't a full grid search (which would be 10⁴+ combinations), but it's systematic enough to find good values.

## IoU Threshold Tuning

| τ | Mean IoU | Macro-F₁ | Micro-F₁ |
|---|----------|----------|----------|
| 0.3 | 0.5736 | 0.4998 | 0.6760 |
| **0.5** | **0.5603** | **0.5146** | **0.7064** |
| 0.7 | 0.5586 | 0.4746 | 0.7046 |

τ governs how stringent anchor-to-ground-truth matching is.
- **Lower τ** → more anchors assigned positive → noisy weak matches
- **Higher τ** → only strong overlaps used → reduced recall

τ = 0.5 won. Best macro-F₁, second-best mean IoU, decent micro-F₁. It also matches the SSD default for object detection.

## Hard Negative Mining Tuning

| R | Mean IoU | Macro-F₁ | Micro-F₁ |
|---|----------|----------|----------|
| 0.1 | 0.5662 | 0.5043 | 0.7121 |
| **0.4** | **0.5731** | **0.4974** | **0.7091** |
| 0.8 | 0.4148 | 0.5290 | 0.8458 |
| 1.5 | 0.1129 | 0.2173 | 0.9571 |

R is the negative-to-positive ratio. R=1.5 has the misleading-best micro-F₁ but disastrous mean IoU. R=0.4 gave the cleanest balance: best mean IoU and respectable F₁ scores.

Lesson: do not trust a single metric in isolation. R=1.5 would have looked amazing on the micro-F₁ leaderboard and shipped a broken model.

## Loss Weight Balancing

| α; β | Mean IoU | Macro-F₁ | Micro-F₁ |
|------|----------|----------|----------|
| α=1; β=1 | 0.5724 | 0.5127 | 0.7200 |
| α=2; β=1 | 0.5802 | 0.5126 | 0.7171 |
| α=3; β=1 | 0.5688 | 0.5397 | 0.7152 |
| **α=1; β=2** | **0.5715** | **0.5384** | **0.7248** |
| α=1; β=3 | 0.5583 | 0.5101 | 0.7164 |
| α=2; β=3 | 0.5725 | 0.5337 | 0.7239 |
| α=3; β=2 | 0.5744 | 0.5074 | 0.6978 |

α weights classification, β weights localization.
- α=1, β=2 won — slightly favoring localization
- This makes sense for swimming because precise boundaries matter for stroke and kick counting

The loss weights effect is more subtle than IoU threshold or R; differences across configurations are small (~0.02 F₁), but consistent.

## Scale Factor Tuning

| Scales s | Mean IoU | Macro-F₁ | Micro-F₁ |
|----------|----------|----------|----------|
| {0.3, 0.5} | 0.5042 | 0.5126 | 0.7332 |
| {0.3, 0.5, 0.8} | 0.5510 | 0.4855 | 0.7048 |
| {0.5, 1.5} | 0.5208 | 0.5310 | 0.7506 |
| {2, 3} | 0.5656 | 0.5079 | 0.6978 |
| **{2, 3, 4}** | **0.5498** | **0.5381** | **0.7559** |

Scales {2, 3, 4} won — the highest micro-F₁ and second-best macro-F₁.

Why larger scales worked: swimming activities span tens to hundreds of frames at 52.63 Hz. Stroke cycles are ~1-2 seconds (50-100 frames). Turns are ~2-3 seconds (100-150 frames). Fractional scales like {0.3, 0.5} produce window slices that are too short to give meaningful temporal context for these durations.

## Input Modality Study

The final experiment, with optimal hyperparameters fixed: **accelerometer-only vs. accelerometer + gyroscope**.

| Input | Mean IoU | Macro-F₁ | Micro-F₁ | Stroke MAE | Kick MAE |
|-------|----------|----------|----------|------------|----------|
| Accel | 0.5900 | 0.5894 | 0.7405 | 3.57 | 4.21 |
| Accel + Gyro | 0.5735 | 0.6565 | 0.7709 | 3.35 | 4.35 |

Adding the gyroscope:
- ✅ Improved macro-F₁ by 0.07 — meaningful
- ✅ Improved micro-F₁ by 0.03
- ✅ Slightly improved stroke-count MAE
- ❌ Slightly worse kick-count MAE
- ❌ Slightly worse mean IoU

Net assessment: gyroscope helps overall, particularly for the rare classes that pull macro-F₁ up. Mean IoU regression and the kick-count uptick are interesting but small. The gain is real, especially for under-represented activities.

## Per-Class F₁ with vs. without Gyroscope

| Class | Accel only | Accel + Gyro |
|-------|-----------|--------------|
| Butterfly | 0.946 | 0.957 |
| Backstroke | 0.966 | 0.946 |
| Breaststroke | 0.833 | 0.864 |
| Freestyle | 0.878 | 0.882 |
| Underwater kick | 0.762 | 0.797 |
| **Underwater glide** | **0.156** | **0.324** |
| **Push-off** | **0.062** | **0.455** |
| Turn | 0.500 | 0.606 |
| Wall touch | 0.200 | 0.077 |

The really interesting story is in the rare classes. Push-off F₁ jumped from 0.062 to 0.455 with gyroscope — that's huge. Underwater glide doubled. Turn went from 0.5 to 0.6.

Wall touch went down — but it's the rarest class with very few samples, so this might be noise.

The takeaway: **gyroscope data is most valuable for classes with subtle or sparse motion signatures** (push-offs, glides, turns). For high-velocity rich-signal strokes, the accelerometer alone already does well.

## What I'd Do Differently

If I were starting fresh:
- I'd run the experiments more iteratively — re-tune τ and R after picking scales, since the optimal can shift
- I'd report standard deviations (these are single-run numbers, so some variation is hidden)
- I'd add a learning-rate experiment — that one I didn't tune

## Keywords

hyperparameter tuning, grid search, IoU threshold, hard negative mining ratio, loss weight balancing, scale factor, multi-scale generator, input modality study, accelerometer vs gyroscope, ablation, sensitivity analysis, single-metric trap, per-class F1, rare class detection
