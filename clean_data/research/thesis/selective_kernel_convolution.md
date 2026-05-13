# Selective Kernel Convolution (SKConv)

## What It Is

The Selective Kernel Convolution block, introduced by Gao et al., is the core feature-extraction unit in my MTHARS pipeline. It's designed specifically for sensor-based human activity recognition, and it solves a real problem: **how do you choose the right receptive field when different activities operate at different time scales?**

Instead of forcing one fixed kernel size, SKConv learns to **dynamically select and weight multiple receptive fields** based on the input.

## The Three-Stage Strategy: Split, Fuse, Select

SKConv implements a Split → Fuse → Select pattern:

### Split
Multiple convolutional branches with **distinct receptive fields** run in parallel, each extracting its own feature representation. In my architecture, the SKConv block uses three Conv2D paths with different dilations:
- `Conv2D (3/1/1/1)` — kernel 3, dilation 1
- `Conv2D (3/1/2/2)` — kernel 3, dilation 2
- `Conv2D (3/1/3/3)` — kernel 3, dilation 3

These three branches see the input at three effective receptive fields, capturing patterns at different temporal granularities simultaneously.

### Fuse
A global average-pooling and channel-reduction layer aggregates all the branch features into a compact descriptor. This descriptor summarizes the input's overall characteristics in a low-dimensional space — basically asking the network, "what are we looking at right now?"

### Select
A SoftMax-based attention mechanism generates **per-branch weights** that determine how to combine the branch outputs into the final feature representation. The attention weights are conditioned on the descriptor, so the model adaptively decides which receptive field matters most for the current input.

## Why This Is the Right Tool for Swimming

In swimming, the temporal scale of what you're trying to recognize varies massively:

- A **wall touch** is a sharp impulse, fractions of a second
- An **underwater kick** is a moderate-duration event, less than half a second
- A **freestyle stroke cycle** can be 1-2 seconds
- A **turn-and-push-off sequence** can span 2-3 seconds

If I picked a single receptive field, I'd be optimizing for one of these and compromising on the others. SKConv lets the network adaptively route different inputs through the receptive field that best fits them. The wall touch path gets attention from the smaller-receptive-field branch; the stroke cycle path gets attention from the larger one.

## Connection to Transformers

There's an interesting structural parallel here. The Split-Fuse-Select paradigm mirrors the transformer's **multi-head attention mechanism**, where parallel attention heads capture diverse aspects of the input and recombine them via learned weights.

By dynamically selecting and weighting convolutional kernels, SKConv extracts both fine-grained local patterns and broad global dependencies across the IMU signal — effectively enriching the feature space in a transformer-like way, but with the inductive biases of convolutions (translation equivariance, locality).

I find this connection elegant. It's part of why I trust SKConv as a design choice — it's not just a heuristic, it has a principled relationship to attention.

## Computational Cost

The dynamic kernel selection yields significant accuracy improvements on benchmark HAR datasets with only a **modest increase in computational cost**. That's a good trade — most of the heavy lifting is in the parallel branches, but they're each lean. The fuse stage is global pooling + a small MLP. The select stage is a softmax. Nothing exotic.

## My Configuration

In my final pipeline:
- Two SKConv modules stacked, both producing 256-channel feature maps
- Each followed by batch normalization and ReLU
- Operating on 1D temporal sensor data (not 2D as in the original Gao et al. computer vision context)

The 256-channel output is what feeds into the Multi-Scale Window Generator downstream.

## Keywords

selective kernel convolution, SKConv, Gao et al, multi-scale features, dynamic receptive field, split fuse select, attention mechanism, channel attention, dilated convolution, multi-head attention parallel, CNN backbone, feature extraction, batch normalization, ReLU, 1D convolution, sensor HAR, dilation, kernel size 3
