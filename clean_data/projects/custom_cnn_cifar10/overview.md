# CustomCNNforCIFAR-10 — Overview

## What It Is

A **custom convolutional neural network** designed for classifying 32×32 pixel images into 10 categories on the CIFAR-10 dataset. The architecture draws inspiration from VGG — stacked convolutional layers — but is adapted to balance accuracy with low inference latency for edge deployment.

GitHub: https://github.com/markshperkin/CustomCNNforCIFAR-10

## The Competition

This was a class Kaggle-style competition for the **Edge and Neuromorphic Computing course at USC**. The scoring metric was unusual and specifically designed for edge ML:

> **Final score = average accuracy / average latency**

That formula makes both axes matter. A purely accurate model that takes too long to run loses points. A blazingly fast model with poor accuracy also loses. You had to optimize both.

I placed **third** in the competition.

## What It Does

Takes a 32×32 RGB image as input. Predicts one of 10 CIFAR-10 classes:
- airplane
- automobile
- bird
- cat
- deer
- dog
- frog
- horse
- ship
- truck

The CNN extracts features through stacked convolutions and pooling, then a final classifier head produces the class probabilities.

## Architecture Inspiration

VGG (Visual Geometry Group networks) was the inspiration. VGG popularized the pattern of stacking many small (3×3) convolutional layers rather than fewer large ones. This gives:
- More expressive feature representations
- Smaller per-layer parameter counts
- Better gradient flow during training

I borrowed that core structure and tuned it for the specific accuracy/latency tradeoff the competition demanded.

## Why It Mattered

This project taught me:
- How architecture choice trades against latency
- Why VGG's design is durable (small kernels, deep stacks)
- How to design custom CNN architectures from scratch (vs. just using torchvision pre-builts)
- The discipline of benchmarking against a fixed score that combines speed + accuracy

It was also a good warm-up for my later EdgeFaceSearch project, which took the same accuracy/latency tradeoff and turned it into a systematic search problem.

## My Role

Built the entire model architecture, training pipeline, and evaluation. Sole owner of this submission.

## Keywords

CustomCNNforCIFAR-10, CIFAR-10, image classification, custom CNN, VGG-inspired, edge computing, accuracy latency tradeoff, USC, Edge and Neuromorphic Computing, Kaggle competition, third place, 32x32 images, 10-class classification
