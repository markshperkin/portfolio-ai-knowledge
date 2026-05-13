# MNIST — Implementation Details

## Architecture

A **feedforward fully-connected network** (multilayer perceptron) for MNIST classification. The repo includes multiple variants showing iterative architecture exploration — original baseline, then versions with increased hidden layer counts.

The basic shape:
- **Input**: 28×28 grayscale image, flattened to 784-dim vector
- **Hidden layer(s)**: ReLU-activated fully connected layers
- **Output**: 10-class softmax (one per digit 0-9)

The "increased hidden layers" variants demonstrate the relationship between model capacity and accuracy. Adding more layers helps until you start overfitting on a dataset as well-trodden as MNIST.

## Training Components

### Optimizer
**SGD** (Stochastic Gradient Descent), with the option to swap in Adam. The README documents that the optimizer is "changeable to Adam" — a deliberate design choice to make experimentation easy.

For MNIST, both SGD and Adam reach high accuracy. SGD converges more slowly but often generalizes slightly better. Adam is faster to converge.

### Loss Function
**Cross-entropy** — standard for multi-class classification. Combined implicitly with softmax via `nn.CrossEntropyLoss`.

### Training Loop
Standard PyTorch training pattern:
1. Forward pass through the model
2. Compute loss against ground-truth labels
3. Backward pass to compute gradients
4. Optimizer step to update weights
5. Track loss/accuracy per epoch

Run for a fixed number of epochs, save the best checkpoint.

## Tech Stack Details

| Component | Library |
|-----------|---------|
| Network operations | PyTorch |
| Dataset loading | Torchvision (`MNIST` dataset class) |
| Image preprocessing for inference | Pillow / PIL |
| Numerical ops | NumPy |
| Visualization | Matplotlib |

The dataset loading uses Torchvision's built-in MNIST class, which auto-downloads the data on first run. This is the standard PyTorch pattern.

## Key Features

### 1. Training Module
Fully runnable training loop with configurable optimizer, learning rate, batch size, and number of epochs.

### 2. Validation Testing
Evaluates accuracy on the MNIST test set. Reports both per-class accuracy and overall accuracy.

### 3. Custom Image Inference
This is the practically interesting part — the system can take an arbitrary PNG of a hand-drawn digit, preprocess it (resize to 28×28, grayscale, normalize), and classify it.

This requires:
- Image loading via PIL
- Resizing to model input size
- Normalization to match MNIST's preprocessing (mean/std subtraction)
- Inference with the trained model
- Argmax to get the predicted digit

The custom inference pipeline forces you to think about deployment — the model exists in a vacuum during training, but inference requires real-world preprocessing.

### 4. Model Persistence
Saves trained weights as `.pt` files. The repo contains multiple checkpoints from different runs, demonstrating that the model can be retrained and the best version kept.

## What MNIST Teaches You

Even though MNIST is "easy":

### Data Preprocessing Matters
Normalizing inputs to mean 0, std 1 dramatically improves training. Forgetting this nearly always results in slow or failed training.

### Validation Curves Reveal Overfitting
Track training and validation accuracy. When validation plateaus while training keeps improving — you're overfitting. MNIST is small enough that this happens easily with a too-large model.

### Custom Inference Requires Discipline
Models don't generalize automatically to your hand-drawn images. You have to match the training preprocessing exactly. Off-by-one in the normalization or resize and the model fails on data it should be able to classify.

### Reproducibility Matters
Set random seeds. Pin library versions. Save preprocessing code with the model. These practices feel pedantic on MNIST but are essential when you scale up.

## Lessons Learned

### The Pipeline Is the Lesson
The actual classification accuracy isn't the takeaway. The takeaway is the end-to-end pipeline: data → model → training → validation → inference. Once you've built that pipeline for MNIST, you can build it for any classification task.

### Small Wins Build Confidence
Getting MNIST to >97% accuracy is satisfying even though it's standard. Building working ML systems from scratch is fundamentally about a series of small wins.

### Don't Skip the Fundamentals
I built this in a Neural Networks course, not as research. That's exactly the right context — you have to understand what each piece does before you can reason about more complex systems.

## Connection to Later Projects

The skills I built here transferred:
- The PyTorch training loop pattern shows up in every later project
- Custom inference pipelines become essential for deployment
- Validation methodology informs every benchmarking decision

MNIST was a foundational project, in the literal sense — it laid the foundation for everything else.

## Keywords

MNIST implementation, MLP, fully connected network, ReLU activation, softmax, SGD optimizer, Adam optimizer, cross-entropy loss, PyTorch training loop, Torchvision, model checkpointing, custom inference, PIL image preprocessing, validation curves, overfitting, foundational pipeline
