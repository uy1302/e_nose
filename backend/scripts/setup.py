"""
Setup script for E-Nose project
"""
import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Successfully installed all packages!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    
    return True

def check_directory_structure():
    """Check if all required directories exist"""
    print("📁 Checking directory structure...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "src",
        "models", 
        "data/raw",
        "data/processed",
        "data/processed/formatted_data",
        "data/processed/decoder_scaler",
        "configs",
        "scripts",
        "docs"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
            print(f"⚠️  Missing directory: {dir_path}")
        else:
            print(f"✅ Found: {dir_path}")
    
    if missing_dirs:
        print(f"\n📁 Creating missing directories...")
        for dir_path in missing_dirs:
            full_path = project_root / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {dir_path}")
    
    return True

def check_config_files():
    """Check if config files exist"""
    print("⚙️  Checking configuration files...")
    
    project_root = Path(__file__).parent.parent
    config_file = project_root / "configs" / "config.yaml"
    
    if config_file.exists():
        print("✅ Configuration file found!")
        return True
    else:
        print("⚠️  Configuration file not found!")
        return False

def run_setup():
    """Run complete setup"""
    print("🚀 Starting E-Nose project setup...\n")
    
    success = True
    
    # Check directory structure
    if not check_directory_structure():
        success = False
    
    print()
    
    # Check config files
    if not check_config_files():
        success = False
    
    print()
    
    # Install requirements
    if not install_requirements():
        success = False
    
    print()
    
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Put your raw data in data/raw/")
        print("2. Run preprocessing: python src/preprocessing.py")
        print("3. Train models: python src/train_ann.py")
        print("4. Make predictions: python src/predict.py")
    else:
        print("❌ Setup encountered some issues. Please check the output above.")
    
    return success

if __name__ == "__main__":
    run_setup() 