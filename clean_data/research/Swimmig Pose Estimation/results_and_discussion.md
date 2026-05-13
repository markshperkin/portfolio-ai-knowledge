# Results & Discussion

## Positive Outcomes

The HRNet-W32 architecture demonstrated effectiveness in underwater pose estimation by accurately predicting keypoint locations for familiar swimming poses within the training dataset.

The model's ability to maintain high-resolution representations and fuse multi-scale features enabled precise spatial localization of **13 anatomical keypoints**:
- Head
- Shoulders (left and right)
- Elbows (left and right)
- Hands (left and right)
- Hips (left and right)
- Knees (left and right)
- Ankles (left and right)

These are the standard human-pose keypoints, adapted to swimming context.

## Dataset Size Comparison: 84 Frames vs. 411 Frames

The most informative result in this paper is the comparison between two models trained on different dataset sizes — same architecture, same hyperparameters, just more data.

### The Model Comparison

| Keypoint | Confidence (411 model) | Confidence (84 model) | Distance (411 model) | Distance (84 model) |
|---|---|---|---|---|
| 1 | 0.6 | 0.1 | 4.2 | 34 |
| 2 | 0.5 | 0.0 | 2.3 | 210 |
| 3 | 0.6 | 0.0 | 4.1 | 100 |
| 4 | 0.6 | 0.0 | 3.8 | 93 |
| 5 | 0.5 | 0.0 | 3.7 | 135 |
| 6 | 0.5 | 0.0 | 3.6 | 171 |
| 7 | 0.7 | 0.0 | 1.2 | 33 |
| 8 | 0.4 | 0.0 | 3.1 | 115 |
| 9 | 0.9 | 0.0 | 2.8 | 57 |
| 10 | 0.5 | 0.0 | 1.0 | 85 |
| 11 | 0.6 | 0.0 | 3.9 | 133 |
| 12 | 0.6 | 0.0 | 4.3 | 152 |
| 13 | 0.6 | 0.1 | 2.5 | 142 |

The 411-frame model:
- Confidence scores generally **0.4 to 0.9** across keypoints
- Distance errors mostly **1-4 pixels**

The 84-frame model:
- Confidence scores essentially **0.0** for nearly every keypoint
- Distance errors of **30-200+ pixels**

The 84-frame model isn't just worse — it's **functionally broken** on unseen poses. The 411-frame model produces useful predictions.

### What This Tells Us

This isn't a marginal data-effect result. **Even modest dataset increases dramatically improve robustness** in pose estimation. The 5x data jump (84 → 411 frames) is the difference between a non-functional model and a usable one.

The implication: pose estimation in narrow domains is severely data-limited. If you want underwater pose estimation that generalizes, you need a few thousand frames at minimum, not a few hundred.

## Negative Outcomes

Despite the model's strengths, real limitations emerged:

### Limited Generalization
The smaller 84-frame model exhibited a **pronounced inability to generalize**, performing well only on poses identical to those seen during training. This underscores the susceptibility of ML models to overfitting with small or narrowly scoped datasets.

### No Dedicated Validation/Test Split
The absence of dedicated validation and testing datasets restricted rigorous performance assessment. Evaluation was largely qualitative on held-out frames — useful for intuition but not for benchmarking.

I flag this honestly because it limits the strength of the conclusions. A proper evaluation framework with documented train/val/test splits is needed for rigorous benchmarking.

## Discussion

### Strengths
The results validate HRNet-W32's strengths for this domain:
- **High-resolution maintenance** matters for fine-grained joint localization
- **Multi-scale fusion** helps even with significant occlusions
- **Visibility-weighted training** reduces noise from unreliable joints

These characteristics make HRNet-W32 a robust solution for **controlled environments** where training and testing scenarios align closely.

### Generalization Challenges
When the model was exposed to unseen swimming strokes and poses, generalization suffered. The 84/411 comparison shows this directly. The larger dataset enabled meaningful generalization; the smaller one didn't.

This suggests expanding the dataset with more varied swimming styles, angles, and environmental conditions could **significantly enhance the model's applicability**.

### Augmentation Contribution
The implemented data augmentation (horizontal flipping, rotation, translation) contributed to robustness by simulating variability in the training data. They helped address occlusions and distortions common in underwater environments.

### Evaluation Framework Limitation
A key limitation: no dedicated validation/testing framework. While performance on training data and qualitative assessments of unseen frames provided valuable insights, **structured evaluation using separate datasets is necessary for rigorous benchmarking**. Such a framework would offer a clearer picture of generalization across diverse scenarios.

## Looking Ahead

The study opens several avenues for enhancement:

1. **Expand the dataset** — broader range of swimmer types, strokes, environmental conditions
2. **Hyperparameter optimization** — refine the model architecture and training schedule
3. **Transfer learning** — leverage pre-trained terrestrial pose models and fine-tune underwater
4. **Formal evaluation framework** — train/val/test splits with documented metrics

These steps will help develop a more generalizable, robust pose estimation system applicable to:
- Swimming performance analysis
- Injury prevention
- Biomechanical studies
- Sports science research more broadly

## Bigger Picture

This work represents an important step toward creating tools that empower swimmers and coaches to improve technique and achieve better outcomes. By addressing the observed limitations and building on the demonstrated strengths, future iterations can transform underwater swimming analysis into a precise and actionable science.

The ML side is solvable. The bottleneck is data — collecting, annotating, and curating diverse underwater pose datasets at scale.

## Keywords

results, HRNet performance, pose estimation results, dataset size effect, 84 frames vs 411 frames, generalization, overfitting, confidence scores, distance errors, pixel accuracy, validation testing limitation, qualitative evaluation, augmentation effect, future work, dataset expansion, transfer learning, swimming performance analysis
