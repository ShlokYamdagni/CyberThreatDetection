"""
Model Training Module
Trains multiple classifiers, evaluates them, and selects the best one.
"""

import os
import json
import logging
import time
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and evaluates multiple ML models for threat detection."""

    def __init__(self, models_dir='models', test_size=0.2, random_state=42):
        self.models_dir = models_dir
        self.test_size = test_size
        self.random_state = random_state
        self.best_model = None
        self.best_model_name = None
        self.all_results = {}
        os.makedirs(models_dir, exist_ok=True)

    def get_models(self):
        """Return dictionary of models to train."""
        return {
            'Random Forest': RandomForestClassifier(
                n_estimators=100, max_depth=20, random_state=self.random_state, n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100, max_depth=5, learning_rate=0.1, random_state=self.random_state
            ),
            'Decision Tree': DecisionTreeClassifier(
                max_depth=15, random_state=self.random_state
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(
                n_neighbors=5, n_jobs=-1
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000, random_state=self.random_state, n_jobs=-1
            ),
        }

    def split_data(self, X, y):
        """Split data into training and testing sets."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        logger.info(f"Data split: Train={X_train.shape[0]}, Test={X_test.shape[0]}")
        return X_train, X_test, y_train, y_test

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate a trained model and return metrics."""
        y_pred = model.predict(X_test)

        metrics = {
            'accuracy': round(accuracy_score(y_test, y_pred), 4),
            'precision': round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 4),
            'recall': round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 4),
            'f1_score': round(f1_score(y_test, y_pred, average='weighted', zero_division=0), 4),
        }

        # ROC AUC (binary classification)
        try:
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test)[:, 1]
            else:
                y_proba = model.decision_function(X_test)
            metrics['roc_auc'] = round(roc_auc_score(y_test, y_proba), 4)
        except Exception:
            metrics['roc_auc'] = None

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()

        # Classification report
        metrics['classification_report'] = classification_report(
            y_test, y_pred, output_dict=True, zero_division=0
        )

        return metrics

    def train_all_models(self, X, y):
        """Train all models, evaluate, and select the best one."""
        X_train, X_test, y_train, y_test = self.split_data(X, y)

        models = self.get_models()
        results = {}
        best_f1 = -1

        for name, model in models.items():
            logger.info(f"Training {name}...")
            start_time = time.time()

            try:
                model.fit(X_train, y_train)
                train_time = round(time.time() - start_time, 2)

                metrics = self.evaluate_model(model, X_test, y_test)
                metrics['training_time'] = train_time

                results[name] = {
                    'metrics': metrics,
                    'model': model,
                }

                logger.info(
                    f"{name} - Accuracy: {metrics['accuracy']}, "
                    f"F1: {metrics['f1_score']}, Time: {train_time}s"
                )

                # Track the best model by F1 score
                if metrics['f1_score'] > best_f1:
                    best_f1 = metrics['f1_score']
                    self.best_model = model
                    self.best_model_name = name

            except Exception as e:
                logger.error(f"Error training {name}: {str(e)}")
                results[name] = {'error': str(e)}

        self.all_results = results
        logger.info(f"Best model: {self.best_model_name} (F1: {best_f1})")
        return results

    def save_best_model(self):
        """Save the best model to disk."""
        if self.best_model is None:
            raise ValueError("No trained model to save. Run train_all_models first.")

        model_path = os.path.join(self.models_dir, 'best_model.pkl')
        joblib.dump(self.best_model, model_path)
        logger.info(f"Best model ({self.best_model_name}) saved to {model_path}")

        # Save training results metadata
        results_meta = {}
        for name, data in self.all_results.items():
            if 'metrics' in data:
                metrics_copy = data['metrics'].copy()
                # Remove non-serializable items
                metrics_copy.pop('classification_report', None)
                results_meta[name] = metrics_copy

        meta_path = os.path.join(self.models_dir, 'training_results.json')
        with open(meta_path, 'w') as f:
            json.dump({
                'best_model': self.best_model_name,
                'results': results_meta,
            }, f, indent=2)
        logger.info(f"Training results metadata saved to {meta_path}")

        return model_path

    def load_model(self, model_path=None):
        """Load a saved model from disk."""
        if model_path is None:
            model_path = os.path.join(self.models_dir, 'best_model.pkl')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")
        return model

    def get_training_summary(self):
        """Return a summary of all training results."""
        summary = []
        for name, data in self.all_results.items():
            if 'metrics' in data:
                m = data['metrics']
                summary.append({
                    'model': name,
                    'accuracy': m['accuracy'],
                    'precision': m['precision'],
                    'recall': m['recall'],
                    'f1_score': m['f1_score'],
                    'roc_auc': m.get('roc_auc'),
                    'training_time': m.get('training_time'),
                    'is_best': name == self.best_model_name,
                })
            else:
                summary.append({
                    'model': name,
                    'error': data.get('error', 'Unknown error'),
                })
        return summary
