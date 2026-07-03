# 🛡️ AI-Based Cyber Threat Detection Framework

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?style=for-the-badge&logo=flask&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.4-red?style=for-the-badge&logo=chart.js&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An intelligent network intrusion detection system powered by machine learning, featuring a modern dark-themed cybersecurity dashboard.**

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [Screenshots](#-screenshots) • [API Docs](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [ML Pipeline](#-ml-pipeline)
- [Dataset](#-dataset)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

The **AI-Based Cyber Threat Detection Framework** is a comprehensive web application that uses machine learning to classify network traffic as normal or malicious. It trains multiple classification models, automatically selects the best performer, and provides an intuitive dashboard for threat analysis.

### Key Capabilities
- 🧠 **Multi-Model Training** — Trains 5 ML models and auto-selects the best
- 🎯 **Real-time Prediction** — Instant threat classification with confidence scores
- 📁 **Batch Processing** — Upload CSV files for bulk threat analysis
- 📊 **Visual Analytics** — Interactive charts, confusion matrices, and radar plots
- 📜 **Prediction History** — Full audit trail with search and filters
- ⬇️ **Export Results** — Download prediction results as CSV

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Dashboard** | Real-time stats, model performance charts, threat distribution |
| **Manual Prediction** | Form with 41+ network features and quick-fill presets |
| **CSV Upload** | Drag-and-drop file upload with progress tracking |
| **Model Analytics** | Compare all 5 models with detailed metrics tables |
| **Prediction History** | Searchable, filterable history with download links |
| **REST API** | Full JSON API for programmatic access |
| **Dark Theme** | Professional cybersecurity-themed dark UI |
| **Responsive** | Works on desktop, tablet, and mobile devices |

---

## 🛠 Tech Stack

### Backend
- **Python 3.9+** — Core language
- **Flask 3.0** — Web framework
- **Scikit-learn 1.3** — Machine learning
- **Pandas 2.1** — Data processing
- **NumPy 1.26** — Numerical computing
- **Joblib** — Model serialization

### Frontend
- **HTML5 / CSS3 / JavaScript** — Core web technologies
- **Bootstrap 5.3** — Responsive UI framework
- **Chart.js 4.4** — Interactive visualizations
- **Bootstrap Icons** — Icon library
- **Google Fonts (Inter)** — Typography

### ML Models
| Model | Description |
|-------|-------------|
| Random Forest | Ensemble of decision trees |
| Gradient Boosting | Sequential boosted trees |
| Decision Tree | Single tree classifier |
| K-Nearest Neighbors | Instance-based learner |
| Logistic Regression | Linear classifier |

---

## 📁 Project Structure

```
CyberThreatDetection/
├── app.py                          # Flask application entry point
├── config.py                       # Application configuration
├── train_model.py                  # Model training script
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
│
├── dataset/
│   └── generate_sample_data.py     # Synthetic dataset generator
│
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py            # Data cleaning & feature engineering
│   ├── training.py                 # Multi-model training pipeline
│   └── predictor.py                # Prediction service
│
├── routes/
│   ├── __init__.py
│   ├── views.py                    # Page rendering routes
│   └── api.py                      # REST API endpoints
│
├── templates/
│   ├── base.html                   # Base template with sidebar
│   ├── index.html                  # Landing page
│   ├── dashboard.html              # Main dashboard
│   ├── predict.html                # Manual prediction form
│   ├── upload.html                 # CSV upload page
│   ├── history.html                # Prediction history
│   ├── analytics.html              # Model analytics
│   └── about.html                  # About page
│
├── static/
│   ├── css/
│   │   ├── style.css               # Main styles (dark theme)
│   │   ├── landing.css             # Landing page styles
│   │   └── dashboard.css           # Dashboard styles
│   └── js/
│       ├── main.js                 # Core JavaScript
│       ├── charts.js               # Chart.js configurations
│       └── upload.js               # File upload handler
│
├── models/                         # Saved models (generated)
├── uploads/                        # Uploaded files (generated)
├── results/                        # Prediction results (generated)
└── logs/                           # Application logs (generated)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/CyberThreatDetection.git
cd CyberThreatDetection

# 2. Create virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the ML model
python train_model.py

# 5. Run the application
python app.py
```

### Access the Application
Open your browser and navigate to: **http://localhost:5000**

---

## 📖 Usage Guide

### 1. Train the Model
Run `python train_model.py` to:
- Generate the synthetic dataset (25,000 samples)
- Preprocess the data (cleaning, encoding, scaling)
- Train 5 ML models
- Auto-select the best model by F1 Score
- Save the model and preprocessor

### 2. Dashboard
View real-time statistics including:
- Model status and accuracy
- Threat distribution charts
- Model comparison bar charts
- Confusion matrix
- Recent prediction history

### 3. Manual Prediction
- Fill in network connection parameters (41 features)
- Use quick-fill presets for Normal, DoS, Probe, or R2L attacks
- Get instant prediction with confidence score

### 4. Batch Upload
- Upload a CSV file with network traffic data
- Get bulk predictions with summary statistics
- Download results as a CSV file

### 5. History
- View all past predictions with timestamps
- Filter by type (single/batch), result (attack/normal)
- Search across all entries

---

## 🔌 API Documentation

### Base URL: `http://localhost:5000/api`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | System health check |
| `/api/model-info` | GET | Get model information |
| `/api/predict` | POST | Single prediction (JSON body) |
| `/api/predict-batch` | POST | Batch prediction (CSV upload) |
| `/api/download/<filename>` | GET | Download results CSV |
| `/api/history` | GET | Get prediction history |
| `/api/history/clear` | POST | Clear prediction history |
| `/api/training-results` | GET | Get model training results |
| `/api/dashboard-stats` | GET | Get dashboard statistics |

### Single Prediction Example
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "duration": 0,
    "protocol_type": "tcp",
    "service": "http",
    "flag": "S0",
    "src_bytes": 0,
    "dst_bytes": 0,
    "count": 400,
    "serror_rate": 0.95
  }'
```

### Response
```json
{
  "prediction": 1,
  "label": "Attack",
  "confidence": 98.5,
  "threat_info": {
    "level": "Threat Detected",
    "color": "#ff1744",
    "icon": "shield-exclamation"
  }
}
```

---

## 🧠 ML Pipeline

```
Data → Clean → Feature Engineer → Encode → Scale → Train → Evaluate → Select Best → Save
```

### Preprocessing
1. **Data Cleaning** — Remove NaN, inf, duplicates
2. **Feature Engineering** — Create byte_ratio, total_bytes, error_rate features
3. **Label Encoding** — Encode protocol_type, service, flag
4. **Standard Scaling** — Normalize all features

### Evaluation Metrics
- **Accuracy** — Overall correctness
- **Precision** — True positive rate
- **Recall** — Sensitivity / Detection rate
- **F1 Score** — Harmonic mean (used for model selection)
- **ROC AUC** — Area under ROC curve
- **Confusion Matrix** — TP, TN, FP, FN breakdown

---

## 📊 Dataset

The framework uses a synthetic dataset modeled after **NSL-KDD** (the industry standard for intrusion detection research).

| Property | Value |
|----------|-------|
| Samples | 25,000 |
| Features | 41+ |
| Classes | Binary (Normal/Attack) |
| Attack Types | DoS, Probe, R2L, U2R |
| Format | CSV |

### Attack Distribution
| Category | Percentage | Description |
|----------|-----------|-------------|
| Normal | 45% | Legitimate traffic |
| DoS | 25% | Denial of Service |
| Probe | 15% | Network scanning |
| R2L | 10% | Remote to Local |
| U2R | 5% | User to Root |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Built as an engineering major project for academic and portfolio purposes.

---

<div align="center">

**⭐ Star this repository if you found it useful! ⭐**

Made with ❤️ and 🐍

</div>
