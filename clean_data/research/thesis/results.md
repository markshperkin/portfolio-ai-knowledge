# Final Results

## Headline Numbers

In leave-one-subject-out validation:

**Accelerometer only:**
- Micro-F₁: **0.7405**
- Macro-F₁: **0.5894**
- Mean IoU: 0.5900
- Stroke-count MAE: 3.57
- Kick-count MAE: 4.21

**Accelerometer + Gyroscope:**
- Micro-F₁: **0.7709**
- Macro-F₁: **0.6565**
- Mean IoU: 0.5735
- Stroke-count MAE: 3.35
- Kick-count MAE: 4.35

The gyroscope-augmented model is the better one overall.

## What These Numbers Mean

Translating from F₁ scores to "what can this actually do":

- **77% F₁ overall.** That's good enough that, in a typical 100-yard swim set, the model gets the right activity for roughly three-quarters of detected events.
- **65% macro-F₁.** This is the more honest number — it weighs all classes equally, including the rare ones. 0.65 is moderate; the rare classes (turns, push-offs, wall touches) are still pulling the average down.
- **Stroke-count MAE around 3.4** per 100-yard set. Most swims have 30-60 strokes, so this is roughly a 10% error on stroke counts.
- **Kick-count MAE around 4.2** per 100-yard set. Underwater kicks vary more across athletes, so the error is higher.

For everyday training feedback purposes — "approximately how many strokes did you take, and what stroke were you swimming when?" — this is genuinely useful. For elite competitive analysis where every stroke matters, it's not yet there.

## Per-Class Performance Breakdown

The accelerometer + gyroscope model:

| Class | F₁ | Comment |
|-------|-----|---------|
| Butterfly | 0.957 | Excellent |
| Backstroke | 0.946 | Excellent |
| Breaststroke | 0.864 | Strong |
| Freestyle | 0.882 | Strong |
| Underwater kick | 0.797 | Solid |
| Underwater glide | 0.324 | Weak |
| Push-off | 0.455 | Moderate |
| Turn | 0.606 | Moderate |
| Wall touch | 0.077 | Poor |

The classes split clearly into two groups:

**Rich signal, frequent → strong performance:**
- Butterfly, backstroke, breaststroke, freestyle (full stroke cycles)
- Underwater kick (hundreds of training samples)

**Sparse signal or rare → weaker performance:**
- Underwater glide, push-off, turn (sparse, ambiguous signals)
- Wall touch (only ~50 training samples; right-hand touches don't register on the left-wrist sensor)

This is a class-imbalance and modality story. The architecture works; the dataset has known limitations on rare events.

## Confusion Matrix Insights

The confusion matrices (Figures 5.1 and 5.2 in the thesis) show:
- Most confusion is between similar activities (butterfly ↔ breaststroke; turn ↔ push-off)
- Accelerometer-only model has more cross-class bleed for the rare events
- Gyroscope reduces several specific confusions, especially turn vs. underwater glide

## Training Convergence

Training loss curves (Figure 5.3) showed steady convergence over 50 epochs for both modalities. No signs of overfitting at 50 epochs. The step-decay LR drop at epoch 30 produced a clear loss reduction without instability.

Validation accuracy and IoU curves (Figure 5.4) tracked training closely, suggesting the model generalized reasonably well within the LOSO setting.

## Comparison to Baselines

When evaluated **solely on stroke classification and underwater-kick detection**, my accelerometer-only model performs **on par with specialized pipelines** focused exclusively on those tasks (e.g., Delhaye et al., Zhang et al., Chen and Hu).

The added value of my pipeline is doing all four tasks **simultaneously** with a **single sensor** — counting strokes and kicks while also segmenting laps and turns. No prior work had demonstrated this combination on a single wrist-worn IMU.

## What's Honest About These Numbers

A few things worth flagging:

1. **Single-run results.** I didn't run multiple seeds and report variance. There's likely 1-2% variation across runs.
2. **N=11 swimmers.** That's a small dataset. Class imbalance for rare events is severe, and the model has limited generalization data.
3. **Single device (Tic Watch Pro 5).** Cross-device generalization (Apple Watch, Garmin, Polar) wasn't tested.
4. **Held-out subject = the author.** I served as the LOSO test subject, which is a non-standard methodological choice and could introduce subtle bias.
5. **Wall-touch results are unreliable** for the reasons noted (~50 samples; right-hand touches invisible to left-wrist sensor).

I'm transparent about these limitations because pretending they don't exist would be intellectually dishonest. The work is a meaningful step forward; it's not a finished product.

## Keywords

results, final results, leave-one-subject-out, LOSO validation, micro F1, macro F1, mean IoU, stroke count MAE, kick count MAE, per-class F1, confusion matrix, training convergence, baseline comparison, limitations, single-IMU swimming, accelerometer gyroscope, MTHARS results
