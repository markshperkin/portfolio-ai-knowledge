# Data Preprocessing Pipeline

## The Goal

Before the model sees anything, the raw sensor data has to be cleaned, aligned, and packaged into uniformly sized training examples with precisely localized labels. Preprocessing is where most real ML projects either succeed or quietly fail. I tried to be deliberate about it.

## Stage 1: Time-to-Sample Index Conversion

The raw accelerometer and gyroscope streams are recorded at 52.63 Hz, with timestamps. Step one is converting everything into a unified sample-index framework — meaning labels and signals are both expressed as integer positions in the time series.

The process:

1. Subtract the initial timestamp from each measurement → zero-based relative time vector
2. Take each annotated event (defined by center time and duration) and map it to discrete sample indices by locating the nearest neighbors in the relative time array
3. Recompute all segment centers and lengths as integer sample units
4. Truncate both sensor streams at the highest labeled index — anything past the last annotation is unannotated tail and gets dropped

After this stage, everything is in sample-space, not clock-space. That makes the rest of the pipeline cleaner.

## Stage 2: Sliding Window Extraction

Fixed-length windows are extracted from each indexed session to create uniform training examples.

The configuration:

- **Window size**: 300 time points (after counting overlap → effective 450 time points per window)
- **Stride / overlap**: 50% overlap

For each window, only annotations whose **entire span** falls within the window boundaries are retained. This is important — partial segments on the boundary get dropped. Including only fully-contained segments means each window has clean, complete labels rather than truncated fragments that would confuse the regression head.

## Why That Window Size

300 time points × 50% overlap → 450-point windows on average contain roughly **5 ground-truth segments** each. That number is intentional. Too few and the model doesn't learn temporal context. Too many and individual events get lost in the soup. Five is a sweet spot I converged on through experimentation.

The 50% overlap is also intentional — it ensures that any segment that would have been clipped on a window boundary in one position will be fully contained when a neighboring window slides over it. So no real event gets dropped from the dataset just because of bad alignment.

## Stage 3: Label Coordinate Adjustment

Once a window is extracted, the original segment centers (which are absolute positions in the full session) get adjusted to reflect their offset relative to the **start of the window**. Now each segment's coordinates are window-local.

This produces a set of window-localized labels for every training example.

## Stage 4: Feature-Level Down-Sampling

Before the model ingests the labels, segment centers and lengths are down-sampled by an integer reduction factor (three) to match the network's feature-level resolution.

Why? The CNN backbone reduces the temporal dimension of the input as it processes through layers. The feature map output has fewer time positions than the input, so labels need to live at that lower resolution. Otherwise the regression targets wouldn't align with the predicted positions.

Textual activity names get mapped to numeric class identifiers at the same time.

## Stage 5: Shuffling and Batching

Final preparation before training:

1. Shuffle all the windows randomly to promote stochasticity during training
2. Partition into mini-batches of fixed size (8, in the final config)

Standard stuff but it matters. Without shuffling, the model would see all of one swimmer's data before another's, and that breaks SGD's iid assumption.

## What This Buys Me

Together these preprocessing stages guarantee that the multi-task model receives:
- Uniformly indexed sensor streams
- Precisely localized labels
- Appropriately sized training batches

That's the precondition for the model to do its job — accurate segmentation and classification of swimming activities.

## Lessons from the Pipeline

A few things that ended up mattering more than I expected:

- **Truncating to last labeled index** prevents the model from training on long unannotated tails which would otherwise be classified as background and skew the loss
- **Only retaining fully-contained segments per window** kept the regression targets clean and consistent
- **Down-sampling labels to feature resolution** is one of those gotchas that's easy to miss; if you skip it, the regression head trains on misaligned targets and your loss is much worse than it should be

## Keywords

preprocessing, data pipeline, time alignment, sample index, sliding window, window size, 300 time points, 450 time points, 50% overlap, segment localization, label coordinates, feature-level resolution, down-sampling, mini-batch, shuffling, integer reduction factor, IMU preprocessing, ground-truth alignment
