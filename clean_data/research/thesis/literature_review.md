# Literature Review

## Where the Field Started

Human activity recognition (HAR) is one of the most active research topics in pervasive computing. The field grew out of a few different application areas:

- **Ambient assisted living (AAL)** — continuous monitoring of activities of daily living in smart homes and care settings, especially for the elderly.
- **Human-computer interaction** with sensor data — early work on real-time activity recognition.
- **Context-aware computing** — using passive infrared motion detectors and similar sensors to infer context cheaply and privately.
- **Healthcare** — probabilistic sequence models like HMMs and CRFs, plus unsupervised pattern discovery, for monitoring people who need help living independently.

This is the broader academic context my thesis sits inside.

## Classical Machine Learning Era

Before deep learning swept through HAR, classical ML algorithms dominated. SVMs, k-Nearest Neighbors, Random Forests — all of them leveraging handcrafted time and frequency-domain features extracted from sensor streams. They worked. They still work in some niches.

The problem with classical approaches is that handcrafted feature extraction demands a ton of domain expertise and tends to generalize poorly. If you trained an SVM on running data and tried to apply it to swimming, you'd have to redo the feature engineering. That's not where the field could afford to stay.

## The Deep Learning Wave

Deep learning automated the feature extraction. Convolutional neural networks (CNNs) showed that you could feed in raw sensor streams and learn temporal and spatial patterns end-to-end. Müller et al. adapted three CNN architectures and introduced a Scaling-FCN classification head for IMU-based fitness recognition. Zhao et al. went further with parallel CNNs ingesting both DWT and STFT representations — getting near-perfect precision on a diverse set of sports activities.

LSTMs added the ability to capture long-range temporal dependencies. Researchers stacked them, made them bidirectional, ensembled them. Vakacherla et al. combined CNN with LSTM in a hybrid and got over 98% accuracy on five daily activities from a single chest-mounted accelerometer. Khatun et al. added self-attention to a CNN-LSTM and hit 99.93% on H-Activity, 98.76% on MHEALTH, and 93.11% on UCI-HAR.

Hybrid GRU-CNN architectures pushed things further. DeepSense used CNN modules for local features and stacked GRU layers for temporal dynamics. AttnSense added multi-level attention over both modalities. Stacking 1D-CNN heads with a GRU head hit state-of-the-art for clinical balance assessment from a single IMU.

## The Transformer Era

The Transformer changed everything in sequence modeling. Self-attention without recurrence. People immediately tried it on HAR. Mahmud et al. processed raw IMU streams through self-attention and beat earlier CNN-RNN hybrids. Later work optimized for mobile — Shavit and Klein, Dirgová Luptáková et al. — getting accuracy above 99% with mobile-friendly inference. Guo et al. enhanced the Transformer with a convolutional feature extractor block and vector-based relative position embedding for state-of-the-art HAR.

## Swimming-Specific Work

In swimming activity recognition specifically, sliding-window segmentation paired with deep learning has been the dominant approach:

- **Delhaye et al.** segmented sacrum-mounted IMU data into 90-frame (1.8s) windows, ran them through a deep Bi-LSTM stack, predicted eight classes (four strokes, wall pushes, turns, underwater phases, rest). F1 of 0.96 and lap-time MAPE under 4.1%.
- **Zhang et al.** used a 150ms sliding window with 10ms stride on six lower-limb IMUs. They extracted time-domain features and used a stroke-dependent quadratic discriminant analysis model. Per-stroke accuracies from 97.24% to 99.10%.
- **Chen and Hu** introduced a hybrid DCNN-BiLSTM architecture: ten body-worn IMUs, 200-sample windows with 50% overlap at 200Hz, convolutional feature learning, then bidirectional LSTM. Balanced accuracies above 92% even when reduced to two sensors.

## What's Still Missing

Sliding-window approaches have a real limitation: they cannot reliably estimate the number of activity repetitions, because the true start and end points of each swim action remain unknown. Windows don't align with strokes — they're just a fixed-length grid laid over time.

Recent work tries to break out of fixed windowing entirely. Aminikhanghahi et al. frame segmentation as online change-point detection — kernel-based density-ratio divergence between consecutive windows flags real change points. Li et al.'s P2LHAP abandons sliding windows and splits each sensor channel into overlapping patches fed to a Seq2Seq Transformer that predicts patch-level labels.

## Why MTHARS

This is the gap MTHARS fills, and why I chose it as the foundation for my work. It's anchor-based — like SSD in computer vision — meaning it predicts variable-length segments directly rather than forcing everything into a fixed window. That makes counting events possible because each predicted segment is a real, bounded event.

I built on MTHARS specifically because it uniquely handles all four tasks (classification, segmentation, stroke counting, kick counting) in a single end-to-end pipeline.

## Keywords

literature review, related work, human activity recognition, HAR, ambient assisted living, smart homes, classical machine learning, SVM, KNN, Random Forest, deep learning, CNN, LSTM, GRU, DeepSense, AttnSense, Transformer, self-attention, swimming activity recognition, Delhaye, Zhang, Chen and Hu, P2LHAP, sliding window, change point detection, MTHARS, anchor-based detection, SSD, segmentation, stroke counting, IMU
