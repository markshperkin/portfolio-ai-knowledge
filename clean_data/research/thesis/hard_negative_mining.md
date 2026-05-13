# Hard Negative Mining

## The Class Imbalance Problem

In an anchor-based detector, the vast majority of anchors are **background** — they don't correspond to any real activity. In my pipeline, after the multi-scale window generator, you might have hundreds of anchors per training example but only a handful matched to real segments.

If you naively train on all anchors, the classification loss is overwhelmingly driven by background examples, and the model just learns "everything is background." The few positive anchors get drowned out. That's the core problem hard negative mining solves.

## What Hard Negative Mining Does

Instead of using all background anchors in the loss, you use only the **hardest** ones — the background anchors the model is most confidently mistaking for activities. By concentrating the loss on the difficult negatives, the model is forced to learn features that distinguish subtle confusion cases rather than just dunking on trivial easy negatives.

## The Algorithm

For each anchor `i`, the assigned label is `yᵢ`. `yᵢ = 0` means background; `yᵢ > 0` means a positive (matched) anchor.

### Step 1: Collect Background Anchors
First, gather all anchors with `yᵢ = 0`.

### Step 2: Compute "Hardness" Score
For each background anchor, compute a hardness score:

`hᵢ = max(over c > 0) ℓᵢ,c`

Where `ℓᵢ,c` is the logit for class `c` at anchor `i`, and the max is over the `K` non-background activity classes.

In plain English: `hᵢ` measures how strongly — and incorrectly — the model is predicting some real activity at this background anchor. High `hᵢ` means the model thinks this background looks a lot like an activity. That's a hard negative.

### Step 3: Sort and Select Top-K
Sort the background anchors in descending order of `hᵢ` and retain only the top:

`⌊R · N_pos⌋`

Where `N_pos` is the total number of positive anchors and `R` is the user-defined negative-to-positive ratio.

The idea: for every `R` background anchors you keep one positive, but you only keep the hardest `R · N_pos` background anchors out of all the available ones.

## Why This Works

By concentrating the classification loss on the **hardest negatives**, the model:
- Avoids being swamped by trivial background examples
- Learns features that better distinguish subtle, confusion cases
- Effectively does its own implicit curriculum learning — the loss is biggest where the model is most confused

This is a well-known trick from object detection (SSD uses it), but it's particularly important here because the background class is so dominant in time-series HAR.

## Tuning the Ratio R

I systematically tuned `R` and the results were eye-opening:

| R | Mean IoU | Macro-F₁ | Micro-F₁ |
|---|----------|----------|----------|
| 0.1 | 0.5662 | 0.5043 | 0.7121 |
| **0.4** | **0.5731** | **0.4974** | **0.7091** |
| 0.8 | 0.4148 | 0.5290 | 0.8458 |
| 1.5 | 0.1129 | 0.2173 | 0.9571 |

A few things to notice:

- **R = 1.5 looks great on micro-F₁ (0.95) but is a disaster on Mean IoU (0.11) and macro-F₁ (0.22).** What's happening: with so many hard negatives, the model is over-suppressing background and under-localizing — it's getting most positives right (high micro-F₁) but for entirely the wrong reasons (terrible localization, terrible class balance).
- **R = 0.8 also looks tempting but the Mean IoU drops** to 0.41, indicating localization is suffering.
- **R = 0.4 was my chosen value** — it balances classification accuracy against localization quality.

This is a great example of why you can't just optimize for one metric. Micro-F₁ in isolation is misleading.

## What I Learned

- **Hard negative mining is essential** for anchor-based 1D HAR. Without it, the model collapses.
- **Per-metric tuning matters.** R = 1.5 has the best micro-F₁ but the worst macro-F₁ and mean IoU. You have to look at the whole picture.
- **The balance is delicate.** Too few hard negatives and easy ones drown the loss; too many and you over-attention them and lose localization.

## Keywords

hard negative mining, class imbalance, background class, negative sampling, hardness score, top-k selection, neg-pos ratio, R hyperparameter, SSD style training, classification loss, anchor sampling, training strategy, online hard example mining, OHEM
