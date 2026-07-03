"""
Data Preprocessing Module
Handles data cleaning, feature engineering, encoding, and scaling.
"""

import os
import logging
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler

logger = logging.getLogger(__name__)

# Columns in the NSL-KDD-like dataset
CATEGORICAL_COLS = ['protocol_type', 'service', 'flag']
BINARY_LABEL_COL = 'label'
ATTACK_TYPE_COL = 'attack_type'

# Columns to drop during training (target columns)
TARGET_COLS = [BINARY_LABEL_COL, ATTACK_TYPE_COL]

# Required feature columns for prediction (all except targets)
FEATURE_COLS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]


class DataPreprocessor:
    """Handles all data preprocessing for the cyber threat detection pipeline."""

    def __init__(self, models_dir='models'):
        self.models_dir = models_dir
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        os.makedirs(models_dir, exist_ok=True)

    def load_data(self, filepath):
        """Load CSV dataset."""
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    def clean_data(self, df):
        """Clean the dataset: handle missing values, duplicates, and infinities."""
        logger.info("Cleaning data...")
        initial_shape = df.shape

        # Replace infinities with NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Drop rows with NaN values
        df.dropna(inplace=True)

        # Drop duplicates
        df.drop_duplicates(inplace=True)

        # Reset index
        df.reset_index(drop=True, inplace=True)

        logger.info(f"Data cleaned: {initial_shape} -> {df.shape}")
        return df

    def encode_categorical(self, df, fit=True):
        """Label-encode categorical columns."""
        logger.info("Encoding categorical features...")
        df = df.copy()

        for col in CATEGORICAL_COLS:
            if col not in df.columns:
                logger.warning(f"Column '{col}' not found in data, skipping encoding.")
                continue

            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
            else:
                le = self.label_encoders.get(col)
                if le is None:
                    raise ValueError(f"No fitted encoder found for column '{col}'.")
                # Handle unseen labels by assigning a default value
                known_classes = set(le.classes_)
                df[col] = df[col].astype(str).apply(
                    lambda x: le.transform([x])[0] if x in known_classes else -1
                )

        return df

    def feature_engineering(self, df):
        """Create additional features from existing ones."""
        logger.info("Performing feature engineering...")
        df = df.copy()

        # Byte ratio feature
        df['byte_ratio'] = np.where(
            df['dst_bytes'] > 0,
            df['src_bytes'] / (df['dst_bytes'] + 1),
            df['src_bytes']
        )

        # Total bytes
        df['total_bytes'] = df['src_bytes'] + df['dst_bytes']

        # Error rate features
        df['total_error_rate'] = df['serror_rate'] + df['rerror_rate']

        # Service rate difference
        df['srv_rate_diff'] = df['same_srv_rate'] - df['diff_srv_rate']

        # Host service diversity
        df['host_srv_diversity'] = df['dst_host_diff_srv_rate'] + df['dst_host_srv_diff_host_rate']

        return df

    def prepare_features(self, df, fit=True):
        """Prepare feature matrix (X) and labels (y)."""
        df = self.clean_data(df)
        df = self.feature_engineering(df)
        df = self.encode_categorical(df, fit=fit)

        # Separate features and target
        y = None
        if BINARY_LABEL_COL in df.columns:
            y = df[BINARY_LABEL_COL].values

        # Drop target columns
        drop_cols = [c for c in TARGET_COLS if c in df.columns]
        X = df.drop(columns=drop_cols)

        # Keep only numeric columns
        X = X.select_dtypes(include=[np.number])

        if fit:
            self.feature_names = X.columns.tolist()
            X_scaled = self.scaler.fit_transform(X)
        else:
            # Align columns with training features
            for col in self.feature_names:
                if col not in X.columns:
                    X[col] = 0
            X = X[self.feature_names]
            X_scaled = self.scaler.transform(X)

        return X_scaled, y, self.feature_names

    def prepare_single_input(self, input_dict):
        """Prepare a single input dictionary for prediction."""
        df = pd.DataFrame([input_dict])
        X, _, _ = self.prepare_features(df, fit=False)
        return X

    def save_preprocessor(self):
        """Save encoders and scaler to disk."""
        path = os.path.join(self.models_dir, 'preprocessor.pkl')
        joblib.dump({
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
        }, path)
        logger.info(f"Preprocessor saved to {path}")

    def load_preprocessor(self):
        """Load encoders and scaler from disk."""
        path = os.path.join(self.models_dir, 'preprocessor.pkl')
        if not os.path.exists(path):
            raise FileNotFoundError(f"Preprocessor file not found: {path}")

        data = joblib.load(path)
        self.label_encoders = data['label_encoders']
        self.scaler = data['scaler']
        self.feature_names = data['feature_names']
        logger.info("Preprocessor loaded successfully.")
