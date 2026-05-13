# Results

## Validation Accuracy

The implemented ST-GCN model achieved **peak validation accuracy of 87.6%** by epoch 49 on NTU RGB+D, evaluated across **49 different action classes** with an 80/20 train/validation split.

The training and validation accuracy curves (Figure 4 in the paper) show clean convergence — both metrics rising steadily without divergence, indicating no significant overfitting. Training and validation loss (Figure 5) decrease monotonically with the LR drops at epochs 30 and 40 producing the expected stepwise improvements.

## Comparison to Literature

Per the original ST-GCN paper, the architecture achieves on NTU RGB+D:
- **Cross-subject (X-sub)**: 84.5%
- **Cross-view (X-view)**: 92.2%

These compare with heavier GCN variants like 2s-AGCN, which hits 88.5% / 95.1% — slightly higher but with larger model size and compute requirements.

My **87.6% validation accuracy** falls within the range expected for this architecture and validates the implementation. The literature uses different evaluation protocols (X-sub vs. X-view splits) than my simple 80/20, so direct comparison isn't apples-to-apples — but the magnitude is right.

## Edge Hardware Performance

The original paper measured ST-GCN's inference speed on an **NVIDIA Jetson Nano**, where it processes **993 frames per second**. That's far more than enough for live, real-time deployment in IoMT (Internet of Medical Things) settings or other resource-constrained environments.

I conducted my own inference speed measurements on different hardware:

### NVIDIA RTX 4070 Super (GPU)
- Average latency per batch: 0.156s (±0.015s)
- Average latency per sample: 0.0097s
- Throughput: **102.8 samples/sec**

### Intel i7-14700F (CPU)
- Average latency per batch: 2.354s (±0.037s)
- Average latency per sample: 0.147s
- Throughput: **6.8 samples/sec**

Each sample contains **300 frames**. So the GPU effectively processes ~30,000 frames per second, and the CPU processes ~2,000 frames per second.

| Device | Avg Latency/Batch | Avg Latency/Sample | Throughput |
|--------|------------------|-------------------|------------|
| GPU (RTX 4070 Super) | 0.156s | 0.0097s | 102.8 samples/s |
| CPU (i7-14700F) | 2.354s | 0.147s | 6.8 samples/s |

## What These Numbers Mean

### Edge Deployment is Viable
Even on CPU only (i.e., no GPU acceleration), ST-GCN processes ~2,000 frames per second. For real-time applications running at typical video frame rates (30-60 FPS), this is **30-60x faster than required**. The architecture is unambiguously deployable on edge hardware.

### GPU Acceleration is Worth It
The GPU is ~15x faster than CPU. For applications that process many parallel streams (e.g., security camera surveillance, multi-patient monitoring), GPU is the right choice. For single-stream applications (one wearable, one user), CPU is more than sufficient.

### Real-World Implications
ST-GCN can run in:
- **Smartphones** — CPU-class throughput is plenty for one user's action stream
- **Smart watches** — would need optimization but is in the realm of feasible
- **Embedded medical monitors** — Jetson Nano-class boards run at near-real-time
- **Surveillance servers** — GPUs can handle dozens of simultaneous streams

## Confirming Edge Feasibility

The combined results confirm that **ST-GCN's adaptive spatial-temporal architecture delivers competitive accuracy at a fraction of size and cost**, making it well suited for on-device inference.

This is exactly what the original wearable system was meant to enable — but couldn't, due to hardware sensor failures. The ML side delivers the deployability vision; the hardware side just couldn't catch up.

## Why These Results Matter

A few reasons these numbers are meaningful beyond the headline accuracy:

### 1. Independent Validation
Reproducing literature results from scratch (different hardware, different framework setup, different train/val split) and getting comparable numbers validates the architecture's robustness. Many published methods don't replicate cleanly. ST-GCN does.

### 2. Real-World Hardware Benchmarks
The original paper used Jetson Nano. I measured RTX 4070 Super (modern consumer GPU) and i7-14700F (modern consumer CPU) — much closer to what real users would deploy on. These benchmarks complement the original measurements.

### 3. Multi-Class Capability
49 distinct action classes is a meaningful classification space. Single-class detection or binary classification is much easier than 49-way classification — the 87.6% result reflects genuine multi-class capability, not a degenerate case.

### 4. Application-Ready
The combination of competitive accuracy + edge feasibility means ST-GCN is ready for real applications, not just research demos. That's the bar the original wearable project was trying to clear.

## Limitations of These Results

A few honest caveats:

- **Single train/val split** — multiple cross-validation runs would reduce variance in reported numbers
- **NTU RGB+D only** — generalization to other datasets (Kinetics, smaller domain-specific corpora) wasn't tested
- **No hyperparameter tuning** — I followed the literature's settings; my own tuning might have improved the 87.6% number
- **Inference benchmarks are point estimates** — measured on specific hardware with specific batch configurations; production deployment numbers may vary

## Keywords

results, accuracy, validation accuracy, 87.6%, NTU RGB+D, classification accuracy, edge inference, latency benchmarks, throughput, GPU performance, CPU performance, RTX 4070 Super, i7-14700F, Jetson Nano, real-time inference, edge deployment, model efficiency, ST-GCN benchmarks
