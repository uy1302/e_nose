@echo off
REM E-Nose Project Management Script
REM Usage: run_project.bat [command]

if "%1"=="" goto :show_help
if "%1"=="help" goto :show_help
if "%1"=="setup" goto :setup
if "%1"=="preprocess" goto :preprocess
if "%1"=="train-ann" goto :train_ann
if "%1"=="train-tree" goto :train_tree
if "%1"=="train-all" goto :train_all
if "%1"=="predict" goto :predict
if "%1"=="compare" goto :compare
if "%1"=="visualize" goto :visualize
if "%1"=="app" goto :app
if "%1"=="clean" goto :clean
goto :invalid_command

:show_help
echo 🔬 E-Nose Project Management
echo.
echo Available commands:
echo   setup       - Run project setup
echo   preprocess  - Preprocess data
echo   train-ann   - Train ANN model
echo   train-tree  - Train tree models (RF + XGBoost)
echo   train-all   - Train all models
echo   predict     - Run prediction with sample data
echo   compare     - Compare model performance
echo   visualize   - Generate visualizations
echo   app         - Run web application
echo   clean       - Clean temporary files
echo   help        - Show this help
echo.
echo Example: run_project.bat setup
goto :end

:setup
echo 🚀 Running project setup...
python scripts\setup.py
goto :end

:preprocess
echo 📊 Preprocessing data...
cd src
python preprocessing.py
cd ..
goto :end

:train_ann
echo 🧠 Training ANN model...
cd src
python train_ann.py
cd ..
goto :end

:train_tree
echo 🌳 Training tree models...
cd src
python train_tree_model.py
cd ..
goto :end

:train_all
echo 🏋️ Training all models...
cd src
python train_ann.py
python train_tree_model.py
cd ..
goto :end

:predict
echo 🔮 Running prediction...
cd src
python predict.py
cd ..
goto :end

:compare
echo 📈 Comparing models...
cd src
python compare_model.py
cd ..
goto :end

:visualize
echo 📊 Generating visualizations...
cd src
python visual_gen.py
cd ..
goto :end

:app
echo 🌐 Starting web application...
cd src
python app.py
cd ..
goto :end

:clean
echo 🧹 Cleaning temporary files...
del /q *.tmp 2>nul
del /q *.cache 2>nul
del /q src\*.tmp 2>nul
del /q src\*.cache 2>nul
rd /s /q __pycache__ 2>nul
rd /s /q src\__pycache__ 2>nul
echo Temporary files cleaned.
goto :end

:invalid_command
echo ❌ Invalid command: %1
echo Run 'run_project.bat help' for available commands.
goto :end

:end 