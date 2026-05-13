# Training Hyperparameters

## The Final Configuration

After all the tuning experiments, here's exactly what I trained the final model with:

| Component | Value |
|-----------|-------|
| IoU threshold (τ) | 0.5 |
| Hard negative ratio (R) | 0.4 |
| Classification loss weight (α) | 1 |
| Localization loss weight (β) | 2 |
| Window size | 450 samples (300 + 50% overlap) |
| Frame reduction factor | 3 |
| Multi-scale generator scales | {2, 3, 4} |
| Optimizer | Adam |
| Initial learning rate | 1 × 10⁻³ |
| Epochs | 50 |
| Batch size | 8 |
| LR schedule | reduce by 0.1 at epoch 30 |

## How I Got Here

Each of these values came from a tuning experiment. I documented them all separately:

- **τ = 0.5** chosen after IoU threshold tuning. Lower (0.3) introduced noisy weak matches; higher (0.7) starved the model of training signal.
- **R = 0.4** chosen after hard negative mining tuning. Higher values (0.8, 1.5) collapsed mean IoU even though they raised micro-F₁, indicating over-suppression.
- **α = 1, β = 2** chosen after loss weight balancing. Slightly favoring localization gave better mean IoU and macro-F₁ together.
- **Scales {2, 3, 4}** chosen after scale tuning. Larger scales worked better than fractional ones because swim activities span tens to hundreds of frames.
- **Window size 300 + 50% overlap = 450** chosen for an average of ~5 ground-truth segments per window.
- **Frame reduction factor 3** matches the network's feature-level resolution to label coordinates.

## Optimizer Choice

**Adam** with learning rate `1 × 10⁻³`. Standard. I didn't tune the optimizer extensively — Adam works well for problems with this level of complexity and sparse positive examples (where some parameters get rare gradient signal). SGD with momentum might have squeezed out marginal gains but at the cost of more babysitting.

## Learning Rate Schedule

I used a step-decay schedule: train at `1e-3` for the first 30 epochs, then reduce by a factor of 10 to `1e-4` for the remaining 20 epochs.

This kind of step decay is a workhorse for anchor-based detection. The model needs the higher LR early to navigate the rough loss landscape of joint classification + regression; late in training, the lower LR helps it settle into a clean minimum without bouncing around.

I didn't try cosine annealing or warmup — those might have helped marginally but the step decay was good enough that further LR engineering wasn't the bottleneck.

## Batch Size

**8** examples per mini-batch. Small. This was driven by GPU memory constraints — the multi-scale window generator produces a lot of intermediate tensors per example, and the feature maps get large. Batch size 8 was the sweet spot where I could fit a batch on the available hardware without aggressive checkpointing.

Smaller batches mean noisier gradients, but with `N_pos` normalization in the loss, the variance is manageable.

## Number of Epochs

**50 epochs.** Validated by watching training loss curves and validation accuracy. The loss curves showed steady convergence (Figure 5.3) without overfitting at 50 epochs. Longer training didn't help; shorter undertrained.

## Inference Settings

For inference, I apply non-maximum suppression (NMS) on the classification confidences and offset regressions to produce the final temporally localized activity segments. The NMS algorithm is documented separately (see `non_maximum_suppression.md`).

## Reproducibility Notes

If anyone wanted to reproduce this exactly:
- Use the same window size (300) and overlap (50%)
- Use the same frame reduction factor (3) for label coordinate alignment
- Match the hyperparameters in the table above
- Use leave-one-subject-out cross-validation with 11 subjects (held-out subject = author)
- Random seed wasn't fixed in my experiments, so expect ~1% variation across runs

## Keywords

hyperparameters, training configuration, IoU threshold tau, hard negative ratio R, alpha, beta, loss weights, window size, 450 samples, frame reduction, scales, Adam optimizer, learning rate, 1e-3, step decay, batch size 8, 50 epochs, non-maximum suppression, MTHARS training, leave-one-subject-out
