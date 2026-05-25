# Swimming Pose Estimation Paper — Overview

## Summary

This paper, "Swimming Pose Estimation," is a research project I led at the University of South Carolina. I'm the sole author. The work applies the **High-Resolution Network (HRNet)** architecture to detect and analyze swimmer poses during underwater activities — a domain that's been largely underexplored due to its unique challenges.

Email contact: shperkin@email.sc.edu

## What the Paper Does

It tackles a real, hard problem: **underwater pose estimation**. While human pose estimation has matured for terrestrial scenarios (sports analytics, motion capture, AR/VR), underwater environments break most of the assumptions those models depend on. My work adapts HRNet to underwater swim footage and demonstrates that the model can produce useful keypoint detections — when given enough training data.

## Why Underwater Pose Estimation is Hard

A few unique challenges:

- **Poor visibility** — water scatters and absorbs light differently than air
- **Occlusions** from turbulence, bubbles, and other swimmers
- **Dynamic lighting** — caustic patterns, refraction, ambient light shifts
- **Scarcity of annotated datasets** — labeling underwater video is time-intensive and few public datasets exist
- **Joint occlusion** — swimmers' joints frequently exit the water frame, become covered by bubbles, or get hidden by their own body in streamline

Standard pose estimation models trained on COCO (which is overwhelmingly terrestrial) fail to generalize. This study explicitly trains on an **underwater-only** dataset to address these challenges directly.

## My Approach

- Collected video footage from the **University of South Carolina swim team** during practice
- Annotated keypoints in **COCO format with visibility flags** (0 = not in frame, 1 = occluded, 2 = visible)
- Used **HRNet-W32** — the variant that maintains high-resolution feature representations throughout the network
- Applied data augmentation: horizontal flipping, random rotation, translation
- Trained with **Adam optimizer**, learning rate 1e-3, batch size 8, 100 epochs
- Used **MSE loss** on heatmaps with **visibility-weighted dynamic loss** (occluded joints contribute less to the gradient)

## Key Results

The model accurately predicts 13 anatomical keypoints (head, shoulders, elbows, hands, hips, knees, ankles) for poses similar to the training distribution.

A direct comparison between two models — one trained on 84 frames vs. one trained on 411 frames — produced a striking finding: the **larger dataset model generalized dramatically better**. The 84-frame model essentially failed on novel poses, while the 411-frame model achieved confidence scores around 0.5-0.9 across keypoints with much smaller distance errors.

This isn't surprising in the abstract, but the magnitude of the improvement underscores how data-hungry pose estimation models are — even modest dataset increases yield outsize generalization gains.

## Code

GitHub repo: https://github.com/markshperkin/SwimmingPoseEstimation

## Why This Work Matters

Beyond academic interest, accurate underwater pose estimation enables:
- **Performance analysis** — coaches can quantify technique on a per-stroke basis
- **Injury prevention** — biomechanical asymmetries become detectable
- **Tailored training regimens** — pose data informs personalized coaching
- **Broader sports science** — a foundation for similar work in diving, water polo, synchronized swimming

The work itself is an early step. The more important contribution is showing that HRNet — designed for terrestrial pose estimation — can be adapted to underwater contexts with the right dataset and visibility handling.

## Honest Limitations

Stated upfront in the paper:

1. **No dedicated validation/test split** — evaluation was largely qualitative on held-out frames; rigorous benchmarking would require formal split
2. **Small dataset overall** — even 411 frames is tiny by computer vision standards
3. **Single domain** — only USC swim team; no cross-pool, cross-team validation

I list these because honest research transparency matters more than inflated claims.

## Keywords

swimming pose estimation, underwater pose estimation, HRNet, HRNet-W32, high resolution network, computer vision, keypoint detection, COCO format, visibility annotations, occlusion handling, swim performance analysis, biomechanics, USC swim team, Mark Shperkin, underwater computer vision, sports analytics, numpy, pandas
