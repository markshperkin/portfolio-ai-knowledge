# Literature Review

## Where Pose Estimation Started

Human pose estimation has long been a central problem in computer vision, with applications ranging from activity recognition and human-computer interaction to sports performance analysis.

**Traditional approaches** relied on probabilistic graphical models or pictorial structures. These were effective in constrained scenarios but struggled with complex poses and environmental variability. They didn't generalize well, and they required heavy hand-engineering of features.

The advent of **deep learning revolutionized the field**, enabling robust keypoint detection and heatmap estimation using convolutional neural networks (CNNs). This is the lineage I'm building on.

## Existing Pose Estimation Architectures

### Hourglass Networks
Early CNN-based methods like Hourglass Networks adopted a **high-to-low resolution process followed by symmetric low-to-high recovery** to generate keypoint predictions. The idea: down-sample to capture context, then up-sample to recover spatial precision.

**Limitation**: Significant spatial precision loss due to intermediate down-sampling. Even with skip connections, the recovered high-resolution features lose detail compared to the original.

### SimpleBaseline
Methods like SimpleBaseline used **transposed convolutions to recover high-resolution representations**.

**Limitation**: Transposed convolutions can introduce artifacts and reduce accuracy for fine-grained spatial tasks. They're also somewhat blunt instruments — they trade compute for resolution recovery, not always cleanly.

### Cascaded Pyramid Networks (CPN)
Multi-scale fusion techniques like Cascaded Pyramid Networks aimed to mitigate these issues by **combining features across resolutions**.

**Limitation**: These methods relied heavily on separating up-sampling stages, which introduced computational complexity and limited spatial fidelity. The fusion happened at discrete points rather than continuously.

## High-Resolution Network (HRNet)

HRNet introduced a paradigm shift by **maintaining high-resolution representations throughout the network**.

### The Key Idea
Instead of down-sampling and then recovering, HRNet **never lets go of the high-resolution stream**. It connects multiple resolution subnetworks **in parallel**, enabling continuous multi-scale feature fusion.

This design ensures that high-resolution features are enriched with information from low-resolution representations **at every stage**, eliminating the need for explicit upsampling.

### Why This Matters
For pose estimation specifically, you need **precise spatial localization** of keypoints. A keypoint that's off by a few pixels matters when you're computing joint angles for biomechanical analysis. Architectures that lose and recover spatial information are inherently disadvantaged here.

HRNet's "always-high-resolution" design directly addresses this. The high-resolution stream is enriched with context from the low-resolution streams via repeated multi-scale fusion, but it never loses the fine spatial detail that down-sampling discards.

### Validated Performance
HRNet's architecture has been validated on multiple benchmarks:
- **COCO Keypoint Detection** — outperformed traditional networks
- **MPII Human Pose** — also outperformed prior methods
- Both in **accuracy and computational efficiency**

This is what made it the natural choice for my underwater application — it's the strongest off-the-shelf pose architecture I could adapt.

## Challenges in Underwater Pose Estimation

Despite advancements in pose estimation, **applications in underwater environments remain underexplored**. The unique challenges:

- **Poor visibility** — light absorption and scattering reduce image contrast
- **Occlusions** from bubbles and turbulence
- **Dynamic lighting** — caustics, refraction, surface ripples
- **Lack of domain-specific datasets** — most pose data is COCO/MPII (terrestrial)
- **Lack of features optimized for underwater conditions** — color profiles, occlusion patterns differ

Traditional models designed for terrestrial environments often **fail to generalize** to these scenarios. This is the gap my work addresses.

## Why HRNet Is the Right Tool

HRNet brings two specific properties that matter for underwater pose:

1. **High-resolution features throughout** — preserves the fine spatial detail needed to localize joints in low-contrast underwater images
2. **Multi-scale fusion** — combines information across resolutions, helping the network identify keypoints even when local context is weak (occluded by bubbles, low-light areas, etc.)

When paired with **visibility annotations** (which let the model handle occluded joints gracefully) and **underwater-specific training data**, HRNet becomes a strong starting point for this domain.

## What's Different in This Study

A few things this work brings to the table that prior pose estimation literature doesn't directly address:

- **Domain-specific underwater training set** — most pose work uses generic terrestrial data
- **Visibility-weighted loss** — explicitly handles the occlusion-heavy reality of underwater scenes
- **Empirical study of dataset size effect** — comparing 84-frame vs. 411-frame models to characterize the data-quantity sensitivity

The insights gained have potential applications in **swimming performance analysis, biomechanical studies, and injury prevention** — extending pose estimation's reach into a meaningful new application area.

## Keywords

literature review, related work, pose estimation history, Hourglass Networks, SimpleBaseline, transposed convolution, Cascaded Pyramid Networks, CPN, HRNet, high resolution network, COCO Keypoint Detection, MPII Human Pose, multi-scale fusion, parallel subnetworks, underwater computer vision, occlusion, domain gap, visibility-aware training
