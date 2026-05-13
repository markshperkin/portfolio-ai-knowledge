# Future Work

## What's Next After This Thesis

I outlined three concrete directions for future work that build on the limitations and gaps identified during this research.

## 1. Address Class Imbalance with More Data

The first priority is tackling the pronounced class imbalance in the dataset. The plan:

**Collect additional examples of rare events**, particularly:
- Wall touches (only ~54 training samples)
- Various turn types (open turns, flip turns, IM transitions in their many forms)

The goal is to equalize the number of samples per class as much as possible. Once a more balanced corpus is assembled, I'd then explore **targeted data augmentation** to further expand the effective dataset size and smooth out residual imbalances.

Promising augmentation directions:
- Time warping for stroke cycles (preserve class but shift duration)
- Sensor noise injection (mimic real-world watch movement)
- Stroke-pair concatenation to synthesize more transition events
- Mirror augmentation for handedness variation

After enrichment, retrain and quantify the gain from sample diversity vs. balance.

## 2. Lap-Time and Set-Time Prediction

The current pipeline detects events but doesn't compute timing analytics. Adding this turns the pipeline from a pure recognition tool into a **comprehensive performance analytics system**.

The technical bridge is straightforward in principle:
- **Lap time = time between consecutive wall pushes** → needs reliable push-off detection
- **Set time = time from initial push-off to final wall touch** → needs both endpoints

These derived metrics would be enormously useful to coaches because they're what coaches actually care about — splits, totals, pacing. The pipeline already produces the inputs (segments with timestamps), so this is mostly engineering.

The accuracy of derived timing depends on push-off and wall-touch detection accuracy, which the input modality study already showed are still weak classes. So this work is coupled with the data-collection effort above.

## 3. Alternative Sensor Placements

The wrist is convenient (everyone owns smartwatches) but has limitations:
- Right-hand wall touches are invisible to a left-wrist sensor
- Wrist motion is dominated by stroke cycles, drowning out signals from turns and push-offs
- Streamline position tucks the wrist near the body, reducing some motion fidelity

Alternative or complementary sensor placements worth investigating:

**Head or goggle-mounted IMUs:**
- More stable reference frame for wall-contact detection
- Cleaner interpretation of underwater-kick and stroke cycle phases
- Less interference from arm motion

**Hybrid configurations:**
- Wrist + head, or wrist + chest
- Compare wrist-only vs. multi-sensor accuracy/cost tradeoffs

The goal is to identify the **optimal mounting strategy** that maximizes accuracy while minimizing disruption to the athlete's natural technique. A goggle sensor might give cleaner data but adds setup friction; a wrist sensor is friction-free but compromises on rare events.

## 4. Real-Time Architecture (Beyond the Thesis Plan)

Although MTHARS delivers strong accuracy, its multi-scale window generator incurs substantial computational overhead, making real-time inference challenging. To address this, future work will investigate **fully sequential, memory-based architectures** — LSTM or GRU networks that ingest raw IMU streams end-to-end without explicit window slicing and pooling.

The benefits of recurrent architectures:
- Inherent temporal modeling without redundant multi-scale extraction
- No anchor-based proposals → no NMS overhead
- Lower per-step compute → potentially mobile-friendly
- Streaming inference is native (next sample → next prediction)

The trade-offs:
- May lose multi-scale flexibility
- Anchor-based event counting is harder to replicate cleanly with frame-level RNNs

This architectural shift promises a simpler pipeline and faster inference on embedded hardware — paving the way for **live, low-latency feedback during swimming training**, which is the long-term vision for the work.

## Bigger Picture

Putting these directions together, the path from "research thesis" to "shipped product" involves:

1. **More data, better balanced** — the model is dataset-limited, not architecture-limited at this point
2. **Derived analytics** — lap times, splits, set times — to give coaches what they actually want
3. **Sensor modality experiments** — figure out the best hardware for the job
4. **Lighter architecture** — make it run on the watch itself, in real time

Each is its own meaningful research project. None requires fundamentally new ML — the core questions are answered. The remaining work is engineering, data collection, and optimization.

## What I'd Personally Want to Do

If I had unlimited time and resources, my priority order would be:
1. **Bigger dataset first** — every other improvement amplifies in proportion to data quality
2. **Recurrent architecture next** — solves the real-time problem, which is the deployment blocker
3. **Goggle-mounted sensor study** — most likely to break through on rare-event accuracy
4. **Lap-time analytics last** — important but mostly engineering once detection is solid

The thesis was a solid step. The product is still ahead.

## Keywords

future work, research directions, class imbalance, data augmentation, time warping, sensor noise injection, lap time prediction, set time prediction, sensor placement, head mounted IMU, goggle mounted IMU, hybrid sensor configuration, real-time inference, LSTM, GRU, recurrent architectures, mobile deployment, streaming inference, MTHARS limitations
