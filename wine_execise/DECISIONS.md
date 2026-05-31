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

## 6. Data Architecture Decision: Relational Split

For the relational data exercise, features were split into two tables:

| Table | Features | Rationale |
|-------|----------|-----------|
| `chemical.csv` | alcohol, malic_acid, ash, alcalinity_of_ash, magnesium, color_intensity, proline | General composition & physical properties — measured via titration, spectrophotometry, chromatography |
| `phenols.csv` | total_phenols, flavanoids, nonflavanoid_phenols, proanthocyanins, hue, od280_od315 | Phenolic profile panel — all polyphenol subclasses + UV/optical ratios that reflect phenolic content |

This mirrors how a real wine lab organizes data: one table for general chemistry, another for the phenolic analysis panel.

---

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
