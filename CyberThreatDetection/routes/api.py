"""
API Routes Module
REST API endpoints for predictions, file upload, and data retrieval.
"""

import os
import json
import uuid
import logging
from datetime import datetime

import pandas as pd
from flask import Blueprint, request, jsonify, current_app, send_file

api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)

# Lazy-loaded predictor instance
_predictor = None


def _get_predictor():
    """Lazy-load the ThreatPredictor singleton."""
    global _predictor
    if _predictor is None:
        from ml.predictor import ThreatPredictor
        _predictor = ThreatPredictor(models_dir=current_app.config['MODELS_FOLDER'])
    return _predictor


def _save_to_history(entry):
    """Append a prediction entry to the history file."""
    history_path = os.path.join(current_app.config['RESULTS_FOLDER'], 'prediction_history.json')
    history = []
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r') as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            history = []

    history.insert(0, entry)  # Most recent first
    # Keep last 500 entries
    history = history[:500]

    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)


def _allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'csv'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


# ─── Health Check ────────────────────────────────────────────────────

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint."""
    predictor = _get_predictor()
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.is_ready(),
        'timestamp': datetime.now().isoformat(),
    })


# ─── Model Info ──────────────────────────────────────────────────────

@api_bp.route('/model-info', methods=['GET'])
def model_info():
    """Return information about the loaded model."""
    try:
        predictor = _get_predictor()
        info = predictor.get_model_info()
        return jsonify(info)
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Single Prediction ──────────────────────────────────────────────

@api_bp.route('/predict', methods=['POST'])
def predict_single():
    """Predict a single network connection."""
    try:
        predictor = _get_predictor()
        if not predictor.is_ready():
            return jsonify({
                'error': 'Model not trained yet. Please run train_model.py first.'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided.'}), 400

        # Validate required fields
        required = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400

        # Convert numeric fields
        numeric_fields = [
            'duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
            'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised',
            'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
            'num_shells', 'num_access_files', 'is_host_login', 'is_guest_login',
            'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
            'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
            'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
            'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
            'dst_host_serror_rate', 'dst_host_srv_serror_rate',
            'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
        ]
        for field in numeric_fields:
            if field in data:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = 0.0

        # Set defaults for missing optional fields
        defaults = {k: 0.0 for k in numeric_fields}
        for k, v in defaults.items():
            if k not in data:
                data[k] = v

        result = predictor.predict_single(data)

        # Save to history
        history_entry = {
            'id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now().isoformat(),
            'type': 'single',
            'input_summary': {
                'protocol': data.get('protocol_type', 'N/A'),
                'service': data.get('service', 'N/A'),
                'src_bytes': data.get('src_bytes', 0),
                'dst_bytes': data.get('dst_bytes', 0),
            },
            'prediction': result['label'],
            'confidence': result.get('confidence'),
        }
        _save_to_history(history_entry)

        return jsonify(result)

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Batch Prediction (CSV Upload) ──────────────────────────────────

@api_bp.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Predict from an uploaded CSV file."""
    try:
        predictor = _get_predictor()
        if not predictor.is_ready():
            return jsonify({
                'error': 'Model not trained yet. Please run train_model.py first.'
            }), 503

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded.'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected.'}), 400

        if not _allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed.'}), 400

        # Save uploaded file
        upload_dir = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex[:12]}_{file.filename}"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)

        # Read and predict
        df = pd.read_csv(filepath)
        if df.empty:
            return jsonify({'error': 'Uploaded CSV is empty.'}), 400

        results, summary = predictor.predict_batch(df)

        # Save results to a downloadable CSV
        results_dir = current_app.config['RESULTS_FOLDER']
        os.makedirs(results_dir, exist_ok=True)
        result_filename = f"results_{uuid.uuid4().hex[:8]}.csv"
        result_filepath = os.path.join(results_dir, result_filename)

        result_df = df.copy()
        result_df['prediction'] = [r['prediction'] for r in results]
        result_df['prediction_label'] = [r['label'] for r in results]
        result_df['confidence'] = [r['confidence'] for r in results]
        result_df.to_csv(result_filepath, index=False)

        # Save to history
        history_entry = {
            'id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now().isoformat(),
            'type': 'batch',
            'filename': file.filename,
            'total_records': summary['total'],
            'attacks_detected': summary['attacks'],
            'normal_detected': summary['normal'],
            'attack_percentage': summary['attack_percentage'],
            'result_file': result_filename,
        }
        _save_to_history(history_entry)

        return jsonify({
            'results': results[:100],  # Return first 100 for display
            'summary': summary,
            'result_file': result_filename,
            'total_results': len(results),
        })

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Download Results ────────────────────────────────────────────────

@api_bp.route('/download/<filename>', methods=['GET'])
def download_results(filename):
    """Download prediction results CSV."""
    try:
        results_dir = current_app.config['RESULTS_FOLDER']
        filepath = os.path.join(results_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found.'}), 404

        return send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Prediction History ─────────────────────────────────────────────

@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get prediction history."""
    try:
        history_path = os.path.join(
            current_app.config['RESULTS_FOLDER'], 'prediction_history.json'
        )
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                history = json.load(f)
            return jsonify(history)
        return jsonify([])
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/clear', methods=['POST'])
def clear_history():
    """Clear prediction history."""
    try:
        history_path = os.path.join(
            current_app.config['RESULTS_FOLDER'], 'prediction_history.json'
        )
        if os.path.exists(history_path):
            with open(history_path, 'w') as f:
                json.dump([], f)
        return jsonify({'message': 'History cleared successfully.'})
    except Exception as e:
        logger.error(f"History clear error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Training Results ────────────────────────────────────────────────

@api_bp.route('/training-results', methods=['GET'])
def get_training_results():
    """Get training results and model comparison data."""
    try:
        meta_path = os.path.join(
            current_app.config['MODELS_FOLDER'], 'training_results.json'
        )
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({'error': 'No training results found. Train the model first.'}), 404
    except Exception as e:
        logger.error(f"Training results error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ─── Dashboard Stats ────────────────────────────────────────────────

@api_bp.route('/dashboard-stats', methods=['GET'])
def dashboard_stats():
    """Get aggregated stats for the dashboard."""
    try:
        stats = {
            'model_status': 'not_loaded',
            'total_predictions': 0,
            'threats_detected': 0,
            'normal_detected': 0,
            'threat_percentage': 0,
        }

        # Model status
        predictor = _get_predictor()
        if predictor.is_ready():
            stats['model_status'] = 'active'
            info = predictor.get_model_info()
            stats['model_type'] = info.get('model_type', 'Unknown')

            if 'training_results' in info:
                best = info['training_results'].get('best_model', 'Unknown')
                best_results = info['training_results'].get('results', {}).get(best, {})
                stats['accuracy'] = best_results.get('accuracy', 0)
                stats['best_model'] = best

        # History stats
        history_path = os.path.join(
            current_app.config['RESULTS_FOLDER'], 'prediction_history.json'
        )
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                history = json.load(f)
                stats['total_predictions'] = len(history)

                for entry in history:
                    if entry.get('type') == 'single':
                        if entry.get('prediction') == 'Attack':
                            stats['threats_detected'] += 1
                        else:
                            stats['normal_detected'] += 1
                    elif entry.get('type') == 'batch':
                        stats['threats_detected'] += entry.get('attacks_detected', 0)
                        stats['normal_detected'] += entry.get('normal_detected', 0)

                total = stats['threats_detected'] + stats['normal_detected']
                if total > 0:
                    stats['threat_percentage'] = round(
                        (stats['threats_detected'] / total) * 100, 1
                    )

        return jsonify(stats)
    except Exception as e:
        logger.error(f"Dashboard stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500
