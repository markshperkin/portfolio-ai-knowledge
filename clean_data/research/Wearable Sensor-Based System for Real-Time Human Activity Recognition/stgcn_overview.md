# ST-GCN Architecture Overview

## What ST-GCN Is

The **Spatio-Temporal Graph Convolutional Network (ST-GCN)** is a deep learning architecture specifically designed for human action recognition from skeleton data. After the wearable hardware approach failed, I shifted to implementing ST-GCN as proposed by Ghosh et al. and validated it on the NTU RGB+D benchmark.

ST-GCN's core insight: **a human skeleton is a graph**. Joints are vertices. Anatomical connections (bone structures) are spatial edges. The same joint across consecutive frames are temporal edges. By modeling the human body as a spatio-temporal graph, you can apply graph convolutions to learn rich representations of motion.

## Why Skeleton-Based HAR

Working from skeletal data has several advantages over raw video:
- **Compact representation** — 25 3D joint coordinates per frame vs. millions of pixels
- **Privacy-preserving** — no identifying visual features
- **Lighting-invariant** — works in any visibility condition
- **Cross-domain** — joints look the same regardless of camera angle, environment, or clothing
- **Edge-deployable** — small input dimension means small models can be effective

These properties match the original wearable-system goals — privacy, robustness, deployability.

## The Two Core Innovations

ST-GCN's contribution comes from two parallel feature extraction streams that decouple spatial and temporal information:

### 1. Spatial Convolutional Layer
Based on **adaptive graph convolutions** that learn data-dependent adjacency matrices. The network "attends" to the most informative joint relationships, going beyond the fixed anatomical structure.

### 2. Temporal Convolutional Layer
Lightweight, efficient convolutions along the time axis that capture motion dynamics across consecutive frames.

By **decoupling** spatial and temporal streams (rather than entangling them in a single big network), ST-GCN achieves:
- **High accuracy** competitive with heavier methods
- **Compact model footprint** — fewer parameters
- **Fast inference** — suitable for edge devices

## High-Level Architecture

The complete ST-GCN model:

1. **Initial batch normalization layer** — stabilizes training from the start
2. **10 sequential spatio-temporal convolutional blocks** — the main processing pipeline
3. **Fully connected layer with softmax** — outputs class probability distribution

That's it. The model isn't deep by modern standards (~10 blocks), but the careful design of each block makes it effective.

## A Single ST-GCN Block

Each block has:
- **Spatial convolution layer** (one parallel stream)
- **Temporal convolution layer** (the other parallel stream)
- Both outputs go through **batch normalization** and **ReLU activation**
- **Channel-wise concatenation** of the two streams
- **1×1 convolution** to fuse and reduce the combined dimensionality
- **Residual connection** for gradient flow

## Connection to Original Wearable Goals

ST-GCN delivers what the wearable system was meant to provide:
- **Real-time inference** on edge devices (993 frames/sec on Jetson Nano per the paper)
- **Activity classification** across many distinct movement classes
- **Skeleton-based** — could be paired with optical pose estimation OR a fixed wearable IMU array (without the position tracking requirement)

In some sense, ST-GCN solves the ML half of the original wearable problem, sidestepping the position-reconstruction half that doomed the hardware approach.

## NTU RGB+D Dataset

I trained ST-GCN on **NTU RGB+D**, a large-scale benchmark by Shahroudy et al.:
- **56,880 RGB-D video samples**
- **Over 4 million frames**
- **60 distinct action classes**
  - 40 daily activities
  - 9 health-related actions
  - 11 mutual (two-person) actions
- **40 subjects**
- **80 camera viewpoints**
- Captured using **Kinect v2 sensors**

Each sample provides synchronized modalities:
- RGB frames
- Depth maps
- Infrared sequences
- **3D joint coordinates for 25 body landmarks** ← this is what ST-GCN consumes

The skeletal modality is what makes this dataset ideal for graph-based HAR methods. Human joints become graph vertices, with spatial edges from anatomy and temporal edges across frames.

## Why ST-GCN Was the Right Choice

After the hardware failure, ST-GCN was the right pivot for several reasons:

1. **Compatible with original goals** — real-time HAR on resource-constrained devices
2. **Validated in literature** — well-cited paper with documented benchmarks
3. **Available dataset** — NTU RGB+D removes the data-collection bottleneck
4. **Implementable in PyTorch** — clean framework for training and benchmarking
5. **Edge-deployable** — supports the original deployment vision

## Keywords

ST-GCN, spatio-temporal graph convolutional network, skeleton-based action recognition, graph neural network, NTU RGB+D, 3D joint coordinates, adaptive graph convolution, temporal convolution, two-stream architecture, spatial-temporal decoupling, edge deployment, Ghosh et al, Shahroudy et al, IoMT, Internet of Medical Things, Kinect v2, action classification, numpy, pandas
