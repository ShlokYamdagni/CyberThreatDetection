"""
View Routes Module
Handles all page rendering routes.
"""

import os
import json
from flask import Blueprint, render_template, current_app

views_bp = Blueprint('views', __name__)


@views_bp.route('/')
def index():
    """Landing page."""
    return render_template('index.html')


@views_bp.route('/dashboard')
def dashboard():
    """Main dashboard page with analytics."""
    model_info = _get_model_info()
    training_results = _get_training_results()
    prediction_history = _get_prediction_history()
    return render_template(
        'dashboard.html',
        model_info=model_info,
        training_results=training_results,
        prediction_history=prediction_history
    )


@views_bp.route('/predict')
def predict_page():
    """Manual prediction form page."""
    model_info = _get_model_info()
    return render_template('predict.html', model_info=model_info)


@views_bp.route('/upload')
def upload_page():
    """CSV upload page."""
    model_info = _get_model_info()
    return render_template('upload.html', model_info=model_info)


@views_bp.route('/history')
def history_page():
    """Prediction history page."""
    prediction_history = _get_prediction_history()
    return render_template('history.html', prediction_history=prediction_history)


@views_bp.route('/analytics')
def analytics_page():
    """Analytics and model performance page."""
    training_results = _get_training_results()
    return render_template('analytics.html', training_results=training_results)


@views_bp.route('/about')
def about_page():
    """About page."""
    return render_template('about.html')


def _get_model_info():
    """Get model information from saved metadata."""
    meta_path = os.path.join(current_app.config['MODELS_FOLDER'], 'training_results.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            return json.load(f)
    return None


def _get_training_results():
    """Get training results for display."""
    meta_path = os.path.join(current_app.config['MODELS_FOLDER'], 'training_results.json')
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            data = json.load(f)
            return data.get('results', {})
    return {}


def _get_prediction_history():
    """Get prediction history from saved results."""
    history_path = os.path.join(current_app.config['RESULTS_FOLDER'], 'prediction_history.json')
    if os.path.exists(history_path):
        with open(history_path, 'r') as f:
            return json.load(f)
    return []
