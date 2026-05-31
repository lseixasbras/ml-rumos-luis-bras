from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

sys.path.append(str(Path(__file__).parent.parent))

from models.predict import predict_cultivar, predict_cultivar_proba
from models.train import (
    train_logistic_regression, train_xgboost,
    train_random_forest, train_svm, save_model
)
from config import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Wine Classification ML API")


class PredictRequest(BaseModel):
    # 13 features from the wine dataset
    alcohol: float = 0.0
    malic_acid: float = 0.0
    ash: float = 0.0
    alcalinity_of_ash: float = 0.0
    magnesium: float = 0.0
    total_phenols: float = 0.0
    flavanoids: float = 0.0
    nonflavanoid_phenols: float = 0.0
    proanthocyanins: float = 0.0
    color_intensity: float = 0.0
    hue: float = 0.0
    od280_od315: float = 0.0
    proline: float = 0.0
    model: Optional[str] = "logistic"


class TrainRequest(BaseModel):
    model_type: str = "logistic"
    params: Optional[Dict] = {}


class TrainResponse(BaseModel):
    model_type: str
    status: str
    metrics: Optional[Dict] = None
    message: str


class PredictResponse(BaseModel):
    cultivar_prediction: int  # 0=cultivar_1, 1=cultivar_2, 2=cultivar_3
    probabilities: Dict[str, float]  # {"cultivar_1": 0.1, "cultivar_2": 0.3, "cultivar_3": 0.6}
    model_used: str


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # TODO: Extract features from req into a dict
    # features = {
    #     'alcohol': req.alcohol,
    #     'malic_acid': req.malic_acid,
    #     'ash': req.ash,
    #     'alcalinity_of_ash': req.alcalinity_of_ash,
    #     'magnesium': req.magnesium,
    #     'total_phenols': req.total_phenols,
    #     'flavanoids': req.flavanoids,
    #     'nonflavanoid_phenols': req.nonflavanoid_phenols,
    #     'proanthocyanins': req.proanthocyanins,
    #     'color_intensity': req.color_intensity,
    #     'hue': req.hue,
    #     'od280_od315': req.od280_od315,
    #     'proline': req.proline
    # }
    
    # TODO: Call predict_cultivar() with req.model
    # cultivar = predict_cultivar(req.model, features)
    
    # TODO: Call predict_cultivar_proba() with req.model
    # proba = predict_cultivar_proba(req.model, features)
    # probs_dict = {'cultivar_1': float(proba[0][0]), ...}
    
    # TODO: Handle None cases
    # if cultivar is None: cultivar = 0
    # if probs_dict is None: probs_dict = {"cultivar_1": 0.33, ...}
    
    logger.info(f"Prediction: cultivar={cultivar}, model={req.model}")
    return PredictResponse(
        cultivar_prediction=cultivar,
        probabilities=probs_dict,
        model_used=req.model
    )


@app.get("/health")
def health():
    # TODO: Return {"status": "healthy"}
    pass


@app.post("/train", response_model=TrainResponse)
def train(req: TrainRequest):
    # Hardcoded data path (not exposed to user)
    data_path = Path(__file__).parent.parent / "data" / "processed" / "clean_data.csv"

    # TODO: Load data from data_path
    # df = pd.read_csv(data_path)
    # X = df.drop('class', axis=1)
    # y = df['class']
    
    # TODO: Split data (hardcoded test_size=0.2)
    # X_train, X_test, y_train, y_test = train_test_split(...)
    
    # TODO: Train model based on req.model_type
    # if req.model_type == 'logistic':
    #     model = train_logistic_regression(X_train, y_train, req.params)
    # elif req.model_type == 'xgboost':
    #     model = train_xgboost(X_train, y_train, req.params)
    # ...
    
    # TODO: Evaluate on test set
    # y_pred = model.predict(X_test)
    # metrics = {'accuracy': ..., 'f1_macro': ...}
    
    # TODO: Save model (backend handles path)
    # save_model(model, req.model_type)
    
    logger.info(f"Model {req.model_type} trained")
    return TrainResponse(
        model_type=req.model_type,
        status="success",
        message=f"Model saved to models/{req.model_type}.joblib"
    )
