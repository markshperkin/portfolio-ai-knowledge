# EdgeFaceSearch — Tech Stack

## Languages

**Python** (100%) — entire project.

## Core Frameworks

### PyTorch
Used for model training and evaluation throughout the search. Each candidate architecture is built using PyTorch's `torchvision.models` (for the standard CNN backbones) plus a custom regression head.

### ONNX
For model conversion and edge deployment. After training, the optimal PyTorch model is exported to ONNX format for inference on Jetson Nano. ONNX is the bridge between research-friendly PyTorch and production-friendly inference runtimes.

### NVIDIA CUDA
Used during training for GPU acceleration. Optional — the code works on CPU too but training would be impractically slow.

## Architecture Search Components

### CNN Backbones (21 explored)
The search included a wide variety of architectures from `torchvision.models`:
- ResNet family (ResNet18, ResNet34, ResNet50, ...)
- VGG variants
- MobileNet variants (designed specifically for edge deployment)
- EfficientNet variants
- DenseNet
- SqueezeNet
- And others

Each backbone has different size, compute, and accuracy characteristics. The point of the search was finding which one fit best for the latency target.

### Custom Regression Head
A two-layer head sits on top of each backbone:
- **Layer 1** — reduces dimensionality by half from the backbone's output
- **Layer 2** — produces 4 values: bounding box `(x, y, width, height)`

The simple regression head keeps the bounding-box-specific parameters minimal — most of the work happens in the backbone, which is the part being searched over.

## Key Files

| File | Purpose |
|------|---------|
| `secondSearch.py` | Executes the multi-stage architecture search |
| `results.py` | Sorts configurations by fitness function |
| `plot.py` | Visualizes training curves |
| `ONNX.py` | Converts PyTorch models to ONNX format |
| `trainopt.py` | Trains the final optimal architecture |
| `dataloader.py` | Handles dataset ingestion |
| `evaluate.py` | Computes assessment metrics |

The codebase is organized around the search workflow: search → sort → visualize → finalize → export.

## Dataset

**FDDB (Face Detection Data Set and Benchmark)** — a widely used benchmark for face detection research.
- Annotated face bounding boxes
- Diverse images covering different lighting, poses, occlusions
- Standard split for fair benchmarking

## Evaluation Metrics

### Intersection over Union (IoU)
Standard bounding box accuracy metric. Measures how well a predicted box overlaps with ground truth.
- IoU = 0 — no overlap
- IoU = 1 — perfect alignment

The competition required a minimum IoU threshold, with latency as the tiebreaker.

### Inference Latency
Measured directly on **NVIDIA Jetson Nano** — not on a development GPU. This was a strict requirement: the latency that mattered was the deployment-environment latency.

The Jetson Nano measurement requires:
- Loading the ONNX model on the device
- Running inference in a measurement loop
- Excluding warm-up iterations
- Averaging across many runs

## Development vs. Deployment

A meaningful split between training and inference environments:

### Training (Development)
- Big GPU (e.g., GTX/RTX-class) for fast experimentation
- PyTorch native models
- Full Python ecosystem with all the heavy dependencies

### Inference (Deployment)
- Jetson Nano (small edge device)
- ONNX Runtime
- Minimal dependency footprint

This split is typical for edge AI projects. You can't train on Jetson Nano (too slow), and you don't want to deploy with the full PyTorch dependency tree (too heavy).

## Why ONNX Specifically

ONNX (Open Neural Network Exchange) is the standard interchange format for ML models:
- Framework-agnostic — train in PyTorch, deploy in ONNX Runtime, TensorRT, OpenVINO, etc.
- Optimized inference — runtimes apply graph-level optimizations
- Hardware-friendly — runtimes integrate with vendor accelerators (CUDA, Metal, NPU)

For Jetson Nano specifically, NVIDIA's TensorRT can ingest ONNX directly and produce a hardware-optimized inference engine. This pipeline (PyTorch → ONNX → TensorRT → Jetson) is the canonical edge deployment path.

## Why This Stack Choice Matters

A few takeaways:

### Why PyTorch for Search
Dynamic graphs make iterating fast. With 84 candidate configurations, fast iteration matters. Static-graph frameworks would have been clunkier for the search workflow.

### Why ONNX for Deployment
Without ONNX (or similar), you'd have to install full PyTorch on Jetson Nano. That's hundreds of MB of dependencies for what should be lightweight inference. ONNX strips that down to just what's needed.

### Why CUDA Only for Training
Inference on Jetson uses TensorRT or ONNX Runtime, not bare CUDA. CUDA is for the dev side.

## Keywords

PyTorch, ONNX, CUDA, NVIDIA Jetson Nano, neural architecture search, NAS, ResNet, VGG, MobileNet, EfficientNet, regression head, bounding box, FDDB, IoU, latency benchmarking, edge deployment, TensorRT, ONNX Runtime, hardware acceleration, deployment pipeline
