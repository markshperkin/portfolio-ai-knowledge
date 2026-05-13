# Multi-Scale Window Generator

## The Problem It Solves

After the CNN backbone produces a feature map `M` with 256 channels at `N` temporal positions, the next problem is figuring out **how to query that feature map for activities of varying durations**.

An underwater kick lasts ~30 frames. A backstroke lap lasts ~140 frames. A wall touch is ~40 frames. If I just take a fixed-size temporal window centered on each position, I'm picking one duration and biasing the model toward activities of that scale. That's the trap the Multi-Scale Window Generator is designed to avoid.

## The Idea (From Duan et al.)

Duan et al. proposed a unified anchor-based mechanism: at each feature-sequence position, the network generates **two windows per scale** `s ∈ {s₁, ..., sₘ}`. The window lengths are calculated as:

- `L₁ = ⌊N · √s⌋`
- `L₂ = ⌊N / √s⌋`

Where `N` is the backbone's output length.

These windows act as **temporal anchors** — analogous to the bounding boxes in object detection. They cover both short-duration impulses and long-duration activities at the same time. By generating multiple per scale and using multiple scales, the network has a rich set of pre-defined "candidate windows" it can refine into actual segment predictions.

## The Pipeline

For each of the `N` time positions in the backbone's feature map:

1. For each scale `s`, compute window lengths `L₁` and `L₂`
2. Extract those windows from the feature map (slice them out)
3. **Zero-pad** any slices that extend beyond the data boundaries (so windows near the start or end of the sequence still produce uniform shapes)
4. **Mean-pool** each window over the time dimension, collapsing it to a single vector
5. Repeat for all scales

We end up with `2S` pooled feature maps (two per scale, `S` scales total). Concatenate them all along the channel dimension and you get the unified multi-scale feature map `M`.

`M` is what feeds into both the classification head and the segmentation head downstream.

## Why It Works

The multi-scale strategy gives the model the temporal context appropriate for whatever it's looking at. Short events are captured by the smaller windows; longer events are captured by the larger ones. By concatenating across scales, every position in the output has access to information at multiple time scales simultaneously.

This is a 1D analog of feature pyramid networks in computer vision. Same idea — different scales for different object sizes.

## Scale Tuning

I systematically tuned the scale set during experiments. From Table 5.4 in the thesis:

| Scales `s` | Mean IoU | Macro-F₁ | Micro-F₁ |
|------------|----------|----------|----------|
| {0.3, 0.5} | 0.5042 | 0.5126 | 0.7332 |
| {0.3, 0.5, 0.8} | 0.5510 | 0.4855 | 0.7048 |
| {0.5, 1.5} | 0.5208 | 0.5310 | 0.7506 |
| {2, 3} | 0.5656 | 0.5079 | 0.6978 |
| **{2, 3, 4}** | **0.5498** | **0.5381** | **0.7559** |

I went with `{2, 3, 4}` for the final model — best balance between micro- and macro-F₁. Larger scales did better than fractional ones because swimming activities tend to span tens to hundreds of frames; the multi-scale generator with smaller fractional scales was looking at slices too short to give meaningful context.

## Boundary Handling

Edge cases at sequence boundaries were a real concern. To maintain uniform window lengths at the sequence edges, any out-of-bounds slices are zero-padded and then mean-pooled. This yields exactly `N` consistent feature vectors for the downstream heads — no shape mismatches, no awkward padding artifacts in the loss.

## What This Buys Us

The multi-scale feature map `M` is a rich representation that lets a single model handle activities of vastly different durations without specialized per-class architectures. It's also the bottleneck for computational cost — every position runs every scale's pooling, so the cost is `O(N × 2S × max_window_size)` per forward pass. That's a real cost and one of the reasons I flagged the architecture as too heavy for real-time inference on smartwatches in my conclusion.

## Keywords

multi-scale window generator, anchor-based detection, temporal anchors, Duan et al, feature pyramid, multi-scale features, mean pooling, zero padding, scale factor tuning, window length, swimming segmentation, 1D feature extraction, MTHARS, scale set, boundary handling
