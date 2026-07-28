# Titanic Survival Classification — Overview

## Summary

An end-to-end, reproducible machine-learning pipeline that predicts Titanic passenger survival from the Kaggle `train.csv`. It covers data loading, exploratory analysis, leakage-free preprocessing, **two competing models** — a PyTorch MLP and an XGBoost baseline — trained by standalone scripts, plus a Streamlit inference app with metrics, plots, and model explainability via permutation importance and SHAP.

I built it as a timed take-home for a data scientist role, with a **one-day window**. **It passed and I was moved to the next interview round.**

GitHub: https://github.com/markshperkin/titanic-survival-classification

## What The Assignment Asked For

A classic setup: take the Titanic dataset, build a deep-learning model, make it runnable, show your work. Only `train.csv` is used — the train/validation split is created in code so both models are evaluated on exactly the same held-out rows.

The part that isn't stated but is obviously what's being tested: can you build something *reproducible and honest*, or do you just get a number? Titanic is a solved problem with a well-known accuracy ceiling around 0.80–0.83. Nobody is impressed by 0.82 accuracy. What they're reading is the pipeline discipline underneath it.

## How I Approached It

I decided early that the differentiators would be:

1. **Two models on an identical pipeline**, so the comparison is actually fair rather than two separately-tuned things with different preprocessing.
2. **Provable absence of leakage** — every learned statistic fit on training rows only, including inside each cross-validation fold.
3. **Explainability that answers "why this passenger?"**, not just "which features matter."
4. **A deployable artifact** — a Streamlit app that loads the *same* fitted preprocessor from disk, so training and inference genuinely share one pipeline.

Given one day, that's a scope I could finish properly. Adding a third model or a hyperparameter framework would have meant cutting one of the four.

## The Headline Result

On a held-out 179-passenger validation set:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Majority baseline ("all died") | 0.6145 | – | – | – | – |
| **PyTorch MLP** | 0.8212 | 0.7467 | **0.8116** | 0.7778 | **0.8551** |
| **XGBoost** | **0.8324** | **0.7826** | 0.7826 | **0.7826** | 0.8432 |

Both land roughly 20 points over the majority-class baseline and near the known Titanic ceiling. There's no decisive winner: XGBoost edges accuracy and F1 with a tidy 26-tree model, the MLP wins ROC-AUC — better-calibrated ranking of survival probability.

The finding I actually care about: **feature engineering, not model choice, drove performance.** The engineered `Title` feature is the strongest predictor for both models by a wide margin.

## Project Structure

```
src/                 shared, model-agnostic pipeline
  data.py            load_raw() — local-first, Kaggle API fallback
  split.py           stratified train/val split, shared by both models
  features.py        stateless feature engineering (Title, FamilySize, …)
  preprocessing.py   TitanicPreprocessor — fit-on-train → 23-column matrix; save/load
mlp/                 PyTorch deep model
  model.py           MLP, train loop (early stopping, mini-batch), evaluate
  tune.py            5-fold CV grid search (150 configs) → best_config.json
  train.py           final train → mlp.pt + preprocessor.joblib
xgb/                 XGBoost classical model — same three-file shape
notebooks/01_eda.ipynb   exploratory analysis, 8 sections, runs clean top-to-bottom
ds_app.py            Streamlit inference + explainability app
```

The `src/` — `mlp/` — `xgb/` split is the structural decision that makes the comparison honest. Everything model-agnostic lives in `src/` and both model packages import it. Neither model can quietly get a better pipeline than the other.

## The Stack

pandas, numpy, scikit-learn, PyTorch, XGBoost, SHAP, Streamlit, matplotlib/seaborn, Jupyter, and the Kaggle API for the data fallback.

## Reproducibility

- Deterministic stratified split, `seed=42`, written to disk and reused unless `--force`.
- Python, NumPy, and torch all seeded.
- `train.py` runs standalone with a baked-in default config, and picks up the tuned `best_config.json` if the search has been run — so the pipeline never has a step you're *required* to run first.
- The fitted preprocessor is saved with the model and reloaded by the app.

That last one is the piece people skip. A model artifact without its fitted preprocessor isn't reproducible inference — it's a set of weights and a hope that you re-derive the same 23 columns.

## Keywords

Titanic, Kaggle, binary classification, survival prediction, machine learning pipeline, PyTorch, MLP, neural network, XGBoost, gradient boosting, scikit-learn, pandas, feature engineering, data leakage, cross-validation, stratified split, ROC-AUC, SHAP, permutation importance, explainability, Streamlit, reproducibility, take-home assessment, data scientist interview, passed to next interview round
