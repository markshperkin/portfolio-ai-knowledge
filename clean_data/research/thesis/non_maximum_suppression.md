# Non-Maximum Suppression (NMS)

## Why NMS Is Needed

The MTHARS model produces lots of overlapping segment proposals — each anchor at each position is a potential prediction. Many of those proposals are redundant, all pointing at roughly the same activity but with slightly different boundaries and slightly different confidence scores.

Without NMS, you'd get a messy, multiple-counting output. NMS cleans it up by keeping the highest-confidence prediction and suppressing overlapping lower-confidence ones — leaving you with a tidy, non-overlapping set of detected activities.

## My Two-Stage 1D NMS

I refine the model's raw segment proposals using a **two-stage 1D NMS**. The "1D" part matters — most NMS literature talks about 2D bounding boxes; here I'm working with 1D temporal intervals.

### Stage 1: Per-Class Suppression

For each predicted class (excluding background):

1. Sort that class's proposals by confidence score, descending
2. Greedily select the highest-scoring window
3. Suppress any other windows of the same class that overlap with it
4. Repeat with the next highest-scoring remaining window

This produces a class-wise "preliminary keep" list — within each class, no two surviving proposals overlap.

### Stage 2: Cross-Class Merging

After Stage 1, you might still have overlapping proposals from different classes (e.g., a "freestyle" prediction overlapping with a "turn" prediction). Stage 2 resolves these.

1. Sort all preliminarily kept windows from all classes by confidence, descending
2. In descending order, retain each window only if it doesn't overlap any previously selected window
3. Suppress any cross-class overlaps by always keeping the highest-confidence proposal

The result: a final set of temporally localized, non-overlapping segments, each with its predicted class label and confidence.

## Why Two Stages and Not One

Single-stage NMS (sort everything by confidence, suppress overlapping) has a problem: a high-confidence freestyle prediction can suppress a slightly lower-confidence turn prediction that should also be kept (because they're different activities at different positions).

Two-stage NMS handles within-class redundancy first (multiple freestyle predictions over the same stroke cycle → keep one) and then handles cross-class conflicts (a freestyle vs. turn prediction overlapping → keep the more confident one).

This matters in swimming because activities are tightly packed — a turn ends, immediately followed by a push-off, immediately followed by underwater glide. Single-stage NMS could over-suppress consecutive activities.

## Overlap Calculation

I use the same 1D IoU calculation as during training:
- Two intervals overlap if their IoU > 0
- The amount of overlap determines what gets suppressed

In Stage 2, I apply suppression any time two windows overlap at all (rather than using a fixed IoU threshold). This is because by Stage 2, the within-class duplicates are gone — what remains is genuinely different events, so any temporal overlap is a real conflict.

## What NMS Outputs

For each test sequence, after NMS you get a list of:

`(start_sample, end_sample, predicted_class, confidence)`

That's the final detection output. Stroke counts come from counting freestyle/backstroke/breaststroke/butterfly segments. Kick counts come from counting underwater_kick segments. Lap times can be derived from push-off and wall-touch positions.

## Implementation Notes

- NMS runs only at inference, not during training (during training, the loss is over all anchors)
- Computational cost is `O(N²)` in the number of proposals — for the typical proposal counts in swimming (a few hundred per session), this is trivial
- The two-stage design adds modest extra compute but is worth it for the cleaner output

## Keywords

non-maximum suppression, NMS, 1D NMS, two-stage NMS, per-class suppression, cross-class merging, proposal pruning, inference, post-processing, overlap suppression, confidence-based selection, anchor-based detection, segment deduplication, temporal NMS, MTHARS inference
