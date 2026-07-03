"""
Model Training Script
Run this script to generate the dataset, preprocess it, train models,
and save the best model.

Usage:
    python train_model.py
"""

import os
import sys
import json
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
DATASET_FILE = os.path.join(DATASET_DIR, 'network_intrusion_data.csv')


def main():
    """Main training pipeline."""
    print("=" * 70)
    print("  AI-Based Cyber Threat Detection Framework")
    print("  Model Training Pipeline")
    print("=" * 70)

    # Step 1: Generate dataset if not exists
    if not os.path.exists(DATASET_FILE):
        print("\n[1/4] Generating sample dataset...")
        from dataset.generate_sample_data import generate_dataset
        generate_dataset(DATASET_FILE)
    else:
        print(f"\n[1/4] Dataset found: {DATASET_FILE}")

    # Step 2: Load and preprocess data
    print("\n[2/4] Preprocessing data...")
    from ml.preprocessing import DataPreprocessor
    preprocessor = DataPreprocessor(models_dir=MODELS_DIR)
    df = preprocessor.load_data(DATASET_FILE)
    X, y, feature_names = preprocessor.prepare_features(df, fit=True)

    print(f"  Features: {X.shape[1]}")
    print(f"  Samples: {X.shape[0]}")
    print(f"  Feature names: {feature_names[:10]}... ({len(feature_names)} total)")

    # Step 3: Train models
    print("\n[3/4] Training models...")
    from ml.training import ModelTrainer
    trainer = ModelTrainer(models_dir=MODELS_DIR)
    results = trainer.train_all_models(X, y)

    # Print results
    print("\n" + "=" * 70)
    print("  Training Results")
    print("=" * 70)
    print(f"{'Model':<25} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1 Score':<12} {'ROC AUC':<12} {'Time (s)':<10}")
    print("-" * 95)

    for name, data in results.items():
        if 'metrics' in data:
            m = data['metrics']
            roc = f"{m['roc_auc']:.4f}" if m.get('roc_auc') is not None else 'N/A'
            marker = " [BEST]" if name == trainer.best_model_name else ""
            print(
                f"{name:<25} {m['accuracy']:<12.4f} {m['precision']:<12.4f} "
                f"{m['recall']:<12.4f} {m['f1_score']:<12.4f} {roc:<12} {m['training_time']:<10.2f}{marker}"
            )
        else:
            print(f"{name:<25} ERROR: {data.get('error', 'Unknown')}")

    print(f"\n  [BEST] Best Model: {trainer.best_model_name}")

    # Print confusion matrix for best model
    best_metrics = results[trainer.best_model_name]['metrics']
    cm = best_metrics['confusion_matrix']
    print(f"\n  Confusion Matrix ({trainer.best_model_name}):")
    print(f"    {'':>15} Predicted Normal  Predicted Attack")
    print(f"    Actual Normal   {cm[0][0]:>10}         {cm[0][1]:>10}")
    print(f"    Actual Attack   {cm[1][0]:>10}         {cm[1][1]:>10}")

    # Step 4: Save model and preprocessor
    print("\n[4/4] Saving model and preprocessor...")
    trainer.save_best_model()
    preprocessor.save_preprocessor()

    print("\n" + "=" * 70)
    print("  Training Complete!")
    print(f"  Model saved to: {os.path.join(MODELS_DIR, 'best_model.pkl')}")
    print(f"  Preprocessor saved to: {os.path.join(MODELS_DIR, 'preprocessor.pkl')}")
    print(f"  Results saved to: {os.path.join(MODELS_DIR, 'training_results.json')}")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
