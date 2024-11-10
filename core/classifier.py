import numpy as np
from catboost import CatBoostClassifier
from core.embedder import embed_text


class Classifier():
    def __init__(self, model_path: str) -> None:
        self.model = CatBoostClassifier()
        self.model.load_model(model_path)


    def predict(self, theme, description):
        X_theme = embed_text(theme)
        X_desc = embed_text(description)

        X = np.hstack([X_theme, X_desc])

        probabilities = self.model.predict_proba(X).tolist()
        max_probability = max(probabilities)
        return probabilities.index(max_probability), max_probability
