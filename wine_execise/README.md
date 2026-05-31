# Wine Classification Project

**Dataset:** UCI Wine Recognition — 178 samples, 13 features, 3-class target (cultivar_1, cultivar_2, cultivar_3)

**Download link:** https://archive.ics.uci.edu/dataset/109/wine

## Project Goals

- **Model Selection:** Choose models to compare, justify your choice
- **Best Model:** Choose the best model, justify your choice
- **Training Parameters:** Define test proportion and training setup
- **Preprocessing:** Choose preprocessing steps and transformations, explain why
- **Optimization:** Tune hyperparameters, comment on improvements

## Data Generation

### Clean Data
Generate processed clean data:
```bash
cd data_ingestion && python ingestion.py
```
Output: `data/processed/clean_data.csv`

## Scripts

The following scripts are available in the `scripts/` directory for MLOps workflows.
This is a multiclass classification problem (3 cultivars: cultivar_1, cultivar_2, cultivar_3).

### Script Specifications

| Script | Required Arguments | Optional Arguments | Purpose |
|--------|-------------------|-------------------|---------|
| `run_validation.py` | `--data-path` | - | Validate data quality and schema |
| `run_training.py` | `--data-path`, `--model-type` | `--params` (JSON) | Train model with specified algorithm |
| `run_gate_evaluation.py` | `--model-uri`, `--test-data` | `--gates` (JSON) | Evaluate model against configurable gates |
| `run_registration.py` | `--model-uri`, `--model-name` | - | Register model in MLflow Model Registry |

### Supported Model Types
- `logistic` — Logistic Regression (multiclass)
- `xgboost` — XGBoost Classifier (multiclass, uses `eval_metric='mlogloss'`)
- `random_forest` — Random Forest Classifier (multiclass)
- `svm` — Support Vector Machine (multiclass, uses `decision_function_shape='ovr'`)

### Gate Configuration
Gates are CLI-configurable via the `--gates` argument as a JSON string.
Default gates for multiclass (uses `f1_macro`):
```json
{"accuracy": 0.90, "f1_macro": 0.85}
```

### Usage Examples

```bash
# Validate clean data
python scripts/run_validation.py --data-path data/processed/clean_data.csv

# Train XGBoost model for multiclass (note: eval_metric='mlogloss')
python scripts/run_training.py \
  --data-path data/processed/clean_data.csv \
  --model-type xgboost \
  --params '{"n_estimators": 100, "max_depth": 5}'

# Evaluate model gates (CLI-configurable, multiclass uses f1_macro)
python scripts/run_gate_evaluation.py \
  --model-uri models:/xgboost/1 \
  --test-data data/processed/clean_data.csv \
  --gates '{"accuracy": 0.90, "f1_macro": 0.85}'

# Register model in MLflow
python scripts/run_registration.py \
  --model-uri models:/xgboost/1 \
  --model-name wine_xgb
```

## Session 06: Build an App

Students build a FastAPI inference app using the templates provided.

### App Template
The `api/` directory contains the app template with TODOs for students to implement:
- `api/app.py` — FastAPI app with `/predict`, `/health`, and `/train` endpoints (TODOs)
- `models/predict.py` — Prediction functions: `predict_cultivar()`, `predict_cultivar_proba()` (TODOs)

### Example Input Files
Test the app with example JSON files in `api/example_inputs/`:
- `cultivar_1_sample.json` — Sample with class=0 (cultivar_1)
- `cultivar_2_sample.json` — Sample with class=1 (cultivar_2)
- `cultivar_3_sample.json` — Sample with class=2 (cultivar_3)

### Usage
```bash
# Start the API server
cd wine_execise
uvicorn api.app:app --reload --port 8004

# Health check
curl http://localhost:8004/health

# Predict with example input (cultivar_1 sample)
curl -X POST "http://localhost:8004/predict" \
  -H "Content-Type: application/json" \
  -d @api/example_inputs/cultivar_1_sample.json
```

### Reference: Training Functions
Students should have already implemented these in `models/train.py`:
- `train_logistic_regression()`, `train_xgboost()`, `train_random_forest()`, `train_svm()`
- These can be used to (re)train models that the app will load for inference
