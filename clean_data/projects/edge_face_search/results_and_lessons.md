# EdgeFaceSearch — Results & Lessons

## Competition Result

**Second place** in the Edge and Neuromorphic Computing class competition at USC. The competition evaluated submissions on inference latency on NVIDIA Jetson Nano while requiring a minimum accuracy threshold.

## The Winning Configuration

After three stages of search:

| Parameter | Value |
|-----------|-------|
| Backbone | ResNet18 |
| Learning rate | 0.01 |
| Latency on Jetson Nano | 0.0129 seconds |
| IoU accuracy | 40% |
| Final training epochs | 60 |

13ms inference latency on Jetson Nano-class hardware is genuinely fast. That's ~75 frames per second throughput, comfortable for real-time camera processing.

40% IoU isn't competition-level for face detection in absolute terms — large industrial models on WIDER FACE achieve much higher — but it's reasonable for FDDB given the latency constraint. The whole point was joint optimization, not pure accuracy.

## Why ResNet18 Won

A few reasons ResNet18 came out on top:

### Sweet-Spot Depth
- Deep enough to represent face features well (not just blobs)
- Shallow enough to run fast on weak hardware
- Has skip connections that help training stability with the regression head

### Production-Tested
ResNet18 has well-optimized kernels in TensorRT. The Jetson Nano runs it efficiently because the underlying primitives are heavily tuned.

### Stable at 0.01 LR
Some architectures explode at LR=0.01. ResNet18's batch normalization and skip connections keep gradients well-behaved even at aggressive learning rates.

## What I Learned About Edge Search

### The Ranking Changes by Hardware
What's fastest on a Jetson Nano isn't necessarily fastest on a smartphone or a Coral TPU. The search has to be re-run for each target. There's no universally best edge architecture.

### Latency Isn't Just About Parameter Count
A model with fewer parameters can be slower if its operations don't map well to the target hardware's accelerators. Memory bandwidth, kernel availability, and operator fusion all matter.

### Converged Models Matter
The Stage 1 ranking (after 10 epochs) wasn't perfectly correlated with the Stage 3 ranking (after 60 epochs). Some architectures are slow learners — they need more epochs to show their best. The staged design accommodates this.

### Conditional Hyperparameters
Some LRs work for some architectures but not others. The search-space design has to allow for this — treating LR and architecture as independent factors loses information about their interaction.

## What I'd Do Differently

If I were rebuilding this:

### Use Bayesian Optimization Instead of Grid + Halving
The 21×4 grid plus successive halving approach is fine but inefficient. Bayesian optimization (e.g., via Optuna or Ray Tune) would explore the space more intelligently and find better configurations faster.

### Include Quantization in the Search
INT8 or FP16 quantization can give 2-4x latency improvements on Jetson Nano. The search should include quantization as a search variable, not just an afterthought.

### Test More Datasets
FDDB is fine but WIDER FACE has more diverse and challenging examples. The "best" architecture might differ across datasets, especially for harder edge cases.

### Better Latency Measurement
Single-sample latency on a single device is one number. A more robust measurement would profile across batch sizes, with warm/cold cache states, and across multiple Jetson Nano units to capture variance.

## What This Project Demonstrated

Beyond the competition placement:

1. **Systematic NAS works** — even with simple staged search, you find configurations that beat hand-picked architectures
2. **Edge deployment is a real engineering discipline** — it's not just "make it smaller"; it's joint optimization across architecture, training, and target hardware
3. **PyTorch → ONNX → TensorRT is a viable pipeline** for production edge deployment
4. **Class projects can produce competitive results** — when scoped carefully, undergraduate or graduate coursework can yield genuinely useful systems

## Skills Demonstrated

This project exercised:
- Neural architecture search methodology
- PyTorch model implementation and training
- ONNX export and deployment
- Hardware-aware ML optimization
- Latency benchmarking
- Hyperparameter tuning under compute constraints
- Edge ML engineering (Jetson Nano specifics)
- Competition-driven optimization

## Connection to Other Projects

This work fed directly into my thesis on swimming activity recognition, which had similar deployment constraints (smartwatch, real-time inference). The edge-deployment thinking I developed here transferred:
- Joint accuracy/latency optimization
- Recognition that consumer hardware constraints matter
- Importance of measuring on the actual target device

It also informed my approach to the HAR-STGCN project, where I benchmarked inference on multiple device classes (RTX 4070 Super and i7-14700F).

## Keywords

second place, competition result, ResNet18, 0.0129s latency, 40% IoU, edge ML, NAS results, hardware-aware ML, Jetson Nano benchmarks, bounded search budget, lessons learned, Bayesian optimization, quantization, ONNX TensorRT pipeline, edge deployment engineering, numpy
