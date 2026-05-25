# EdgeFaceSearch — Overview

## What It Is

EdgeFaceSearch is a **neural architecture and hyperparameter search system** for optimizing face bounding-box prediction on resource-constrained edge hardware — specifically NVIDIA Jetson Nano. The project placed **second** in an Edge and Neuromorphic Computing class competition where models were evaluated on **latency** while maintaining a minimum accuracy threshold.

GitHub: https://github.com/markshperkin/EdgeFaceSearch

## What Problem It Solves

Deploying face detection on edge devices is hard. You want:
- **Low latency** — real-time inference on weak hardware
- **Reasonable accuracy** — has to actually find faces
- **Compact model** — memory-constrained devices have limits

These constraints conflict. A bigger model is more accurate but slower. A smaller model is faster but loses accuracy. Finding the right architecture and hyperparameter combination for your specific edge hardware is genuinely hard.

EdgeFaceSearch automates that search. Instead of picking a single architecture and hoping for the best, it systematically explores a large space of CNN backbones × learning rates and finds the best combination for the target hardware.

## How It Works (At a High Level)

The system runs a **structured neural architecture and hyperparameter search** in three stages:

### Stage 1: Initial Screening
- **84 configurations** total
- 21 different CNN base architectures × 4 learning rates (1e-2, 1e-3, 1e-4, 1e-5)
- Each trained for **10 epochs** — fast enough to rank but informative enough to differentiate

### Stage 2: Refinement
- Top **8 candidates** from Stage 1
- Trained for **30 epochs**
- More compute on the most promising configurations

### Stage 3: Final Optimization
- Top **2 finalists** from Stage 2
- Trained for **60 epochs**
- Full optimization to extract maximum performance

This staged approach is much cheaper than running all 84 configs to convergence. You spend most compute on the configurations that actually have a chance of being best.

## The Best Configuration

After the search:
- **Backbone**: ResNet18
- **Learning rate**: 0.01
- **Latency**: 0.0129 seconds on Jetson Nano
- **Accuracy**: 40% IoU on FDDB

ResNet18 won by being a sweet spot — deep enough for the regression task, but shallow enough to run fast on Jetson Nano. The 0.01 LR was aggressive but stable for the bounding-box regression task.

## The Architecture

The model uses a **regression head** with two layers:
- Input layer reduces dimensionality by half from the base architecture's output
- Output layer produces **four values** for bounding box coordinates: (x, y, width, height)

Standard regression formulation. The clever part isn't the head — it's the systematic search to find the right backbone for the latency target.

## Why The Staged Search Matters

A few benefits over alternative approaches:

### vs. Random Search
Random search would waste compute on architectures we know are too slow (very deep networks) or too small (architectures that can't represent face features well). The staged approach focuses budget on plausible candidates.

### vs. Grid Search
Grid search treats all configurations equally. With 84 configs and 60 epochs each, that's 5,040 epochs of compute. The staged approach uses ~840 + 240 + 120 = 1,200 epochs total — roughly 4x cheaper for similar quality.

### vs. Learning-Curve Methods
Bandit-style algorithms (Hyperband, Successive Halving) are similar in spirit. The staged search here is essentially a manual Successive Halving with three rungs.

## Why This Matters

Edge deployment of face detection is a real product need:
- Smart cameras
- Doorbell cameras
- Privacy-preserving face authentication
- On-device photo organization

Off-the-shelf models like RetinaFace are too heavy for Jetson Nano-class hardware. EdgeFaceSearch's approach — domain-specific architecture search — is the right way to get production-quality face detection on weak hardware.

## My Role

This was a class project (Edge and Neuromorphic Computing at USC, Professor Ramtin Zand). I worked with collaborators from Professor Zand's Intelligent Circuits, Architectures, and Systems Lab. I focused on the search methodology, model training, and ONNX deployment pipeline.

## Keywords

EdgeFaceSearch, neural architecture search, NAS, hyperparameter search, edge deployment, NVIDIA Jetson Nano, face detection, bounding box regression, ResNet18, CNN backbone, FDDB dataset, IoU accuracy, latency optimization, three-stage search, successive halving, USC, Ramtin Zand, ICAS Lab, numpy
