# Conclusion

## What This Thesis Established

The headline answer to my research question — **can a single wrist-worn IMU classify and segment all major competitive swim activities while also counting strokes and kicks?** — is **yes, with caveats**.

In leave-one-subject-out validation, the accelerometer-only MTHARS pipeline achieved a micro-F₁ of 0.7405 and a macro-F₁ of 0.5894. Adding gyroscope data improved performance to a micro-F₁ of 0.7709 and a macro-F₁ of 0.6565. Mean IoU stayed above 0.57 in both configurations, indicating temporal localization didn't degrade.

These results confirm that one wrist-worn IMU recording accelerometer and gyroscope is sufficient to deliver accurate segmentation and classification across all competitive swim activities. When evaluated solely on stroke classification and underwater-kick detection, my accelerometer-only model performs **on par with specialized pipelines** focused exclusively on those tasks — but with the added benefit of doing all four tasks simultaneously.

## The Real Challenges I Confronted

Two recurring themes throughout the work:

### Severe Class Imbalance
Underwater kicks, frequent strokes, and turns appeared in vastly different counts. Without hard negative mining and careful loss weighting, the model just learned to predict the dominant classes. Even with mining, rare events (wall touches especially) were under-served.

### High Inter-Swimmer Variability
A single activity label spans a wide range of sensor patterns because eleven athletes produce eleven distinct motion signatures. Capturing the full spectrum demands a larger, more carefully balanced dataset. Without sufficient diversity, unrepresented variations erode both segmentation precision and classification accuracy.

These two challenges are coupled — the rare events are exactly the ones where inter-swimmer variability matters most, because there are too few examples to average out the variability.

## The Architectural Cost

Honest acknowledgment: MTHARS's architectural complexity comes at a steep computational cost. The multi-scale window generator must extract, zero-pad, mean-pool, and concatenate feature slices at several scales **for every time step**. Anchor-based predictions plus non-maximum suppression add further overhead.

The resulting workflow incurs significant memory and latency penalties. The current implementation is **not suitable for true real-time inference** on resource-constrained devices like smartwatches or embedded swim monitors without additional optimization or architectural simplification.

This matters because the whole vision is real-time feedback during training. Until the architecture is slimmed down (or replaced with a more efficient one), the pipeline runs offline only — fine for analytics but not for in-pool feedback.

## What's Genuinely New Here

The contributions, in order of importance:

1. **End-to-end single-IMU pipeline** that simultaneously does stroke classification, lap segmentation, stroke counting, and kick counting. No prior work demonstrated this combination on one wrist-worn sensor.

2. **Systematic hyperparameter ablations** for swimming-specific MTHARS — IoU threshold, hard negative ratio, loss weights, scale factors. Future researchers don't have to redo this grid search.

3. **A modality study** showing that gyroscope data is most valuable for sparse / subtle motion classes (push-offs, glides, turns) while accelerometer alone suffices for full stroke cycles. Useful for designing minimum-hardware deployments.

4. **An honest dataset of 11 collegiate swimmers** with documented variability and limitations. The dataset isn't large but the labeling scheme is rigorous.

## Practical Implications

If you're a researcher or engineer building wearable swim analytics:

- Single wrist-worn smartwatch is a viable platform for stroke and lap analysis
- Anchor-based detection (not just sliding-window classification) gives you bounded events you can count
- Gyroscope adds real value for rare/sparse activities; not just a redundant sensor
- Multi-scale feature extraction matters because activity durations span an order of magnitude

If you're a coach evaluating commercial swim analytics tools:

- Stroke and lap classification on smartwatch hardware is technically feasible at ~75-90% accuracy
- Counting accuracy at ~10% error per set is in the realm of useful for training feedback
- Real-time performance is the unsolved engineering problem; current architectures are too heavy

## Closing Thought

I framed this work around a question — can wearable hardware that millions of athletes already own do meaningful swim analysis? The answer is yes, more than I expected when I started. The remaining work isn't fundamentally about new model architectures (though those help); it's about building bigger, better-balanced datasets and slimming the inference path so it runs on the watch itself.

The gap between "this works in a research pipeline" and "this works in your smartwatch app" is engineering. The fundamental ML problem is largely solved.

## Keywords

conclusion, summary, contributions, single IMU, smartwatch swim analysis, real-time inference limitation, class imbalance, inter-swimmer variability, computational cost, future deployment, stroke classification, lap segmentation, stroke counting, kick counting, MTHARS limitations
