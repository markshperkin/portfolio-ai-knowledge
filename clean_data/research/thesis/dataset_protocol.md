# Dataset: Collection Protocol

## The Athletes

Eleven collegiate-level swimmers from the **University of South Carolina Swim & Dive Team**, ages 18 to 30. These were real Division I athletes, not casual swimmers. That matters — I needed clean, repeatable technique to learn from, and recreational swimmers wouldn't give me that.

I ran the data collection sessions with cooperation from the USC coaching staff: Jeff Poppell, Jason Calanog, and Nils Wich-Glasen. Without their backing this dataset wouldn't exist.

I served as the held-out subject for the leave-one-subject-out validation — meaning my own swims were used as the test set the model never saw during training.

## The Protocol

Every athlete did the same thing:

- **Five 100-yard sets**, one per stroke
- Strokes covered: **freestyle, backstroke, breaststroke, butterfly, individual medley (IM)**
- All performed in a **25-yard pool**
- Pace: comfortable moderate effort
- Rest: approximately 30 seconds between sets

That's a four-stroke matrix plus IM, so each swimmer produced about 500 yards of labeled data. Across eleven swimmers that's a meaningful corpus, even if it's small by general HAR standards.

## Athlete Instructions

Two important guardrails when I gave them the protocol:

1. **Use your normal underwater-kick routine.** I didn't want them faking dolphin kicks they wouldn't normally do. Real-world variability is part of the data.
2. **Maintain consistent stroke technique.** Don't try to "perform" for the watch — just swim like you swim.

This is a tradeoff. I got more authentic data, but it means the dataset captures more inter-swimmer variability than a strictly controlled lab study would.

## What Went Wrong (And How I Fixed It)

During the initial data transfer, **a small number of recordings were corrupted**. This is the kind of thing that happens with consumer hardware in a wet environment — flaky writes, file system hiccups, whatever. I dealt with it by going back and running additional stroke-specific sessions with a subset of athletes to recover those data points.

The lesson: data collection in real environments is messy. Build redundancy into your protocol from day one. I learned that the hard way and would do it differently next time — likely with on-watch checksums and immediate post-session validation before athletes leave the pool.

## Why a 25-Yard Pool

USC's home facility is a 25-yard short-course pool. That's also the standard for NCAA dual meets, so the data reflects realistic competitive distances. It also means lots of turns relative to stroke cycles, which made the dataset rich in lap-transition events — important because turns and push-offs are the rare classes I most needed to learn.

## Keywords

data collection, protocol, USC Swim and Dive, collegiate swimmers, eleven athletes, 100-yard sets, butterfly, backstroke, breaststroke, freestyle, individual medley, IM, 25-yard pool, leave-one-subject-out, LOSO, validation methodology, Jeff Poppell, Jason Calanog, Nils Wich-Glasen, data corruption, recovery sessions, real-world data collection
