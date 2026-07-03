"""
Application Configuration Module
AI-Based Cyber Threat Detection Framework
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cyber-threat-detection-secret-key-2024')
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
    MODELS_FOLDER = os.path.join(BASE_DIR, 'models')
    DATASET_FOLDER = os.path.join(BASE_DIR, 'dataset')
    LOGS_FOLDER = os.path.join(BASE_DIR, 'logs')
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'csv'}
    
    # ML settings
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
