"""
AI-Based Cyber Threat Detection Framework
Main Flask Application Entry Point
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config, config_map


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_map.get(config_name, Config))

    # Create required directories
    for folder in [
        app.config.get('UPLOAD_FOLDER', 'uploads'),
        app.config.get('RESULTS_FOLDER', 'results'),
        app.config.get('MODELS_FOLDER', 'models'),
        app.config.get('DATASET_FOLDER', 'dataset'),
        app.config.get('LOGS_FOLDER', 'logs'),
    ]:
        os.makedirs(folder, exist_ok=True)

    # Configure logging
    _setup_logging(app)

    # Register blueprints
    from routes.views import views_bp
    from routes.api import api_bp
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    app.logger.info('Cyber Threat Detection Framework started successfully.')
    return app


def _setup_logging(app):
    """Configure application logging."""
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


if __name__ == '__main__':
    application = create_app('development')
    application.run(host='0.0.0.0', port=5000, debug=True)
