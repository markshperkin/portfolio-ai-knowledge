# IoU & Anchor-to-Label Assignment

## The Bookkeeping Problem

In an anchor-based detector, you generate hundreds of candidate windows per training sample, but only a handful of them are real activities. So you need a rule for deciding:

- Which anchors are "positive" (matched to a real ground-truth segment)?
- Which anchors are "negative" (don't correspond to anything)?
- For positive anchors, what offset corrections should the network learn?

This is the assignment problem. Solving it cleanly is what makes anchor-based detection work.

## Intersection-over-Union (IoU) on a 1D Timeline

The IoU metric (also called the Jaccard index) measures the overlap between a predicted window and a ground-truth segment. In 2D object detection it's bounding-box overlap; here it's temporal interval overlap.

For a predicted window `W = (wₓ, wₗ)` and a ground-truth segment `T = (tₓ, tₗ)`:

**Endpoints:**
- `wₛₜₐᵣₜ = wₓ - wₗ/2`, `wₑₙd = wₓ + wₗ/2`
- `tₛₜₐᵣₜ = tₓ - tₗ/2`, `tₑₙd = tₓ + tₗ/2`

**Intersection:**
`I = max(0, min(wₑₙd, tₑₙd) - max(wₛₜₐᵣₜ, tₛₜₐᵣₜ))`

**Union:**
`U = (wₑₙd - wₛₜₐᵣₜ) + (tₑₙd - tₛₜₐᵣₜ)`

**IoU:**
`IoU(W, T) = I / U`

IoU ranges from 0 (no overlap) to 1 (perfect alignment). This scalar score is used both during training (for anchor-to-label assignment) and at inference time (for non-maximum suppression).

## Two-Stage Assignment

The assign-windows-to-labels routine implements an SSD-style two-stage matching procedure between anchors `{Wᵢ}` and ground-truth segments `{Tⱼ}`.

### Step 1: Compute the IoU Matrix

`M ∈ ℝ^(nₐ × nᵦ)` where `Mᵢⱼ = IoU(Wᵢ, Tⱼ)`. This gives the temporal overlap between every anchor and every segment.

### Stage 1: One Anchor Per Segment (Mandatory)

Each ground-truth segment `Tⱼ` is paired with the **single anchor that maximizes** `Mᵢⱼ`. This guarantees that every real segment has at least one anchor matched to it — exactly one positive per segment, no orphans.

### Stage 2: Threshold-Based Additional Matches

For all remaining anchor-segment pairs, greedily match any pair whose IoU exceeds threshold `τ` — a tunable hyperparameter. This adds additional positives that have substantial overlap with a ground-truth segment.

Anchors not matched in either stage are assigned to the **background class**.

### Why Two Stages?

Stage 1 ensures recall — even if the threshold is high, every segment gets at least one matched anchor.

Stage 2 ensures sufficient training signal — high-IoU anchors are valuable training examples and shouldn't be wasted as background.

## Regression Targets

For every positive-matched anchor, we compute regression targets `Δx` and `Δl` that the segmentation head will learn to predict:

- `Δx = (tₓ - wₓ) / wₗ` — normalized center offset
- `Δl = ln(tₗ / wₗ)` — log-scale length ratio

`(wₓ, wₗ)` is the matched anchor's center and duration; `(tₓ, tₗ)` is the corresponding ground-truth segment.

The normalization by `wₗ` for `Δx` and the log scale for `Δl` are intentional. They produce regression targets in a roughly unit-scale range, which is much friendlier for the smooth-L1 loss to optimize than raw pixel/sample-space coordinates.

## What This Produces

The assignment procedure yields, for every anchor:
- A class label (one of the activity classes, or background)
- For positive anchors: offset targets `(Δx, Δl)` for the segmentation head

These per-anchor labels and targets become the supervisory signal for the joint classification + segmentation losses.

## IoU Threshold Tuning

I systematically tuned `τ` to find the right balance:

| τ | Mean IoU | Macro-F₁ | Micro-F₁ |
|---|----------|----------|----------|
| 0.3 | 0.5736 | 0.4998 | 0.6760 |
| **0.5** | **0.5603** | **0.5146** | **0.7064** |
| 0.7 | 0.5586 | 0.4746 | 0.7046 |

`τ = 0.5` won. Lower threshold (0.3) admits weaker matches that introduce noise; higher threshold (0.7) is stricter and starves the model of training signal. 0.5 is a balance — and it's also the SSD default, which is reassuring.

## Lessons

A few practical things I learned implementing this:

- **Stage 1 is non-negotiable.** Skipping it (just using thresholding) leaves segments with no matched anchor when their IoU is low — they vanish from the training signal entirely.
- **Log-scale length targets matter.** I tried linear length targets early on and the regression head was much harder to train.
- **Anchor density matters.** If anchors are too sparse, even Stage 1 might match low-IoU anchors that produce huge regression targets. The multi-scale generator's anchor density was carefully chosen to keep this from happening.

## Keywords

intersection over union, IoU, Jaccard index, anchor assignment, two-stage matching, SSD style, ground-truth matching, regression targets, delta x, delta l, normalized offset, log-scale length, IoU threshold, tau, hyperparameter tuning, positive anchor, negative anchor, background class, anchor-based training
