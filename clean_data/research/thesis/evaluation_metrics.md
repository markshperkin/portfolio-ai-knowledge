# Evaluation Metrics

## What I Measured

I evaluated each hyperparameter setting using three metrics that capture different aspects of performance:

- **Mean IoU** — how precisely segments are localized
- **Micro-F₁** — overall detection performance, weighted by class frequency
- **Macro-F₁** — balanced detection performance, treating all classes equally

You need all three. Any one alone is misleading.

## Segment-Level Detection Definitions

To compute precision and recall, I need to define true positives, false positives, and false negatives at the **segment level** (not the frame level — segment-level metrics make sense for an anchor-based detector that produces bounded events).

For each class `c`:

### True Positive (TP)
A proposed segment whose temporal IoU with a ground-truth segment exceeds zero **and** whose predicted class matches the ground-truth class.

So a partial-overlap, correct-class prediction counts as a TP. This is more lenient than typical detection metrics (which often require IoU > 0.5), but it's appropriate for swimming where exact boundary detection isn't always realistic given inter-swimmer signal variability.

### False Positive (FP)
A proposed segment that either:
- (i) overlaps a ground-truth segment (IoU > 0) but is assigned the **wrong class**, or
- (ii) does not overlap any ground-truth segment (IoU = 0) — i.e., a phantom prediction

### False Negative (FN)
A ground-truth segment that either:
- (i) overlaps a proposal of the wrong class, or
- (ii) is not overlapped by any proposal at all

Note that case (i) of FP and case (i) of FN are the same event — a wrong-class detection — counted from both sides. That's intentional; it ensures both precision and recall reflect class confusion.

## Per-Class Precision and Recall

Per-class precision: `Pᶜ = TPᶜ / (TPᶜ + FPᶜ)`
Per-class recall: `Rᶜ = TPᶜ / (TPᶜ + FNᶜ)`

Per-class F₁: `F₁,c = 2 · (Pᶜ · Rᶜ) / (Pᶜ + Rᶜ)`

## Macro vs. Micro F₁

### Macro-F₁
Average per-class F₁ scores equally:

`Macro-F₁ = (1/C) · Σᶜ F₁,c`

This gives every class the same vote regardless of how often it occurs. Wall touches (rarest class, only ~50 training samples) contribute as much as butterflies (~317 training samples).

Macro-F₁ is the right metric when you care about handling **rare events well**. In swimming, wall touches and turns are rare but important — coaches care about lap times, which depend on accurately detecting them. So macro-F₁ matters.

### Micro-F₁
Aggregate TPs, FPs, and FNs across all classes, then compute:

`P_micro = Σᶜ TPᶜ / Σᶜ (TPᶜ + FPᶜ)`
`R_micro = Σᶜ TPᶜ / Σᶜ (TPᶜ + FNᶜ)`
`Micro-F₁ = 2 · (P_micro · R_micro) / (P_micro + R_micro)`

Micro-F₁ is dominated by the most common classes (underwater kicks, individual strokes). It reflects **overall detection performance** weighted by frequency.

## Why Track Both

The hard negative mining tuning experiment (Table 5.2) shows why this matters:

| R | Mean IoU | Macro-F₁ | Micro-F₁ |
|---|----------|----------|----------|
| 0.1 | 0.5662 | 0.5043 | 0.7121 |
| 0.4 | 0.5731 | 0.4974 | 0.7091 |
| 0.8 | 0.4148 | 0.5290 | 0.8458 |
| 1.5 | 0.1129 | 0.2173 | **0.9571** |

R=1.5 gives a "best-in-class" 0.9571 micro-F₁. Looks amazing. But the macro-F₁ collapses to 0.2173 and the mean IoU is a catastrophic 0.1129. What's actually happening: the model is over-predicting common classes and getting most positives right, but it's lost almost all sense of class balance and segment localization.

If I had only tracked micro-F₁, I would've shipped a broken model.

## Mean IoU

Tracks how precisely segments are localized when they're correctly classified. For all true positives, compute the IoU between the predicted segment and the matched ground-truth segment, then average.

Mean IoU = (1 / |TPs|) · Σ IoU(pred, gt)

Mean IoU complements F₁ scores. F₁ tells you "did we detect it?", mean IoU tells you "did we detect it precisely?"

## What I Don't Use

Some metrics I deliberately skipped:
- **Frame-level accuracy** — too lenient for an anchor-based detector; doesn't reflect segment quality
- **mAP at various IoU thresholds** — common in COCO-style detection, but my IoU > 0 definition for TPs is more interpretable for swimming and matches the practical question of "did we count this stroke at all"
- **Confusion matrix only** — useful for diagnostics (and I include them in the thesis), but not as a primary metric

## Stroke and Kick Count Metrics

For the counting tasks specifically, I report **Mean Absolute Error (MAE)**:
- Stroke-count MAE: how far off the predicted stroke count is from the true count, averaged across sets
- Kick-count MAE: same for underwater kicks

Final accelerometer + gyroscope MAEs: 3.35 strokes per set, 4.35 kicks per set. Not bad, but a clear area for improvement.

## Keywords

evaluation metrics, F1 score, micro F1, macro F1, mean IoU, true positive, false positive, false negative, segment-level detection, precision, recall, class imbalance, MAE, stroke count, kick count, hyperparameter evaluation, metric selection, anchor-based detection metrics
