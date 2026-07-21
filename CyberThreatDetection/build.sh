#!/usr/bin/env bash
# build.sh — Render Build Script
# Installs dependencies and trains the model if needed

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Train the model if it doesn't already exist
if [ ! -f "models/best_model.pkl" ]; then
    echo ">>> Training model..."
    python train_model.py
    echo ">>> Model training complete."
else
    echo ">>> Model already exists, skipping training."
fi
