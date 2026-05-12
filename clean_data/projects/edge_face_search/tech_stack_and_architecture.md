# EdgeFaceSearch — Tech Stack & Architecture

## Language

**Python** (100% of codebase)

## Core Frameworks

- **PyTorch** — model training, evaluation, and the core deep learning operations
- **ONNX** — model conversion for cross-platform deployment
- **NVIDIA CUDA** — optional GPU acceleration during training

## Why This Stack

### PyTorch
Standard for research-style architecture search. PyTorch's dynamic graph makes it easy to swap backbones programmatically — exactly what's needed when you're iterating across 21 different architectures.

### ONNX
The deployment target was Jetson Nano, which runs ONNX models efficiently via TensorRT. Converting trained PyTorch models to ONNX gives:
- Cross-framework portability
- Hardware-specific optimizations
- Reduced inference overhead at deployment

### CUDA
For training. Search across 84 configurations × 10+ epochs each is compute-intensive even with the staged design. GPU acceleration was essential to keep wall-clock time reasonable.

## File Structure

The repo is organized around the search pipeline:

| File | Purpose |
|------|---------|
| `secondSearch.py` | Executes the multi-stage architecture search loop |
| `results.py` | Sorts configurations by fitness (accuracy/latency tradeoff) |
| `plot.py` | Visualizes training curves across configurations |
| `ONNX.py` | Converts the best PyTorch model to ONNX format |
| `trainopt.py` | Trains the final optimal architecture |
| `dataloader.py` | Handles FDDB dataset ingestion and preprocessing |
| `evaluate.py` | Computes IoU, accuracy, latency metrics |

## The Fitness Function

The competition was scored on a combination of **accuracy and inference latency**. The search ranks configurations by a fitness metric that combines both — typically **accuracy / latency** so that faster models with reasonable accuracy beat slower models with marginally better accuracy.

This is the right framing for edge deployment. A 95% accurate model that takes 100ms is worse than an 80% accurate model that takes 5ms when you're trying to run real-time face detection on a Jetson Nano.

## Architecture Search Space

### Backbone Architectures (21 total)
The search covers a wide range of CNN backbones from various model families:
- ResNet variants (18, 34, 50)
- MobileNet variants
- EfficientNet variants (small)
- VGG variants
- Custom lightweight architectures

The 21 choices span from "very small, very fast, lower accuracy" through "moderate size, moderate speed" — deliberately excluding anything too heavy to run on Jetson Nano at all.

### Learning Rates (4 values)
- 1e-2 (aggressive)
- 1e-3 (moderate)
- 1e-4 (conservative)
- 1e-5 (very conservative)

This covers two orders of magnitude. Bounding-box regression often works best at higher LRs than classification, so including 1e-2 was important.

### Combinations
21 × 4 = 84 configurations evaluated in Stage 1.

## The Regression Head

After the backbone, a custom **two-layer regression head**:
- **Input layer** — takes the backbone's output features, reduces dimensionality by half
- **Output layer** — produces 4 values for bounding box: (x, y, width, height)

This is straightforward but matters because:
- The dimensionality reduction prevents the head from being parameter-heavy
- 4-output regression cleanly maps to bounding box coordinates
- No softmax — face vs. not-face isn't a classification, just regression of "where is the face"

## Dataset

**FDDB** (Face Detection Data Set and Benchmark) — a standard academic benchmark for face detection. Contains:
- ~5,000 face annotations across ~2,800 images
- Multiple faces per image, varying poses and lighting

FDDB is a reasonable benchmark — not as large as WIDER FACE but big enough for the search to be informative.

## Deployment Pipeline

End-to-end from search to deployment:

1. **Training in PyTorch** on FDDB
2. **Search loop** identifies best configuration
3. **Final training** at 60 epochs on best config
4. **ONNX conversion** for Jetson Nano deployment
5. **TensorRT-accelerated inference** on the target device

The pipeline is reusable — swap in a different dataset or different target hardware and re-run the search.

## Lessons Learned

### Search Budget Allocation
The staged approach (10 → 30 → 60 epochs) was the right call. Running all 84 configs to 60 epochs would have been ~4x more compute for marginal additional information. Spending most compute on candidates that have already proven themselves is the efficient strategy.

### LR Tuning Matters
The "best architecture" depends on the LR. ResNet18 at LR=0.01 won; ResNet18 at LR=1e-5 was probably uncompetitive. Architecture and LR are coupled — they need to be searched together.

### Latency Ranking Differs from Parameter Count
Some larger architectures actually run faster than smaller ones on specific hardware due to better memory access patterns or operator-level optimizations. You can't just pick the smallest model — you have to measure on the target device.

### ONNX Conversion Has Gotchas
Some PyTorch operations don't have clean ONNX equivalents. Sticking to standard ops (Conv, BN, ReLU, Linear) makes deployment painless. Exotic activations or custom layers cause headaches.

## Keywords

PyTorch, ONNX, CUDA, NVIDIA Jetson Nano, TensorRT, edge deployment, neural architecture search, NAS, hyperparameter search, ResNet, MobileNet, EfficientNet, FDDB dataset, face detection, bounding box regression, fitness function, accuracy latency tradeoff, staged search, successive halving, model conversion
