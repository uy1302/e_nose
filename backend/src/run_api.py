#!/usr/bin/env python3
"""
Production runner for E-Nose Flask API
"""
import os
import sys
import logging
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from api import app

def setup_logging():
    """Setup logging configuration"""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/api.log') if os.path.exists('logs') else logging.NullHandler()
        ]
    )

def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Configuration from environment variables
    config = {
        'host': os.getenv('API_HOST', '0.0.0.0'),
        'port': int(os.getenv('API_PORT', 5000)),
        'debug': os.getenv('API_DEBUG', 'False').lower() == 'true',
        'threaded': os.getenv('API_THREADED', 'True').lower() == 'true'
    }
    
    logger.info("Starting E-Nose API Server")
    logger.info(f"Configuration: {config}")
    
    try:
        app.run(**config)
    except KeyboardInterrupt:
        logger.info("API Server stopped by user")
    except Exception as e:
        logger.error(f"API Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 