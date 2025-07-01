"""
E-Nose Source Package

This package contains the main source code for the E-Nose project including:
- Configuration management
- Data preprocessing
- Model training and evaluation
- Prediction functionality
- Web application
"""

__version__ = "1.0.0"
__author__ = "E-Nose"

# Import main modules for easier access
from .config import config
from .predict import predict_with_models

__all__ = [
    'config',
    'predict_with_models'
] 