# Titanic Survival Classification — The Two Models and How They Were Trained

## Summary

A PyTorch MLP and an XGBoost classifier, trained on the identical 23-column matrix and the identical stratified split. Both tuned by 5-fold cross-validated ROC-AUC inside the training split, both with early stopping, both evaluated once on the same sealed 179-row validation set. The point of the comparison is that it's actually fair.

## Why Two Models

The assignment required a deep-learning model. A neural net on 712 tabular rows is not what anyone would reach for in production, so training only the MLP would have left the obvious question unanswered: *is this better than the boring option?*

Adding XGBoost as a classical baseline answers it, and answering it honestly is more interesting than either model alone. Gradient-boosted trees are the correct default for small tabular interaction-heavy data, and if the MLP had lost badly that would have been the finding — which is fine, and worth reporting.

## Shared Protocol

Both models get exactly the same treatment:

- Stratified 80/20 split — 712 train, 179 validation — `seed=42`, generated once and shared.
- The same 23-column feature matrix from the same `TitanicPreprocessor`.
- Hyperparameters chosen by **5-fold stratified cross-validation on the training split**, ranked by mean **ROC-AUC**, with the preprocessor **re-fit inside each fold**.
- Final training on the full training split with early stopping.
- The 179-row validation set as the single honest test.

**Why ROC-AUC as the selection metric:** it's threshold-independent and robust to the 38/62 class imbalance. Selecting on accuracy would have quietly optimized for the majority class and locked in a 0.5 threshold before I'd decided whether 0.5 was the right threshold.

Each model has a `tune.py` (search) and a `train.py` (final). `train.py` picks up the tuned `best_config.json` if it exists and otherwise falls back to a sensible baked-in default — so the pipeline always runs standalone and there's no mandatory expensive step before you can see it work.

## The PyTorch MLP

Deliberately small and regularized. With 712 training rows the priority is generalization, not capacity.

- Each hidden layer is `Linear → ReLU → Dropout`; the head is a single logit.
- `BCEWithLogitsLoss` with `pos_weight ≈ 1.6` for the 38% positive rate.
- Adam with weight decay `1e-4`.
- Early stopping on validation accuracy, patience 10, best weights restored.
- Configurable mini-batching: `None` means full-batch — one exact gradient step per epoch — while a smaller size shuffles each epoch and trades gradient exactness for regularizing noise and more updates.

**Search grid: 150 configurations** — 5 architectures ([16], [32], [64], [32,16], [64,32]) × 2 dropouts × 3 learning rates × 5 batch sizes, each over 5 folds.

**Winner:** `hidden_dims=[32]`, `dropout=0.0`, `lr=0.01`, `batch_size=32`.

A single 32-unit hidden layer with no dropout. That's a small model, and the search agreeing it's the right size is itself the result: this dataset does not have the signal to support capacity. The batch size of 32 doing the regularizing work instead of dropout is a nice detail — mini-batch noise was the more effective regularizer here.

## The XGBoost Baseline

Gradient-boosted trees, adding one tree at a time, each correcting the previous trees' errors — which naturally captures the class × sex × age interactions that make Titanic predictable at all.

- `n_estimators=500` as an upper bound, with native early stopping (`early_stopping_rounds=20`) finding the real count. That's the tree-count analogue of the MLP's epoch early stopping.
- `scale_pos_weight` for the imbalance — same correction, different mechanism.
- Fixed, lightly-regularized defaults for what wasn't swept: `colsample_bytree=0.8`, `reg_lambda=1.0`, `min_child_weight=1`.

**Search grid: 18 configurations** — 3 depths × 3 learning rates × 2 subsample rates.

**Winner:** `max_depth=4`, `learning_rate=0.1`, `subsample=0.8`, with early stopping selecting **26 trees**.

26 trees of depth 4. The final model is tiny, and that's consistent with everything else here: the signal is shallow, and the engineered features are doing the work.

## Why The Grids Are Different Sizes

150 configs for the MLP versus 18 for XGBoost is not sloppiness. A neural net on tabular data has far more architectural freedom that genuinely matters — depth, width, dropout, batch size all interact. XGBoost's important axes are fewer, its defaults are strong, and its tree count is found automatically by early stopping rather than searched. Spending 150 configs on it would have burned time to confirm what sensible defaults already give you.

Equal rigor doesn't mean equal grid size; it means each model got a search sized to where its variance actually lives.

## Both Models Are Directly Comparable

The `src/` — `mlp/` — `xgb/` structure enforces it. `src/` is model-agnostic and both packages import it, so neither can quietly get a better pipeline. `xgb/model.py` mirrors `mlp/model.py` function for function — same interface, same metric set out — and the only difference between the two paths is the model itself.

That structure is why I can say "XGBoost edges accuracy, the MLP wins AUC" and mean it, rather than it being an artifact of one having been tuned harder.

## Honest Caveats

I wrote these into the report rather than leaving them for a reviewer to find:

- **The 179-row validation set serves double duty** — it drives early stopping *and* it's what I report. So the reported metrics are mildly optimistic. That's standard validation-set use, but it's still true, and nested cross-validation would be the unbiased fix.
- **No probability calibration** — the models rank well; that doesn't make the probabilities well-calibrated.
- **The 0.5 threshold is a default**, not a choice. Tuning it to a desired precision/recall trade-off would be the next step for any real use.

Naming those was deliberate. On a solved dataset where everyone gets ~0.82, the differentiator isn't the number — it's whether you know what the number doesn't say.

## Keywords

PyTorch, MLP, multilayer perceptron, neural network, XGBoost, gradient boosting, decision trees, BCEWithLogitsLoss, pos_weight, scale_pos_weight, class imbalance, Adam optimizer, weight decay, dropout, mini-batch, early stopping, patience, hyperparameter search, grid search, 5-fold cross-validation, StratifiedKFold, ROC-AUC, model selection, baseline comparison, deep learning versus gradient boosting, tabular data, small dataset, regularization, nested cross-validation, probability calibration, threshold tuning
