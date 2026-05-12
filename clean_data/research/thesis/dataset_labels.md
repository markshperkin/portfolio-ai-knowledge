# Dataset: Activity Labels & Annotations

## The Nine Classes

I defined **nine hand-crafted activity labels** to capture all the meaningful phases of a swim session. These weren't arbitrary — each one corresponds to a phase that coaches actually care about and that produces a distinct sensor signature:

1. **Freestyle**
2. **Backstroke**
3. **Breaststroke**
4. **Butterfly**
5. **Underwater glide**
6. **Underwater kick**
7. **Push-off**
8. **Turn**
9. **Wall touch**

Refining these definitions and segment boundaries took real iteration. The goal was to reduce ambiguity and make the data signal as uniform as possible across activities of the same class.

## Stroke Definitions (The Asynchrony Problem)

Because the smartwatch was on the **left wrist**, asymmetric strokes had to be defined relative to left-hand motion:

- **Freestyle and backstroke** — each stroke segment **begins** the moment the left hand initiates its pull phase and **ends** when it returns to the recovery position.

This works fine for athletes who lead with their left hand. It introduces variability when an athlete habitually starts or ends a stroke cycle with their right hand. I accepted this trade-off; you can't capture both arms with one wrist-worn sensor.

For symmetric strokes:

- **Butterfly and breaststroke** — bilateral symmetric motion. Segment boundaries are inherently more consistent across swimmers.

## Turn Definitions (The Hard Part)

Turns were the trickiest class because the rules of swimming itself produce different turn mechanics for different stroke transitions:

**Freestyle & Backstroke — Flip Turns:**
- Segment begins just before the somersault initiates
- Segment ends when feet contact the wall
- Backstroke turns always finish on the back; freestyle turns vary — some land on stomach, some on side, some on back

**Butterfly & Breaststroke — Open Turns:**
- Segment begins at hand-wall contact
- Segment ends when both feet are placed on the wall in streamline position
- Direction (left vs. right) introduces additional labeling variability

**Individual Medley — Backstroke-to-Breaststroke Transition:**
- Segment begins at the moment of single-hand wall contact
- Segment ends when feet are secured in streamline
- Athletes may execute as either an open turn OR a somersault
- Somersaults can be forward or backward
- Open turns can be left or right
- Either hand may contact the wall

That last one is wild. A single class label ("IM transition") covers a huge variety of actual sensor patterns. This was a major source of class noise.

## Push-Off Definition

- Segment begins when both feet contact the wall in streamlined position
- Segment ends when feet leave the wall
- Push-off technique varies by stroke: swimmers may push off lying on their side or stomach, but **backstroke push-offs always occur on the back**

## Underwater Activities

Underwater glide and underwater kick phases are annotated separately. Two main sources of variability here:
- Orientation differs across strokes (back vs. stomach)
- Athlete style differs — some keep their arms stable in streamline, others use their arms to gain momentum

Both are valid technique; both produce different signals.

## Wall Touch Definition

The **rarest class** in the dataset, marking the end of a swim set:
- Segment starts when the swimmer approaches the wall
- Segment ends at the moment of contact

Stroke-specific rules apply:
- **Butterfly and breaststroke** require both hands to contact the wall
- **Freestyle and backstroke** allow single-hand touches — and these can sometimes go unregistered if the athlete touches with the **right** hand (the hand without the watch)

That last point is a real issue. The watch is on the left wrist, so right-hand wall touches produce a much weaker signal than left-hand touches. Class imbalance plus modality blind spot — a tough combo.

## Per-Swimmer Variability

Across all labels, I observed substantial inter-swimmer variability:
- Some swimmers do longer strokes with brief glides between cycles; others initiate stroke cycles continuously
- Kick intensity and arm stability during kicks differ a lot
- Turn variations track with overall technique style

A single activity label can therefore span a wide range of sensor patterns. Capturing the full spectrum demands a larger, carefully balanced dataset. Without sufficient diversity, unrepresented variations will erode both segmentation precision and classification accuracy. I document this honestly because it's a real limitation of the work.

## Class Distribution Summary

Total counts and average frame durations from the train/validation split:

| Class | Train Count | Train Avg Frames | Val Count | Val Avg Frames |
|---|---|---|---|---|
| Butterfly | 317 | 71.59 | 56 | 87.59 |
| Backstroke | 219 | 119.98 | 50 | 142.68 |
| Breaststroke | 285 | 96.28 | 41 | 110.73 |
| Freestyle | 248 | 88.04 | 46 | 109.15 |
| Underwater kick | 818 | 34.77 | 102 | 32.60 |
| Underwater glide | 218 | 46.55 | 35 | 50.31 |
| Push-off | 206 | 32.73 | 31 | 32.23 |
| Turn | 152 | 65.86 | 17 | 68.06 |
| Wall touch | 54 | 42.15 | 11 | 50.18 |

Underwater kicks dominate the dataset because in 25-yard short-course swimming, athletes spend a lot of time kicking off the wall in streamline. Wall touches are rarest because there's only one per set per athlete.

## Keywords

activity labels, annotation, ground truth, stroke definitions, freestyle, backstroke, breaststroke, butterfly, underwater kick, underwater glide, push-off, turn, wall touch, individual medley transition, flip turn, open turn, segment boundaries, class imbalance, inter-swimmer variability, asymmetric strokes, symmetric strokes, segmentation labeling, class distribution
