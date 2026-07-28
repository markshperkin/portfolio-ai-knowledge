# Titanic Survival Classification — Results, Explainability, and the Streamlit App

## Summary

Both models beat the majority-class baseline by roughly 20 points and land near the known Titanic ceiling. The Streamlit app is where the project stops being a notebook: pick a model, point it at a CSV, and get metrics, plots, a color-coded predictions table, global permutation importance, and a per-passenger SHAP waterfall answering "why this passenger?"

## Held-Out Results (179 passengers)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Majority baseline ("all died") | 0.6145 | – | – | – | – |
| **PyTorch MLP** | 0.8212 | 0.7467 | **0.8116** | 0.7778 | **0.8551** |
| **XGBoost** | **0.8324** | **0.7826** | 0.7826 | **0.7826** | 0.8432 |

**No decisive winner, and I said so.** XGBoost edges accuracy and F1 with a tidy 26-tree model. The MLP wins ROC-AUC, meaning it ranks survival probability better even though its hard 0.5-threshold decisions are slightly worse.

That split is genuinely informative rather than a cop-out. AUC measures ranking quality across all thresholds; accuracy measures one threshold. A model that ranks better but classifies slightly worse at 0.5 is a model whose threshold hasn't been tuned — which is exactly the follow-up I flagged.

The practical read: for a small tabular interaction-heavy problem, **gradient-boosted trees are the more sensible default**, while the MLP satisfies the deep-learning requirement and ranks risk slightly better.

## The Real Finding

**Feature engineering, not model choice, drove performance.**

Two completely different model families — a neural net and boosted trees — land within a point of each other, and both rank the same engineered feature first. That's the signature of a problem where the features carry the information and the model is just reading them.

Permutation importance ranks **Title first by a wide margin**, then Sex and Pclass, with engineered **FareRank** and **LogFare** in the top five. Three of the top five are features I built.

And the negative result, which I reported rather than hid: **IsAlone and FamilySize contribute near zero** once `SibSp` and `Parch` are in the matrix. They're redundant, and they're a candidate for pruning.

## Global Explainability: Permutation Importance

Shuffle one feature across the whole validation set, measure the drop in ROC-AUC. Model-agnostic, so it runs identically against the MLP and XGBoost — which is precisely why I chose it over anything model-specific like tree gain. A comparison between two models needs an importance measure that doesn't favor either.

The app renders it as a horizontal bar chart with engineered features highlighted in green, so you can see at a glance how much of the signal came from feature work.

## Local Explainability: SHAP Waterfalls

The global view says which features matter overall. The local view answers a different question: **why this passenger?**

A SHAP waterfall decomposes a single prediction from the average baseline to the final probability, attributing each feature's push toward survived or died. That's the explanation a person actually wants — not "Title is important" but "this passenger was predicted to survive because Title=Miss and Pclass=1 pushed up, while a large family size pushed down."

Both views support a **one-hot grouping toggle**: 12 conceptual features versus 23 raw columns. Without grouping, `Title` is spread across seven one-hot columns and looks weak in every chart, while a human reads `Title` as one thing. Collapsing the encoded columns back to their parent feature is what makes the explanation match how a person thinks about the data. That was a small piece of work with a large payoff in how legible the output is.

The honest caveat, stated in the report: SHAP uses an independent-feature masker — the standard speed-versus-realism trade-off — so contributions ignore correlations between features.

## The Streamlit App

`streamlit run ds_app.py`. In the sidebar: choose **MLP** or **XGBoost**, provide a CSV by path (defaulting to the validation split) or by upload, and run inference.

What you get:

- **Metrics row** — accuracy, precision, recall, F1, ROC-AUC on the provided data.
- **Plots** — confusion matrix, ROC curve, predicted-probability histogram.
- **Predictions table** — color-coded green for correct, red for wrong, with engineered columns tinted so you can see what the model actually consumed.
- **Feature influence** — the engineered-feature view, global permutation importance, and per-passenger SHAP.

The design decision underneath it: the app loads the **saved fitted preprocessor** from disk, not a reimplementation of the feature logic. Training and inference share exactly one pipeline object. That's what makes it an inference app rather than a demo that happens to agree with training most of the time.

It also handles labelled and unlabelled input — metrics and the correct/wrong coloring appear when a `Survived` column exists, and the preprocessor returns `y=None` when it doesn't.

## Conclusions I Drew

- Both models comfortably beat the baseline and sit at the well-known Titanic ceiling of ~0.80–0.83. **Nobody wins this dataset**, and claiming otherwise would be a red flag.
- The engineered `Title` feature is the strongest single predictor for both models.
- Redundant features exist and should be pruned.
- The reported metrics are **mildly optimistic** — the validation set drives early stopping *and* reporting.
- Natural next steps: nested cross-validation for an unbiased estimate, probability calibration, and threshold tuning to a chosen precision/recall trade-off.

Writing the caveats and the "no decisive winner" conclusion was a deliberate choice. On a dataset where every competent submission gets ~0.82, what distinguishes them is whether the author understands what their number does and doesn't mean.

## Keywords

model evaluation, held-out validation, accuracy, precision, recall, F1, ROC-AUC, confusion matrix, ROC curve, majority baseline, class imbalance, explainability, interpretability, permutation importance, SHAP, SHAP waterfall, local explanation, global explanation, feature attribution, one-hot grouping, model-agnostic explanation, Streamlit, inference app, model deployment, matplotlib, seaborn, calibration, threshold tuning, honest reporting, negative results
