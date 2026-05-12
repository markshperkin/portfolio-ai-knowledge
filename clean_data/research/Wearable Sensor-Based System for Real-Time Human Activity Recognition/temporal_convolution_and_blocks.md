# Temporal Convolution & ST-GCN Blocks

## Temporal Convolution Layer

While the spatial convolution captures relationships across joints **within a frame**, the temporal convolution operates **purely along the time axis**.

### How It Works

The input has shape `C × T × N`:
- `C` = number of channels (features)
- `T` = number of frames
- `N` = number of joints

The temporal convolution applies a **2D convolution with kernel size `Kt × 1`**:
- `Kt` = number of frames spanned (the temporal kernel)
- `× 1` = only one joint at a time

This shape preserves the joint dimension while capturing temporal patterns. The same temporal pattern is applied to each joint independently — meaning, for each joint, the network learns to recognize how its features change over `Kt` consecutive frames.

### Why This Decoupled Approach

Why not do everything in one giant 3D convolution that mixes space and time? Because separating them yields:
- **Lower parameter count** — `Kt × 1` is much smaller than `Kt × N`
- **Faster computation** — fewer multiplications per forward pass
- **Better generalization** — each operation has a focused purpose
- **Cleaner gradient flow** — each stream's gradient is more interpretable

This kind of factorization is a recurring trick in deep learning. Inception modules, separable convolutions, MobileNet — all use the same pattern: decompose expensive operations into cheaper sequential ones without losing much representational power.

## The ST-GCN Block

A single ST-GCN block fuses the spatial and temporal streams into a single processing unit.

### The Block's Forward Pass

1. **Process input via spatial convolution** (one parallel stream)
2. **Process input via temporal convolution** (other parallel stream)
3. **Batch normalize** and **ReLU activate** both outputs
4. **Channel-wise concatenate** the two streams
5. **1×1 convolution** to fuse and reduce the combined feature dimensionality
6. **Residual connection** added back to the block input

### Why the Residual Connection

Residual connections (skip connections) are now standard in deep networks. They:
- **Improve gradient flow** during backprop
- **Enable training deeper networks** without vanishing/exploding gradients
- **Allow the network to learn an identity mapping** if needed
- **Speed up convergence** in practice

For ST-GCN's 10-block depth, residuals matter — without them, the network would be much harder to train.

### Why the 1×1 Fusion Convolution

After concatenating the spatial and temporal streams channel-wise, you have a feature map with `2C` channels. The 1×1 convolution:
- **Reduces dimensionality** back to `C`
- **Learns to mix** the spatial and temporal features
- **Adds nonlinearity** when followed by activation
- **Keeps parameter count low** (1×1 convs are cheap)

## Complete Architecture

The full ST-GCN model:

1. **Initial batch normalization layer** — input is normalized to stabilize training
2. **10 sequential ST-GCN blocks** — the bulk of the network
3. **Fully connected layer with softmax** — produces class probability distribution

10 blocks is a reasonable depth. Deep enough to learn rich representations; shallow enough to train without sophisticated tricks like deep supervision.

## Training Configuration

I trained the model with the following setup:

| Parameter | Value |
|-----------|-------|
| Framework | PyTorch |
| Optimizer | SGD with Nesterov momentum |
| Momentum | 0.9 |
| Weight decay | 1e-4 |
| Initial learning rate | 0.01 |
| LR reduction | factor of 10 at epochs 30 and 40 |
| Total epochs | 50 |
| Batch size | 16 |
| Loss | Cross-entropy |
| Train/val split | 80/20 |
| Input length | 300 frames (sequences shorter were temporally replicated) |

### Why SGD with Nesterov

For this kind of architecture, SGD with momentum often outperforms Adam. SGD's noise can help find broader minima that generalize better. Nesterov momentum specifically gives a "look-ahead" gradient computation that converges faster than vanilla momentum.

### Why Step LR Decay

Step decay at epochs 30 and 40 is a workhorse schedule. The network learns rapidly early; later, the lower LR helps it settle into a clean minimum. I followed the protocol from Ghosh et al.'s ST-GCN paper to enable direct comparison.

### Why 50 Epochs

50 epochs was enough to reach convergence on NTU RGB+D for this architecture. Training loss and validation loss curves plateau in the last 10 epochs, with peak validation accuracy reached at epoch 49.

### The 300-Frame Padding Trick

ST-GCN expects fixed-length inputs (300 frames per sample). For sequences shorter than 300 frames, I temporally replicated the available frames until reaching 300 — essentially looping the action. This is a simple way to handle variable-length inputs without padding with zeros (which can confuse a temporal model).

## Result

Peak validation accuracy: **87.6% by epoch 49**. The training and validation accuracy/loss curves (Figures 4 and 5 in the paper) show clean convergence without significant overfitting.

This is in line with — though slightly below — the published ST-GCN result of 92.2% on NTU RGB+D's cross-view benchmark. The gap is plausibly attributable to:
- My implementation details vs. the reference codebase
- The specific train/val split
- Hyperparameter choices that I didn't fully tune

87.6% is enough to validate that the architecture is correctly implemented and trains stably. The point isn't to beat the literature — it's to demonstrate reproducibility and confirm edge-feasibility.

## Keywords

temporal convolution, time axis convolution, ST-GCN block, factorized convolution, spatial temporal decoupling, residual connection, 1x1 convolution, batch normalization, ReLU activation, channel concatenation, 10 blocks, PyTorch implementation, SGD Nesterov momentum, weight decay, learning rate schedule, step decay, 300 frame padding, validation accuracy
