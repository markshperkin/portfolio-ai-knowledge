# CustomCNNforCIFAR-10 — Architecture & Implementation

## Inspiration: VGG

The architecture draws from **VGG** — a well-known design that demonstrated stacked 3×3 convolutional layers can match or beat networks with larger kernels. VGG's key design principles:

- Use small kernels (3×3) consistently
- Stack many of them between max-pooling steps
- Double the channel count at each downsampling
- Keep the architecture deep but uniform

This pattern is durable because it makes gradient flow predictable, parameter counts manageable, and the search for hyperparameters tractable.

## My Adaptations

CIFAR-10 is small (32×32) compared to ImageNet (224×224). A literal VGG would over-parameterize — too many channels, too much computation, too slow. So I designed a slimmer variant:

- Fewer total layers (the input is small; you can't go very deep before features collapse)
- Modest channel counts (32 → 64 → 128 → 256 type progression)
- Aggressive downsampling early to manage spatial dimensions
- Smaller fully connected head than VGG's ~4000-unit layers

The result is a model that captures VGG's design philosophy in a footprint sized for CIFAR-10 and the competition's latency constraint.

## Tech Stack

**Language**: Python (100%)

**Framework**: PyTorch (or TensorFlow — the codebase supports both via separate scripts)

**Environment Management**: Conda (with `environment.yml` provided)

**GPU Support**: CUDA-optimized for NVIDIA GPUs during training

**Dataset**: CIFAR-10 (downloaded and preprocessed via included scripts)

## Key Files

| File | Purpose |
|------|---------|
| `get_dataset.py` | Downloads CIFAR-10, splits into train/val/test |
| `train.py` | Model training loop |
| `test.py` | Model evaluation on test set |
| `score.py` | Computes the competition score (accuracy/latency) |
| `to_image.py` | Image conversion utilities |
| `ProjectReport.docx` | Detailed project documentation |

## Training Pipeline

The training workflow:

1. **Data preparation** — `get_dataset.py` fetches CIFAR-10 and splits it
2. **Model definition** — custom CNN class defined in PyTorch/TensorFlow
3. **Training loop** — `train.py` runs SGD or Adam over the training set, validates each epoch
4. **Checkpointing** — saves the best model by validation accuracy
5. **Evaluation** — `test.py` runs the saved model on held-out test data
6. **Scoring** — `score.py` measures latency and computes the final competition score

## Hyperparameters

Standard image classification hyperparameters:
- Optimizer: Adam (or SGD with momentum, depending on which performed better in tuning)
- Learning rate: tuned per the competition setup
- Batch size: tuned for GPU memory and training stability
- Data augmentation: random crops, horizontal flips (standard CIFAR-10 augmentation)

## Latency Measurement

Latency was measured directly — single-image forward pass through the model, repeated many times to get a stable average. This matched the competition's requirement to score on real inference speed, not theoretical FLOPs.

## Optimization Strategies

To improve the accuracy/latency score, I used several techniques:

### Architecture Slimming
Trim layers and channels until accuracy stops dropping. This sounds simple but requires care — pruning the wrong layer kills accuracy, while pruning the right one barely affects it.

### Batch Norm Folding
For inference, batch normalization can be folded into preceding convolutions. This eliminates a layer's compute without changing the output. Free latency savings.

### Activation Function Choice
ReLU is fast. Some fancier activations (Swish, GELU) give small accuracy improvements at noticeable latency cost. ReLU was the right call here.

### Pooling vs. Strided Conv
Max-pooling is faster than strided convolution for downsampling. I used pooling where I could.

## Why VGG's Design Translates

VGG was designed for 224×224 images, but its principles transfer:
- **Small kernels are efficient** even at low resolution
- **Stacked convs build expressive features** regardless of image size
- **Doubling channels at each downsample** maintains representational capacity as spatial size shrinks
- **The pattern is regular** — easy to implement, easy to reason about

For CIFAR-10's smaller input, the same pattern works with smaller dimensions.

## Lessons

A few takeaways:

### Architecture Inspiration ≠ Copying
I started from VGG's principles but didn't copy VGG's specific dimensions. Adapting to CIFAR-10's input size required real architectural decisions.

### Latency Optimization Is Practical, Not Just Theoretical
You can't just pick "fast operations" from a textbook. You have to measure on real hardware. Batch norm folding looks marginal in theory but adds up.

### The Score Function Drives Everything
A pure-accuracy metric and an accuracy/latency metric pull architectures in completely different directions. Knowing the metric early shapes every design choice.

### Practical Skills > Architecture Glamour
Building a production-ready CIFAR-10 classifier from scratch is more valuable training than fine-tuning a pre-built ResNet. You learn what each piece actually does.

## Keywords

CustomCNN, VGG-inspired, CIFAR-10, image classification, PyTorch, TensorFlow, conda environment, CUDA, accuracy latency score, Kaggle competition, 32x32 images, batch norm folding, max pooling, ReLU, SGD Adam optimizer, model design, edge inference, custom architecture, numpy
