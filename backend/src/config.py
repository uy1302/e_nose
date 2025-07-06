"""
Configuration module for E-Nose project
"""
import os
import yaml
from pathlib import Path

class Config:
    """Configuration class to manage project settings"""
    
    def __init__(self, config_path="../configs/config.yaml"):
        """
        Initialize configuration
        
        Args:
            config_path (str): Path to config YAML file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_paths()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        config_file = Path(__file__).parent / self.config_path
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Config file not found: {config_file}")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self):
        """Return default configuration if config file is not available"""
        return {
            'paths': {
                'data': {
                    'raw': 'data/raw',
                    'processed': 'data/processed',
                    'formatted_data': 'data/processed/formatted_data',
                    'decoder_scaler': 'data/processed/decoder_scaler'
                },
                'models': 'models',
                'output': 'data/processed',
                'docs': 'docs'
            },
            'models': {
                'ann': 'models/ann_model.h5',
                'ann_best': 'models/ann_model_best.h5',
                'random_forest': 'models/random_forest_model.pkl',
                'xgboost': 'models/xgboost_model.json'
            },
            'sensors': {
                'features': ['MQ2', 'MQ3', 'MQ4', 'MQ6', 'MQ7', 'MQ135', 'TEMP', 'HUMI']
            }
        }
    
    def _setup_paths(self):
        """Setup base paths relative to project root"""
        self.project_root = Path(__file__).parent.parent
        
    def get_path(self, *keys):
        """
        Get path from config
        
        Args:
            *keys: Keys to navigate through config dict
            
        Returns:
            Path: Absolute path
        """
        config_section = self.config
        for key in keys:
            config_section = config_section[key]
        
        return self.project_root / str(config_section)
    
    def get_model_path(self, model_name):
        """
        Get model file path
        
        Args:
            model_name (str): Name of the model
            
        Returns:
            Path: Absolute path to model file
        """
        return self.project_root / self.config['models'][model_name]
    
    def get_preprocessing_path(self, item_name):
        """
        Get preprocessing file path
        
        Args:
            item_name (str): Name of preprocessing item
            
        Returns:
            Path: Absolute path to preprocessing file
        """
        return self.project_root / self.config['preprocessing'][item_name]
    
    @property
    def sensor_features(self):
        """Get sensor feature names"""
        return self.config['sensors']['features']
    
    @property
    def classes(self):
        """Get class names"""
        return self.config.get('classes', [])

# Global config instance
config = Config() 