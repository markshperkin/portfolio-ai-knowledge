# Titanic Survival Classification — Decisions, Challenges, and Lessons

## Summary

A one-day take-home on a solved dataset. The technical work isn't hard; deciding what to spend the day *on* is. This is the "why X over Y" reference plus the problems I actually hit. **It passed and I moved to the next interview round.**

## The Core Bet

Titanic has a well-known accuracy ceiling around 0.80–0.83. Any competent submission lands there. So the number can't be the differentiator — the **pipeline discipline around it** has to be.

I spent the day on four things:

1. Two models on a provably identical pipeline, so the comparison is fair.
2. Leakage-free preprocessing, including inside CV folds.
3. Explainability that answers "why this passenger?", not just "which features matter."
4. A real inference app sharing the *same fitted preprocessor* as training.

And explicitly not on: a third model, a hyperparameter optimization framework, ensembling, or squeezing out another half point of accuracy. In one day, adding any of those means cutting one of the four — and the four are what a reviewer can't get from a Kaggle kernel.

## Decision: Two Models Instead Of One

The brief required a deep-learning model. A neural net on 712 tabular rows isn't what anyone would reach for in production, which leaves the obvious question hanging: is it better than the boring option?

Adding XGBoost answers it. If the MLP had lost badly, that would have been the finding and I'd have reported it. As it happens they're within a point of each other, which produces a more interesting conclusion than either model alone: the features, not the model, are doing the work.

## Decision: Structural Fairness Via `src/`

The `src/` — `mlp/` — `xgb/` layout isn't organizational tidiness, it's the guarantee that makes the comparison meaningful. Everything model-agnostic (load, split, features, preprocessing) lives in `src/`; both model packages import it. Neither can quietly get a better pipeline.

`xgb/model.py` deliberately mirrors `mlp/model.py` function for function — same interface in, same metric dict out. The only difference between the two paths is the model.

## Decision: ROC-AUC For Model Selection

Threshold-independent and robust to the 38/62 imbalance. Selecting on accuracy would have optimized for the majority class and baked in a 0.5 threshold before I'd decided 0.5 was right. It wasn't — that's a flagged follow-up.

## Decision: Pinned Category Vocabularies

The one-hot encoder is given explicit category lists, so output is always the same 23 columns in the same order. Without it, a CV fold missing a rare title produces 22 columns and the model silently trains on misaligned features; or single-row inference crashes on a shape mismatch.

Small piece of code, whole class of bugs prevented. This is the kind of thing you only write if you've been bitten before.

## Decision: Serialize The Fitted Preprocessor

Saved with `joblib` next to the model and reloaded by the Streamlit app. Training and inference share exactly one pipeline object rather than two implementations that are supposed to agree.

Train/serve skew is the classic way a good model becomes a bad product. Serializing the fitted object makes the skew impossible instead of merely unlikely — and it's maybe five lines.

## Decision: `train.py` Runs Standalone

The tuning step is optional. `train.py` uses `best_config.json` if it's there and a baked-in default otherwise. A reviewer can clone and run one command and get a trained model, without first sitting through a 150-config × 5-fold search.

Making the expensive step optional rather than mandatory is a small kindness to whoever runs your code, and on a graded submission it's the difference between "it worked" and "I'll try later."

## Challenge: FareRank For Single-Row Inference

A fare percentile computed within the input batch is meaningless when the batch is one passenger — you'd get 1.0 every time.

**Fix:** the preprocessor stores sorted training fares per Pclass as a reference, and any new fare is ranked against that stored reference by binary search, with a global-distribution fallback for an unseen Pclass. One row or a thousand, the feature means the same thing.

**Lesson:** for every engineered feature, ask *when* it will be computed, not just what it means. Features that depend on the shape of the input batch are a trap that only springs at inference time.

Interestingly, `TicketGroupSize` goes the other way on purpose — it's counted within the given frame, because "how many people share this ticket" genuinely is a property of the passenger set you're looking at. A lone passenger gets 1, which is correct. Same question asked, opposite answer, both deliberate.

## Challenge: Age Imputation That Doesn't Lie

Filling missing ages with the global median puts a `Master` — a young boy — at 28 years old, in a dataset where young boys survived at a completely different rate than adult men. That's not a missing value handled; that's a wrong value inserted into the most predictive corner of the data.

**Fix:** median age by Title group, falling back to global. The engineered feature improves the imputation of a raw one, which is a nice illustration that feature engineering and cleaning aren't separate phases.

## Challenge: One-Hot Columns Wrecking Explainability

Spread across seven one-hot columns, `Title` looked weak in every importance chart — while being the single strongest predictor. A human reads `Title` as one feature; the matrix has it as seven.

**Fix:** a grouping toggle that maps each conceptual feature to its column indices and collapses both permutation importance and SHAP contributions back to the parent — 12 features instead of 23 columns.

**Lesson:** an explanation that doesn't match how a person thinks about the data isn't an explanation. Getting this right is what turned the charts from "technically correct" to "actually convincing."

## Challenge: Leakage Inside CV Folds

Fitting the preprocessor once on the full training split and reusing it across folds is the standard, easy mistake — the fold's validation rows influenced the scaler and the imputation values, so the CV score comes out optimistic.

**Fix:** a fresh `TitanicPreprocessor` fit on each fold's training rows only. A few extra lines and noticeably slower, and it's the difference between a CV number I trust and one I don't.

## Lesson: Report The Caveats

I wrote into the report that the 179-row validation set serves double duty (early stopping *and* reporting), so the metrics are mildly optimistic; that SHAP uses an independent-feature masker; that IsAlone and FamilySize are redundant; and that there's no decisive winner between the two models.

On a solved dataset, saying what your number doesn't mean is more differentiating than the number. A reviewer who spots an unstated caveat assumes you missed it. A reviewer who reads it stated assumes you understand your own pipeline.

## What I'd Do Differently

- **Nested cross-validation** for an unbiased performance estimate, instead of a validation set doing two jobs.
- **Probability calibration** — the models rank well; that's not the same as well-calibrated probabilities.
- **Threshold tuning** to an explicit precision/recall trade-off rather than the 0.5 default.
- **Prune the redundant features** — the importance analysis already says which ones.

## Keywords

technical decisions, trade-offs, take-home assessment, scope management, model comparison, fair comparison, code structure, shared pipeline, ROC-AUC selection, pinned categories, one-hot encoding, joblib serialization, train-serve skew, data leakage, cross-validation leakage, FareRank, single-row inference, age imputation, grouped imputation, SHAP grouping, explainability, honest reporting, caveats, nested cross-validation, calibration, threshold tuning, feature pruning, lessons learned, data scientist interview
