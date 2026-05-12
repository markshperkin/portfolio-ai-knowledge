# Lessons Learned

## What Surprised Me

A few things I didn't expect going in.

### Single-Metric Optimization is a Trap
The hard-negative-mining experiment was the clearest teacher. R = 1.5 produced a beautiful 0.96 micro-F₁ — and a catastrophic 0.11 mean IoU and 0.22 macro-F₁. If I had only tracked one metric, I would have shipped a broken model that "looked great" on paper.

Always track multiple metrics that capture different failure modes. In detection: at minimum, F₁ scores both ways (micro and macro), plus a localization metric (mean IoU). One metric is a recipe for fooling yourself.

### Gyroscope Adds Most Value Where You Need It Most
I expected the gyroscope to add a uniform improvement across all classes. It didn't. It barely changed performance on the dominant strokes (which were already strong with the accelerometer alone) but made enormous differences on the rare classes — push-off F₁ jumped from 0.062 to 0.455.

This is actually really useful from a deployment perspective: if your sensor budget is constrained, you might be able to drop the gyroscope and still get great stroke classification, but you'd lose your ability to detect lap transitions. The sensor matters most for the events you're worst at.

### Class Imbalance Bites Harder Than I Expected
With 818 underwater-kick samples and 54 wall-touch samples, the imbalance is roughly 15:1. Even with hard negative mining and class-balanced loss weighting, the model can't fully overcome that ratio. Wall touches stayed weak throughout.

Lesson: don't assume mining + weighted loss "fixes" imbalance. Past a certain ratio, you need more data, not better tricks.

## What I'd Do Differently

### Run More Seeds
I reported single-run results. Some of the differences between hyperparameter configurations are probably within seed-to-seed noise. Multiple seeds with mean ± std would have given the experiments more authority.

### Build in Data-Collection Redundancy from Day One
The fact that several recordings got corrupted during initial data transfer was avoidable. On-watch checksums + immediate post-session validation would have caught it before athletes left the pool. I had to schedule re-collection sessions to recover, which was both expensive in coordination effort and stressful.

### Reconsider My LOSO Held-Out Choice
I served as the held-out subject for leave-one-subject-out validation. That's non-standard. While it doesn't bias the model (the model never trains on me), it does mean my swims are the test set. If my technique differs from the average athlete's, the reported numbers might not reflect typical generalization. A more rigorous setup would rotate the held-out subject across all 11 athletes and average. I had time and compute constraints that pushed me toward the simpler version.

### Tune τ and R Iteratively
I tuned τ first, then held it at 0.5 while tuning R. But the optimal τ might shift after R is set. A more iterative search (or a small joint sweep over τ and R) would have been more thorough.

## What I'd Tell Someone Starting Similar Work

### On Anchor-Based Detection for Time Series
- It's the right framing if you need bounded events you can count
- Multi-scale anchors are essential when event durations span an order of magnitude
- Hard negative mining is non-negotiable for problems with dominant background class
- Track both micro and macro F₁ from day one

### On Working with Athletes
- Coaches will help if you respect their time. Show up early, be ready, don't drag the session out
- Athletes will give honest data if you tell them to swim normally and mean it
- Build redundancy into data collection; consumer hardware in wet environments is flaky
- Annotation is the bottleneck, not training. Plan for it.

### On Single-Sensor Constraint
- The big practical reason to use one sensor is that anything more than one is a deployment killer
- The big technical reason is that it forces honest representation learning — you can't lean on cross-sensor disambiguation
- Accept that you'll do worse on some classes (right-hand wall touches with a left-wrist sensor), and document those limitations honestly

## On Writing the Thesis Itself

The thesis writing pushed me to defend choices I had made implicitly. Several of the hyperparameter ablations only happened because writing them up forced me to ask "wait, why did I pick that value?" — and discovering the answer was "because the default seemed reasonable" wasn't satisfying.

Writing forces clarity. Don't avoid it.

## On Open-Source / Open-Science

The thesis is published open-access in USC's Scholar Commons. The dataset and code are not yet public — partly because I want to clean them up before release. That's a personal lesson: build for openness from day one, don't promise yourself you'll clean up later.

## Keywords

lessons learned, reflections, single-metric trap, multi-metric evaluation, gyroscope value, class imbalance lessons, data collection redundancy, LOSO methodology, hyperparameter tuning iteration, anchor-based detection lessons, single-sensor design, athlete data collection, thesis writing, open science, reproducibility
