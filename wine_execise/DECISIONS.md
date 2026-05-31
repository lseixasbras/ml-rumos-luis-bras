# Wine Classification — Project Decisions & Considerations

## 1. Model Selection

### Models Chosen for Comparison

| Model | Why |
|-------|-----|
| **Logistic Regression** | Linear baseline; fast, interpretable, works well when features are scaled. Good reference point to measure if more complex models add value. |
| **Random Forest** | Ensemble of decision trees; handles feature interactions without scaling, robust to outliers. Low tuning effort for strong results. |
| **XGBoost** | Gradient boosting; typically top performer on tabular data. Captures non-linear patterns with regularization to prevent overfitting. |
| **SVM (RBF kernel)** | Strong on small-to-medium datasets; effective when classes are separable in high-dimensional space (13 features, 178 samples). |

### Justification

- **This is a classification problem** — the target is a discrete class label (cultivar 1, 2, or 3), not a continuous value. Regression models (e.g., Linear Regression) would incorrectly treat classes as ordered numeric values and produce meaningless outputs like 1.7. All four models selected are classifiers designed to predict categories.
- The dataset is small (178 samples) → all four models train quickly, so computational cost is not a constraint.
- We include one linear model (Logistic Regression) and three non-linear models to assess whether the class boundaries are linear or complex.
- Random Forest and XGBoost both handle feature importance natively, which aids interpretation.
- SVM is included because it historically performs well on the UCI Wine dataset due to clear class separation in feature space.

---

## 2. Best Model Selection Criteria

The best model will be selected based on:

1. **F1 Macro** (primary metric) — accounts for slight class imbalance (59/71/48) by treating all classes equally.
2. **Accuracy** — overall correctness.
3. **Cross-validation stability** — low variance across folds indicates generalization.
4. **Simplicity** — if two models have similar performance, prefer the simpler one (Occam's razor).

> Final selection will be made after comparing all four models on the held-out test set and 5-fold cross-validation results.

---

## 3. Training Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Test proportion** | 20% (0.2) | 178 samples → ~36 test samples (~12 per class). Enough for meaningful evaluation while keeping 142 for training. |
| **Stratification** | Yes (`stratify=y`) | Preserves class distribution (59/71/48) in both train and test splits. |
| **Random seed** | 42 | Reproducibility across experiments. |
| **Cross-validation** | 5-fold stratified | Standard for small datasets; gives 5 estimates of generalization error. |

### Why 20% and not 30%?

With only 178 samples, a 30% split leaves just 124 training samples. At 20%, we keep 142 for training which gives models more data to learn from, while 36 test samples still provide a reasonable evaluation. The smallest class (cultivar_3 = 48 samples) would have ~10 test samples at 20% — enough to detect gross errors.

---

## 4. Preprocessing Steps

### Steps Applied

| Step | Method | Why |
|------|--------|-----|
| **Standardization** | `StandardScaler` (zero mean, unit variance) | Features have very different scales: proline ranges 278–1680, hue ranges 0.48–1.71. Models like Logistic Regression and SVM are distance/gradient-based and require scaled features. |
| **No encoding needed** | — | All 13 features are continuous numeric. Target is already integer-encoded (0/1/2). |
| **No imputation needed** | — | The dataset has zero missing values (verified during ingestion). |
| **Outlier handling** | Kept as-is (no removal) | With only 178 samples, removing outliers risks losing valuable minority-class information. Standardization reduces outlier impact on distance-based models. |

### Why StandardScaler over MinMaxScaler?

- StandardScaler is preferred when features may have outliers (e.g., proline has high variance). MinMaxScaler compresses everything to [0,1] and is sensitive to extreme values.
- For SVM with RBF kernel and Logistic Regression, StandardScaler produces better-conditioned optimization.
- Random Forest and XGBoost are scale-invariant, so scaling doesn't hurt them but doesn't help either.

### Transformations Considered but Not Applied

| Transformation | Decision | Reason |
|----------------|----------|--------|
| Log transform | Not applied | Most features are approximately normal; proline is right-skewed but tree-based models handle this natively. |
| PCA | Not applied | 13 features is manageable; no need for dimensionality reduction. Interpretability is more valuable here. |
| Feature engineering | Optional | Ratios like `flavanoids/total_phenols` or `color_intensity * hue` may help linear models but add complexity. |

---

## 5. Optimization & Hyperparameter Tuning

### Strategy

1. **Baseline first** — Train all 4 models with default hyperparameters. Record F1 macro and accuracy.
2. **Grid/Random Search** — Tune the top 2 performing models.
3. **Optuna** (optional) — Bayesian optimization for XGBoost if time permits.

### Hyperparameter Search Spaces

| Model | Parameters to Tune | Search Range |
|-------|-------------------|--------------|
| Logistic Regression | `C`, `max_iter` | C: [0.01, 0.1, 1, 10, 100], max_iter: [200, 500, 1000] |
| Random Forest | `n_estimators`, `max_depth`, `min_samples_split` | n_estimators: [50, 100, 200], max_depth: [3, 5, 10, None], min_samples_split: [2, 5, 10] |
| XGBoost | `n_estimators`, `max_depth`, `learning_rate` | n_estimators: [50, 100, 200], max_depth: [3, 5, 7], learning_rate: [0.01, 0.1, 0.3] |
| SVM | `C`, `gamma`, `kernel` | C: [0.1, 1, 10], gamma: ['scale', 'auto', 0.01, 0.1], kernel: ['rbf'] |

### Expected Improvement Commentary

- Logistic Regression is already near-optimal for linearly separable classes; tuning `C` mainly prevents overfitting.
- Random Forest benefits most from `max_depth` tuning to balance bias/variance on small data.
- XGBoost's `learning_rate` and `n_estimators` interact (lower rate needs more estimators); tuning both together is critical.
- SVM's `C` and `gamma` define the decision boundary smoothness; incorrect values lead to overfitting (high C, high gamma) or underfitting (low C).

---

## 6. Data Validation — Validator Design Decisions

### Approach: Two-Layer Validation

We use **Pydantic** (row-level) and **Pandera** (DataFrame-level) together:

| Layer | Tool | Purpose |
|-------|------|---------|
| Row-level | Pydantic `WineRecord` | Validates individual records (e.g., API requests, streaming data). Gives precise error messages per field. |
| Batch-level | Pandera `WineSchema` | Validates entire DataFrames at once (e.g., after loading a CSV). Catches schema-wide issues like wrong dtypes or null columns. Uses `lazy=True` to report ALL errors, not just the first. |

### Why Both?

- **Pydantic** is ideal for validating single records at inference time (API `/predict` endpoint).
- **Pandera** is ideal for pipeline stages where you validate a full dataset before training or evaluation.
- The range constraints are defined once in domain terms and mirrored in both tools.

### Validator Range Decisions

Ranges are set with **~20-30% margin** beyond the observed data to allow for legitimate variation in new wines while catching obvious corruption/errors:

| Feature | Observed Range | Validator Range | Rationale |
|---------|---------------|-----------------|-----------|
| alcohol | 11.03–14.83 | [8, 17] | Wine can range 8-17% ABV across styles; below 8 is likely juice, above 17 is fortified |
| malic_acid | 0.74–5.80 | [0, 7] | Must be non-negative; above 7 g/L would indicate measurement error |
| ash | 1.36–3.23 | [0.5, 5] | Mineral residue; very low/high suggests contamination or error |
| alcalinity_of_ash | 10.6–30.0 | [5, 40] | Generous margin; values outside indicate non-wine sample |
| magnesium | 70–162 | [50, 200] | mg/L range for wine; below 50 suggests dilution, above 200 suggests soil contamination |
| total_phenols | 0.98–3.88 | (0, 6] | Must be strictly positive; upper bound generous for aged wines |
| flavanoids | 0.34–5.08 | [0, 6] | Can approach 0 in some white wines; 6+ is unrealistic |
| nonflavanoid_phenols | 0.13–0.66 | [0, 1.5] | Small fraction of phenols; tight upper bound catches errors |
| proanthocyanins | 0.41–3.58 | [0, 5] | Tannin measure; 5+ would be extreme |
| color_intensity | 1.28–13.0 | (0, 20] | Optical density; must be positive, very high wines exist (port-like) |
| hue | 0.48–1.71 | (0, 2.5] | Ratio of optical densities; always positive, above 2.5 is physically unusual |
| od280_od315 | 1.27–4.00 | (0, 5] | UV absorption ratio; must be positive |
| proline | 278–1680 | [100, 2500] | Amino acid in mg/L; low in cold climates, high in warm/dry regions |
| class | {0, 1, 2} | {0, 1, 2} | Exact set — no margin needed for categorical target |

### Design Principles

1. **No nulls allowed** — The raw dataset has no missing values. Any null in processed data indicates a pipeline bug, not expected variation. Fail fast.
2. **Positivity for all features** — All 13 measurements represent physical/chemical quantities that cannot be negative. Negatives always indicate corruption.
3. **Domain-informed bounds** — Wines from the same region should pass validation even if slightly outside the 178-sample range.
4. **Strict class validation** — The target must be exactly 0, 1, or 2. Any other value (including -1, 3, or NaN) is immediately flagged as a data integrity issue.
5. **Lazy validation in Pandera** — `lazy=True` collects all schema violations before raising, so you see the full picture rather than fixing errors one at a time.

## 7. Dataset Summary

| Property | Value |
|----------|-------|
| Source | UCI Machine Learning Repository |
| Samples | 178 |
| Features | 13 (all continuous) |
| Classes | 3 (cultivar_1: 59, cultivar_2: 71, cultivar_3: 48) |
| Missing values | None |
| Class balance | Slightly imbalanced (33%/40%/27%) |
| Feature scales | Highly variable (proline ~278-1680 vs hue ~0.48-1.71) |

---