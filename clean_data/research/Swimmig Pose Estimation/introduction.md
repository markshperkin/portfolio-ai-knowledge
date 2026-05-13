# Introduction & Motivation

## Why Pose Estimation for Swimming

Swimming performance is heavily reliant on precise technique. Even minor biomechanical adjustments — a slightly tucked elbow, a higher hip position, a small change in catch angle — can produce significant improvements in speed and efficiency. Coaches know this; they spend hours watching and providing feedback.

**Pose estimation systems are emerging as valuable tools** for capturing the keypoints that define an athlete's posture and movements during a stroke. These systems provide insights that enable visualization and analysis of swimming technique — ultimately guiding the improvements that enhance performance.

Beyond immediate feedback, accurate pose estimation lays the groundwork for broader applications:
- **Injury prevention** — detect asymmetries and risky biomechanics before they cause harm
- **Biomechanical research** — quantify technique objectively across athletes
- **Tailored training regimens** — personalize workouts based on individual movement patterns

## The Underwater Pose Estimation Problem

Most pose estimation systems target **terrestrial or above-water scenarios** — running, dancing, daily activity. Underwater introduces a fundamentally different set of conditions:

### Visual Challenges
- **Poor visibility** — light absorption and scattering through water reduces contrast
- **Occlusions caused by turbulence or bubbles** — air pockets and water disturbances obscure body parts
- **Dynamic lighting** — caustics from the surface create shifting bright/dark patterns
- **Color shifts** — water filters certain wavelengths, particularly red and orange

### Domain Challenges
- Inability to predict joints that are above water or occluded — half-submerged poses break standard models
- **Scarcity of annotated underwater datasets** — labeling is time-intensive and the data is hard to collect
- Body posture differs from terrestrial — streamline positions and stroke cycles produce poses rare in COCO/MPII

These challenges mean that off-the-shelf pose models, trained on terrestrial data, generalize poorly underwater. You need domain-specific training and architectural choices that account for occlusion.

## What This Study Does

I chose the **High-Resolution Network (HRNet)** architecture, which is renowned for maintaining high-resolution feature representations throughout the network rather than down-sampling and recovering. By focusing exclusively on underwater environments and employing a dataset I collected and annotated specifically for this context, the system aims to accurately estimate swimmer poses.

To improve generalization and robustness, I applied data augmentation:
- Horizontal flipping
- Random rotation
- Translation

The dataset adopts the **COCO format with visibility annotations** — each keypoint is labeled not just with `(x, y)` but also with a visibility flag. This lets the model handle occluded joints during training, reducing noise in the gradient signal from joints the model couldn't see.

## The Goal

The primary goal of this system is to enable **detailed analysis of swimmers' technique**. This can guide the development of downstream models that suggest targeted improvements — coaches' feedback, scaled.

Such advancements hold promise not only for competitive swimming but also for broader research applications in biomechanics and sports science. Underwater motion analysis is a niche but valuable domain, and methods that work here can transfer to diving, synchronized swimming, water polo, and similar contexts.

## Contribution Summary

The contribution of this paper:
1. **First (or among first)** application of HRNet specifically to underwater swimming pose estimation
2. A **collected and annotated underwater dataset** (USC swim team, 411 frames)
3. Demonstration that **visibility-weighted training** improves results in occlusion-heavy domains
4. **Honest evaluation** showing that data quantity matters dramatically — the 84-frame model fails to generalize while the 411-frame model produces useful predictions

This is an early-stage research contribution. The methods scale, the dataset is small, but the proof-of-concept is solid.

## Keywords

introduction, motivation, swimming technique analysis, biomechanics, pose estimation, underwater computer vision, occlusion challenges, visibility annotations, HRNet, terrestrial vs underwater, sports analytics, technique improvement, injury prevention, COCO format
