# MTHARS Architecture Overview

## What MTHARS Is

MTHARS stands for **Multi-Task Human Activity Recognition and Segmentation**. The original architecture was introduced by Duan et al. for general sensor-based HAR. I adapted it specifically for swimming.

The whole point of MTHARS is that it does **classification and segmentation jointly** — meaning it doesn't just label what activity is happening, it also predicts the precise temporal start and end of each activity, all in a single end-to-end pass. That's the property that lets us count strokes and kicks (because we get bounded segments, not just frame-level labels).

It's an **anchor-based** detector, conceptually similar to SSD (Single Shot MultiBox Detector) from computer vision — but operating on 1D temporal signals instead of 2D images.

## The Modules (How the Forward Pass Works)

The architecture is organized into several interconnected modules. Each does a specific job, but they're all jointly optimized to improve overall performance.

The full forward pass goes like this:

### 1. Backbone (1D CNN + Selective Kernel Convolution)

Input: a tensor `X` of shape `(B, C, T)` — `B` sequences of `C` sensor channels over `T` time steps.

- A 1D convolutional layer expands the channel dimension from `C` to 64
- Two **Selective Kernel Convolution (SKConv)** modules then produce 256-channel feature maps
- Every convolution is followed by batch normalization and ReLU activation

Output: a feature map with 256 channels at `N` temporal positions per example.

### 2. Multi-Scale Window Generator

This module extracts fixed-length slices around each of the `N` positions at `S` different scales. The key insight: short impulses (wall touches) and long activities (full stroke cycles) need different temporal contexts to recognize. So the network looks at multiple time scales simultaneously.

- For each scale, a predefined window length determines how many time steps to include
- Slices that extend beyond the data boundaries are zero-padded
- Mean pooling collapses each slice's time dimension into a single vector
- We generate **two pooled maps per scale**, so we end up with `2S` pooled maps
- These are concatenated along the channel axis to form the unified multi-scale feature map `M`

### 3. Classification Head

`M` goes into a pointwise (1×1) convolution that produces, at each of the `N` positions, a vector of `K` raw class scores — one for each activity category plus background.

- SoftMax converts these into confidence probabilities
- Each position now has a probability distribution over what activity it might contain

### 4. Segmentation Head

In parallel with classification, another pointwise convolution operates on `M` to predict two regression values per position:

- **Δx** — the temporal center offset (how far to shift the anchor's midpoint)
- **Δl** — the length adjustment factor (how much to scale the anchor's duration)

Applying these offsets to the default anchor windows yields refined start and end times that more precisely enclose the target activity.

### 5. Non-Maximum Suppression

At inference time, each refined window is paired with its classification confidence and passed to NMS:
- Proposals are sorted by confidence
- Any window that overlaps a higher-scoring segment is discarded
- The remaining windows constitute the final detected segments

## Architecture Parameter Summary

| Layer | Parameters (kernel / stride / padding / dilation) |
|-------|---------------------------------------------------|
| Layer 1 | Conv2D (5 / 3 / 1) |
| SKConv | Conv2D (3/1/1/1), Conv2D (3/1/2/2), Conv2D (3/1/3/3), three 1×1 fusions |
| Recognition + Segmentation Heads | Conv1D (3 / 1 / 1) |

## Why MTHARS for Swimming

Two reasons.

**First**, the multi-scale window generator is a perfect fit for swimming because event durations vary by an order of magnitude — a wall touch lasts a fraction of a second; a full stroke cycle takes a couple of seconds. Single-scale approaches would have to compromise.

**Second**, the joint classification + segmentation framing means we get bounded events, not just frame labels. Bounded events are countable. That's how I get stroke counts and kick counts as a free byproduct of the architecture, rather than having to bolt on a separate counter.

## Limitations of the Architecture

I want to be honest about this — MTHARS is not free.

The multi-scale window generator must extract, zero-pad, mean-pool, and concatenate feature slices at several scales **for every time step**. That's a lot of redundant work. Anchor-based predictions plus NMS add further overhead.

The architecture's accuracy is strong, but this exhaustive feature-extraction and proposal-pruning workflow incurs real memory and latency penalties. The current implementation is **not suitable for true real-time inference** on resource-constrained devices like smartwatches without further optimization or architectural simplification. That's something I flag explicitly in my conclusion and is one of the main directions for future work.

## Keywords

MTHARS, multi-task, architecture, deep learning, anchor-based, SSD, single shot detector, 1D convolution, CNN backbone, selective kernel convolution, SKConv, multi-scale window generator, classification head, segmentation head, non-maximum suppression, NMS, regression head, joint optimization, end-to-end, Duan et al, temporal activity detection, swimming activity recognition
