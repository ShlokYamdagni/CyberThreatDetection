"""
Prediction Module
Loads the trained model and preprocessor for making predictions.
"""

import os
import logging
import joblib
import numpy as np
from ml.preprocessing import DataPreprocessor

logger = logging.getLogger(__name__)

LABEL_MAP = {0: 'Normal', 1: 'Attack'}
THREAT_LEVEL_MAP = {
    0: {'level': 'Safe', 'color': '#00c853', 'icon': 'shield-check'},
    1: {'level': 'Threat Detected', 'color': '#ff1744', 'icon': 'shield-exclamation'},
}


class ThreatPredictor:
    """Makes predictions using the trained model and preprocessor."""

    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.model = None
        self.preprocessor = None
        self._load()

    def _load(self):
        """Load model and preprocessor from disk."""
        model_path = os.path.join(self.models_dir, 'best_model.pkl')
        if not os.path.exists(model_path):
            logger.warning("Trained model not found. Please train the model first.")
            return

        try:
            self.model = joblib.load(model_path)
            self.preprocessor = DataPreprocessor(self.models_dir)
            self.preprocessor.load_preprocessor()
            logger.info("Model and preprocessor loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading model/preprocessor: {str(e)}")
            self.model = None
            self.preprocessor = None

    def is_ready(self):
        """Check if the predictor is ready to make predictions."""
        return self.model is not None and self.preprocessor is not None

    def predict_single(self, input_dict):
        """Predict a single input (dictionary of features)."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded. Train the model first.")

        try:
            X = self.preprocessor.prepare_single_input(input_dict)
            prediction = int(self.model.predict(X)[0])
            confidence = None

            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(X)[0]
                confidence = round(float(max(proba)) * 100, 2)

            result = {
                'prediction': prediction,
                'label': LABEL_MAP.get(prediction, 'Unknown'),
                'confidence': confidence,
                'threat_info': THREAT_LEVEL_MAP.get(prediction, {}),
            }
            return result

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

    def predict_batch(self, df):
        """Predict for a DataFrame (batch prediction)."""
        if not self.is_ready():
            raise RuntimeError("Model not loaded. Train the model first.")

        try:
            X, _, _ = self.preprocessor.prepare_features(df, fit=False)
            predictions = self.model.predict(X)

            confidences = None
            if hasattr(self.model, 'predict_proba'):
                probas = self.model.predict_proba(X)
                confidences = [round(float(max(p)) * 100, 2) for p in probas]

            results = []
            for i, pred in enumerate(predictions):
                pred_int = int(pred)
                result = {
                    'index': i,
                    'prediction': pred_int,
                    'label': LABEL_MAP.get(pred_int, 'Unknown'),
                    'confidence': confidences[i] if confidences else None,
                }
                results.append(result)

            # Summary statistics
            total = len(predictions)
            attacks = int(np.sum(predictions == 1))
            normal = total - attacks
            attack_pct = round((attacks / total) * 100, 2) if total > 0 else 0

            summary = {
                'total': total,
                'attacks': attacks,
                'normal': normal,
                'attack_percentage': attack_pct,
                'normal_percentage': round(100 - attack_pct, 2),
            }

            return results, summary

        except Exception as e:
            logger.error(f"Batch prediction error: {str(e)}")
            raise

    def get_model_info(self):
        """Return information about the loaded model."""
        if not self.is_ready():
            return {'status': 'not_loaded', 'message': 'Model not trained yet.'}

        info = {
            'status': 'loaded',
            'model_type': type(self.model).__name__,
            'n_features': len(self.preprocessor.feature_names),
            'feature_names': self.preprocessor.feature_names,
        }

        # Load training results if available
        import json
        meta_path = os.path.join(self.models_dir, 'training_results.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                info['training_results'] = json.load(f)

        return info
