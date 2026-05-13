# EdgeFaceSearch — Architecture & Search Design

## The Search Pipeline

The project's architecture isn't really about one neural network — it's about the **search system that finds the best neural network**. Three stages, progressively narrower:

```
Stage 1 (Screening):    84 configs × 10 epochs   →  top 8
Stage 2 (Refinement):    8 configs × 30 epochs   →  top 2
Stage 3 (Final):         2 configs × 60 epochs   →  winner
```

This funnel saves enormous compute. The full search would have been 84 × 60 = 5,040 epoch-equivalents. The funnel is roughly 84×10 + 8×30 + 2×60 = 1,200 epoch-equivalents — about 4× less compute.

## Why a Funnel

The early epochs of training are highly informative — bad architectures show themselves quickly. There's no point training a configuration that's 10% behind at epoch 10 to convergence; it'll still be behind at epoch 60. The funnel exploits this to eliminate clear losers early.

The risk is that a slow-converging configuration might rank low at epoch 10 but be the best at epoch 60. I mitigated this by:
- Keeping the top 8 (not just top 2) after Stage 1
- Confirming Stage 2 rankings stayed roughly consistent through Stage 3

In practice the funnel was reliable.

## The Search Space

### Backbones (21 options)
Drawn from PyTorch's torchvision model zoo. The point was to cover a wide range of compute/accuracy tradeoffs:

- **Light**: MobileNet variants, SqueezeNet
- **Medium**: ResNet18, ResNet34, EfficientNet-B0
- **Heavy**: ResNet50, ResNet101, VGG-16, DenseNet-121

Each backbone produces a feature map. The bounding box regression head sits on top.

### Learning Rates (4 options)
- `1e-2` — aggressive
- `1e-3` — standard
- `1e-4` — conservative
- `1e-5` — very conservative

LR has a huge effect on training. Too high and the model diverges. Too low and it doesn't converge in the available epoch budget. Including 4 values across two orders of magnitude lets the search find the right LR for each backbone.

### What I Didn't Search
A few axes I held fixed to make the search tractable:
- Batch size (constant across all configs)
- Optimizer (Adam, no SGD comparison)
- Data augmentation strategy
- Image resolution
- Loss function (smooth L1 throughout)

A more thorough search would have hit these too. The 84-configuration scope was already at the edge of what was feasible to run.

## Bounding Box Regression Head

After the backbone, a small regression head produces the bounding box.

```
backbone_output (variable dim)
    ↓
Linear(backbone_dim → backbone_dim/2)
    ↓
ReLU activation
    ↓
Linear(backbone_dim/2 → 4)   # x, y, width, height
```

Two layers is intentionally minimal. The intent was to keep the head identical across all backbones so the search isolates the backbone's contribution. If the head varied per backbone, the search would be confounded.

## Loss Function

Smooth L1 (Huber loss) on bounding box predictions. Standard for object detection regression — robust to outliers, smooth gradients near zero.

```
target: (x_gt, y_gt, w_gt, h_gt)
predicted: (x_p, y_p, w_p, h_p)
loss = SmoothL1(predicted - target)
```

Mean across the batch.

## Fitness Function

The search ranks configurations by a custom fitness function combining accuracy and latency. The exact formula varies by competition but is essentially:

```
fitness = accuracy / latency
```

(Or `accuracy - λ * latency` for a weighted version.)

This is what makes the search meaningful for edge deployment — it actively penalizes models that are too slow, regardless of how accurate they are.

## Pipeline Stages in Detail

### Training Phase
For each candidate:
1. Initialize backbone + regression head
2. Train on FDDB for the specified number of epochs
3. Track training loss and validation IoU
4. Save the best checkpoint by validation IoU

### Conversion Phase (Final Stage Only)
For the winning configuration:
1. Load best checkpoint
2. Set to eval mode
3. Trace through ONNX export
4. Validate the ONNX model produces the same outputs as PyTorch

### Latency Measurement Phase (Final Stage Only)
1. Deploy ONNX to Jetson Nano
2. Run a benchmark loop (typically 1000 iterations)
3. Discard first ~50 iterations as warm-up
4. Average remaining latency

This phase is critical and was the actual measurement that determined the competition rankings.

## Why ResNet18 Won

The optimal configuration was **ResNet18 with 0.01 LR**. A few likely reasons:

- **Right size**: ResNet18 is big enough to learn meaningful features but small enough to run fast on Jetson Nano (~0.013s)
- **Mature architecture**: ResNet has well-understood training dynamics — less surprising at the high 0.01 LR
- **Hardware-friendly**: ResNet's blocks (3×3 convs, batch norm, ReLU) are well-optimized in inference runtimes
- **No exotic operations**: Some newer architectures use operations that aren't well-supported in TensorRT — ResNet doesn't have that issue

MobileNet variants were faster but didn't hit the accuracy threshold. EfficientNet had higher accuracy but slower inference. ResNet18 was the right balance.

## Lessons from the Search

A few things this project taught me:

### Edge Deployment ≠ Smaller Models
The intuition is "smaller = faster" but it's not that simple. Architectural choices that look small in parameter count can be slower than larger architectures on specific hardware due to memory access patterns and operator support. **Measure, don't assume.**

### The Hardware is Part of the Design
You can't optimize for "fast" — you can only optimize for "fast on this target hardware." Jetson Nano has specific compute and memory characteristics. Models tuned for it might be slower than expected on a different edge platform.

### Fitness Functions Matter
A single fitness function shapes the entire search. Defining it well is half the battle. `accuracy/latency` ranks differently from `accuracy - 100*latency` even if both seem reasonable.

### Search Funnels Are a Time Multiplier
The 4× compute savings from the funnel was the difference between "run all 84 to convergence" being feasible and not feasible.

## Keywords

architecture search, search funnel, three-stage search, fitness function, accuracy vs latency, ResNet18, MobileNet, EfficientNet, bounding box regression, smooth L1 loss, Huber loss, ONNX export, Jetson Nano deployment, latency measurement, TensorRT, edge optimization, CNN backbone, hyperparameter search, NAS
