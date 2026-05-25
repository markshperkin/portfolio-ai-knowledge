# MNIST — Overview

## What It Is

A **handwritten digit classifier** built with PyTorch. Trains a feedforward neural network on the classic MNIST dataset, validates accuracy, and supports inference on user-provided images. This was an educational project from my Neural Networks course at USC under Professor Vignesh Narayanan.

GitHub: https://github.com/markshperkin/MNIST

## What It Does

Three core capabilities:

1. **Train** a neural network on the MNIST handwritten digit dataset
2. **Validate** model performance on the MNIST test set
3. **Classify** user-provided images (PNGs of digits) into 0-9

It's a complete end-to-end pipeline — training to inference — even though the dataset is the most classic ML benchmark there is.

## Why MNIST Matters as a Project

MNIST is the "Hello World" of deep learning. Implementing it from scratch teaches:
- Data loading and preprocessing
- Model definition in PyTorch
- Training loops with optimizer + loss + backprop
- Validation methodology
- Model checkpointing and persistence
- Inference on novel data

Even though the actual classification task is simple (28×28 grayscale digits, very high baseline accuracy), the pipeline you build doing it is the same pipeline you'd use for any image classification problem.

## What I Built

A complete training and inference system with:
- Configurable hidden layer sizes (multiple model variants saved as different `.pt` files)
- SGD optimizer (with the option to switch to Adam)
- Standard cross-entropy loss
- Validation tracking per epoch
- Persistent model checkpoints

The repository contains multiple trained checkpoints showing the iterative process — `mnist_model.pt`, `mnist_model_with_increased_hidden_layers*.pt`. This documents the experimentation process, not just the final result.

## Tech Stack

**Framework**: PyTorch
**Language**: Mostly Jupyter Notebook (~97%) for the training/exploration, with Python scripts (~3%) for inference

**Key Libraries**:
- PyTorch (network operations)
- Torchvision (MNIST dataset loading)
- Pillow / PIL (image processing for custom inference inputs)
- NumPy (numerical operations)
- Matplotlib (loss/accuracy visualization)

## My Role

Sole author. Built and trained all variants of the model, evaluated them, and packaged the inference pipeline.

## Educational Context

Coursework under **Professor Vignesh Narayanan** at the **University of South Carolina** in his Neural Networks class. The project incorporated practices from academic tutorials on PyTorch implementations.

## Keywords

MNIST, handwritten digit classification, PyTorch, fully connected neural network, MLP, training pipeline, model checkpointing, custom inference, USC, Vignesh Narayanan, Neural Networks course, educational project, Jupyter notebook, foundational ML, numpy
