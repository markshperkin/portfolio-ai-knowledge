# Classification & Segmentation Heads

## The Two-Head Design

After the Multi-Scale Window Generator produces the unified feature map `M`, two parallel heads operate on it:

- **Classification head** — what activity is this?
- **Segmentation head** — where exactly does it start and end?

Both heads use simple pointwise (1×1) convolutional layers. The simplicity is intentional — most of the representational power lives in the backbone and the multi-scale feature aggregation. The heads just need to project the rich feature map into the right output formats.

## Classification Head

### What It Does
The classification head transforms the multi-scale feature representation at each time step into a vector of scores ("logits") for each activity category plus background.

### Implementation
- Pointwise (1×1) convolution
- Output dimension: `K + 1` (where `K` is the number of activity classes; +1 for background)
- Logits are passed through a SoftMax to produce confidence scores

### Interpretation
The output at each position is a probability distribution over all classes. These scores are interpreted as the probability that each candidate window (anchor) at that position contains a given activity.

### At Inference Time
The confidence scores are combined with the boundary adjustments from the segmentation head and fed into non-maximum suppression. NMS keeps only the most reliable, non-redundant segments — that's how we go from per-position scores to a clean final list of detected events.

## Segmentation Head

### What It Does
The segmentation head predicts how to **refine** each anchor window's temporal boundaries to better match the actual activity.

### Implementation
- Pointwise (1×1) convolutional layer operating on the same multi-scale feature map `M`
- Output: two regression values per anchor per position
  - **Δx** — temporal center offset (how far to shift the anchor's midpoint in time)
  - **Δl** — length adjustment factor (how much to scale the anchor's duration)

### Why This Format
This parallels how object detectors regress bounding box offsets in computer vision. Predicting deltas is more stable than predicting absolute coordinates because the anchors already provide a reasonable starting guess; the head just learns small corrections.

### Refinement Math
For an anchor with center `wₓ` and length `wₗ`:
- Refined center = `wₓ + Δx · wₗ`
- Refined length = `wₗ · exp(Δl)`

Note the `exp(Δl)` form — using a log-scale length adjustment ensures positive durations and gives the network smoother gradients to work with.

## How They Cooperate

During training, both heads are supervised jointly through the multi-task loss (see the loss functions doc). The classification head learns to identify what activity is present; the segmentation head learns to localize it precisely.

During inference, the two outputs are combined per anchor:
1. Take each refined window from the segmentation head
2. Pair it with its classification confidence
3. Pass to non-maximum suppression
4. NMS retains only the most confident, non-overlapping segments

The final output is a list of `(start_time, end_time, class_label, confidence)` tuples — a clean, structured representation of detected swim activities.

## Why Pointwise Convs

The choice of 1×1 convolutions for both heads might look minimal, but it's deliberate:

- **Per-position independence** — each time position is processed independently, which makes sense because all the temporal context aggregation already happened in the backbone and the multi-scale generator
- **Efficiency** — 1×1 convs are essentially per-position MLPs, very cheap
- **Architectural symmetry** — both heads share the same form, making the multi-task loss balancing more interpretable

If I had used larger kernels here, I'd have been double-counting temporal context (which is already in the multi-scale features) and adding parameters that don't really help.

## Output Shape Summary

For a backbone output with `N` time positions:
- Classification head output: `(N, K+1)` logits
- Segmentation head output: `(N, 2)` regression values per anchor

Multiplied by the number of anchors per position from the multi-scale generator. After NMS, you typically end up with ~5-10 detected segments per 450-frame window.

## Keywords

classification head, segmentation head, pointwise convolution, 1x1 convolution, regression head, anchor refinement, delta x, delta l, temporal offset, length scaling, softmax, logits, multi-task heads, output decoding, anchor-based detection, MTHARS heads
