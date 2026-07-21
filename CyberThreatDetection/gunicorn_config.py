"""
Gunicorn configuration for production deployment on Render.
"""

import os

# Bind to the port Render provides via $PORT, fallback to 5000
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Workers — Render free tier has limited RAM, keep it lean
workers = 2
threads = 2

# Timeout — model loading can take a moment
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
