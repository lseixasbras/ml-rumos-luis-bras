"""
Model Prediction Module
Contains functions for model inference and prediction.
Multiclass classification (3 cultivars).
"""


def predict(model, X_test):
    """
    Generate predictions using trained model.

    Args:
        model: Trained model object
        X_test: Test features

    Returns:
        Array of predictions (0: cultivar_1, 1: cultivar_2, 2: cultivar_3)
    """
    # TODO: Implement prediction logic
    pass


def predict_proba(model, X_test):
    """
    Generate probability predictions using trained model.
    Multiclass classification (3 cultivars).

    Args:
        model: Trained model object
        X_test: Test features

    Returns:
        Array of class probabilities (n_samples x 3 classes)
    """
    # TODO: Implement probability prediction logic
    pass


def predict_cultivar(model_name, features_dict):
    """
    Predict wine cultivar (0=cultivar_1, 1=cultivar_2, 2=cultivar_3).

    Args:
        model_name: Name of model to use
        features_dict: Dict with 13 feature values

    Returns:
        Predicted cultivar (0/1/2), or None if model fails
    """
    # TODO: Implement cultivar prediction
    # Hint: Load model, call predict() with features_dict
    pass


def predict_cultivar_proba(model_name, features_dict):
    """
    Predict probability distribution across cultivars.

    Args:
        model_name: Name of model to use (should support predict_proba)
        features_dict: Dict with 13 feature values

    Returns:
        Dict with probabilities for each cultivar, or None if fails
        e.g., {"cultivar_1": 0.1, "cultivar_2": 0.3, "cultivar_3": 0.6}
    """
    # TODO: Implement cultivar probability prediction
    # Hint: Load model, call predict_proba(), convert to dict
    # probs = model.predict_proba(X)
    # return {"cultivar_1": float(probs[0][0]), ...}
    pass
