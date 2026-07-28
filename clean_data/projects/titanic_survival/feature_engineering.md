# Titanic Survival Classification — Feature Engineering and Leakage Control

## Summary

Six engineered features turn the raw Titanic columns into a 23-column matrix. The model never sees raw text — `Name`, `Ticket`, and `Cabin` are transformed or dropped. Every learned statistic (imputation values, scaler, encoder, fare reference) is fit on the training split **only**, including inside each cross-validation fold. This is the part of the project I'd defend hardest, because it's where the accuracy actually came from and where most Titanic notebooks quietly leak.

## The Six Engineered Features

| Feature | Built from | Definition and rationale |
|---|---|---|
| **Title** | `Name` | Honorific extracted by regex (Mr, Mrs, Miss, Master, Dr, Rev; everything rare → Other). A strong proxy for sex, age, and social class simultaneously. |
| **FamilySize** | `SibSp` + `Parch` + 1 | Total family aboard including self. |
| **IsAlone** | `FamilySize` | 1 if travelling alone — captures a non-linear survival effect that family size alone doesn't express. |
| **TicketGroupSize** | `Ticket` | How many passengers share a ticket — groups that boarded and travelled together. |
| **LogFare** | `Fare` | `log(1 + Fare)` — compresses a heavy right skew. |
| **FareRank** | `Fare`, `Pclass` | Fare percentile 0–1 **within the same Pclass** — relative wealth, comparable across classes. |

**Title** is the interesting one, and it turned out to be the single strongest predictor for both models. "Braund, Mr. Owen Harris" → `Mr`. It encodes sex, rough age band, and social standing in one categorical, and it does something the raw columns can't: `Master` identifies young boys, who survived at a very different rate than adult men, even though `Sex` says "male" for both. That's information sitting in a text column most pipelines throw away.

**FareRank** was designed with a specific constraint in mind: it has to work for **single-row inference**. A naive percentile computed within the input batch is meaningless when the batch is one passenger. So the preprocessor stores the sorted training fares per Pclass as a reference, and any new fare is ranked against that stored reference via binary search. One row or a thousand, the feature means the same thing.

**TicketGroupSize** goes the other way deliberately — it's counted *within the given frame*, because it's a property of whichever set of passengers you pass in. That matches the inference case: the app receives a CSV and counts groups within it; a lone passenger gets 1.

Getting those two right meant thinking about *when* each feature would be computed, not just what it means.

## Imputation

All fit on train only:

- **Age** → median **by Title group**, falling back to a global median. Imputing a `Master` with the overall median age would put a child at 28. Grouping by title makes the fill class-appropriate.
- **Embarked** → mode (S).
- **Fare** → median, applied *before* `LogFare` and `FareRank` are derived, so downstream features never see a NaN.

## Encoding: Pinned Vocabularies

Seven numeric features standardized (z-score), `IsAlone` passed through, four categoricals one-hot encoded — with **explicitly pinned category vocabularies**:

```python
CATEGORIES = [
    ["female", "male"],                                     # Sex
    [1, 2, 3],                                              # Pclass
    ["C", "Q", "S"],                                        # Embarked
    ["Dr", "Master", "Miss", "Mr", "Mrs", "Other", "Rev"],  # Title
]
```

Output is **always the same 23 columns in the same order**, even when a small CV fold happens to contain no `Rev`, or an inference batch is a single passenger with no `Dr`. Without pinning, a fold with a missing rare title produces a 22-column matrix and the model silently trains on misaligned features — or the app crashes on a shape mismatch at inference.

This is a small piece of code that prevents an entire category of subtle, hard-to-diagnose bugs. It's also the kind of thing you only think of if you've been burned by it.

## No Leakage, By Design

The rule: **every learned statistic comes from training rows only.**

- The `TitanicPreprocessor` learns imputation values, the fare reference, the scaler, and the encoder from `fit(train_df)` and nothing else.
- Inside cross-validation, a **fresh preprocessor is fit on each fold's training rows** — not fit once on the whole training split and reused across folds. That distinction is exactly where most CV pipelines leak: refitting per fold is a few extra lines and it's the difference between an honest CV score and an optimistic one.
- The 179-row validation split is never touched during hyperparameter search. It stays sealed as the single honest test.

## Stateless vs Stateful, Split By File

The codebase enforces the separation structurally:

- **`src/features.py`** — pure transforms. No fitting, no learned state, no use of the target. Identical behavior at train and inference time.
- **`src/preprocessing.py`** — everything that must *learn* from the training split: imputation values, scaler, encoder, the FareRank reference.

If a function lives in `features.py` it cannot leak, because it has nothing to leak from. That's a structural guarantee rather than a convention you have to remember, and it made reviewing my own work fast.

## One Pipeline, Train And Inference

The fitted `TitanicPreprocessor` is saved to disk with `joblib` alongside the model, and reloaded by the Streamlit app. Training and inference share **exactly one** feature pipeline object — not two implementations that are supposed to agree.

Train/serve skew is the classic way a good model becomes a bad product. Serializing the fitted preprocessor makes the skew impossible rather than unlikely.

## What The Explainability Confirmed

Permutation importance ranked **Title first by a wide margin**, then Sex and Pclass, with the engineered **FareRank** and **LogFare** in the top five. Three of the top five features are ones I built.

It also showed something worth acting on: **IsAlone and FamilySize contribute near zero** once `SibSp` and `Parch` are present. They're redundant — a candidate for pruning. I put that in the write-up rather than leaving the feature list looking uniformly useful, because a feature set you haven't pruned is a feature set you haven't understood.

## Keywords

feature engineering, Titanic, Title extraction, honorific, FamilySize, IsAlone, TicketGroupSize, LogFare, FareRank, percentile ranking, imputation, median imputation by group, one-hot encoding, pinned categories, category vocabulary, standardization, z-score, StandardScaler, OneHotEncoder, data leakage, leakage prevention, fit on train only, cross-validation folds, train-serve skew, joblib, sklearn preprocessing, stateless transforms, feature importance, feature pruning
