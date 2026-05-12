# Loss Functions

## The Multi-Task Loss

Training MTHARS requires balancing two objectives in a single backward pass:

1. **Classification** — predict the correct activity class for each anchor
2. **Localization** — refine each positive anchor's temporal boundaries

Each objective gets its own loss term, and they're combined into a single weighted sum. This is the "multi-task" in MTHARS.

## Localization Loss (Smooth L1)

### Definition
Let `P` be the set of indices for positive anchors. For each `i ∈ P`, the model predicts an offset vector `Δ̂ᵢ = (Δ̂x,i, Δ̂l,i)` and the ground truth is `Δᵢ = (Δx,i, Δl,i)`.

`L_loc = Σ(i ∈ P) SmoothL1(Δ̂ᵢ - Δᵢ)`

### Smooth L1 (Huber Loss)
Applied elementwise to the difference `d = Δ̂ - Δ`:

```
SmoothL1(d) = { 0.5 · d²,    if |d| < 1
              { |d| - 0.5,   otherwise
```

### Why Smooth L1 (not L2)
Pure L2 (MSE) is sensitive to outliers — a single bad prediction with large error can blow up the loss and the gradients. Smooth L1 behaves like L2 for small errors (smooth, well-behaved gradients) and like L1 for large errors (less sensitive to outliers, bounded gradient magnitude).

For regression tasks like bounding box / segment offset prediction, this is the right tradeoff. Object detection models (SSD, Faster R-CNN, etc.) use it for the same reason.

### Why Only Positive Anchors
Localization loss is computed only over **positive** anchors — the ones matched to real ground-truth segments. Background anchors don't have meaningful offset targets, so including them would just inject noise into the regression head.

## Classification Loss (Cross-Entropy)

### Definition
Let `A = P ∪ N_hard` be the set of anchors used for classification, where `N_hard` is the set of hard-mined negatives. `K` denotes the number of actual activity categories.

For each anchor `i ∈ A`, the ground-truth label is encoded as a one-hot vector:

`aᵢ = [aᵢ,0, ..., aᵢ,K]`

with exactly one entry equal to 1 (including class 0 for background). The model's predicted distribution is:

`âᵢ = [âᵢ,0, ..., âᵢ,K]`

obtained via SoftMax over the `K + 1` logits.

### The Loss
`L_conf = -Σ(i ∈ A) Σ(c=0 to K) aᵢ,c · log(âᵢ,c)`

Standard categorical cross-entropy, but applied only to the selected anchors `A` — positives and hard-mined negatives.

### Why This Anchor Subset
Including all anchors would push the loss toward a trivial "predict background everywhere" solution. Including only positives + hard negatives focuses the gradient signal where it matters: on examples that are either real activities or look enough like them to fool the model.

## Combined Loss

The two losses are combined via a weighted sum, normalized by the number of positives `N_pos = |P|`:

`L = (1 / N_pos) · (α · L_conf + β · L_loc)`

### The Normalization
Dividing by `N_pos` is important — it makes the loss magnitude roughly invariant to how many real activities happen to be in a given training batch. Without this, batches with many segments would dominate gradient updates.

### The Weights α and β
- `α` weights the classification loss
- `β` weights the localization loss

I tuned these systematically. From Table 5.3:

| α; β | Mean IoU | Macro-F₁ | Micro-F₁ |
|------|----------|----------|----------|
| α=1; β=1 | 0.5724 | 0.5127 | 0.7200 |
| α=2; β=1 | 0.5802 | 0.5126 | 0.7171 |
| α=3; β=1 | 0.5688 | 0.5397 | 0.7152 |
| **α=1; β=2** | **0.5715** | **0.5384** | **0.7248** |
| α=1; β=3 | 0.5583 | 0.5101 | 0.7164 |
| α=2; β=3 | 0.5725 | 0.5337 | 0.7239 |
| α=3; β=2 | 0.5744 | 0.5074 | 0.6978 |

I went with `α=1, β=2`. That weights localization slightly more than classification — which makes sense for swimming where precise boundary detection matters for stroke and kick counting (you need clean segments to count, not just roughly classified frames).

## What This All Trains

This multi-task loss trains the network simultaneously to:
- Classify each anchor correctly (real activity vs. background, and which class)
- Localize each positive anchor's temporal boundaries with high precision

Both objectives drive the same backbone, the same multi-scale features, and the same classification/segmentation heads. Joint training means the features that emerge are useful for both tasks — better than training two separate networks.

## Keywords

loss function, multi-task loss, smooth L1, Huber loss, cross-entropy loss, classification loss, localization loss, regression loss, alpha beta weighting, loss balancing, weighted sum, normalization, N_pos, gradient signal, joint optimization, MTHARS training, SSD loss, anchor-based loss
