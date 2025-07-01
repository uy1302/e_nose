#!/bin/bash
# E-Nose Project Management Script
# Usage: ./run_project.sh [command]

show_help() {
    echo "🔬 E-Nose Project Management"
    echo ""
    echo "Available commands:"
    echo "  setup       - Run project setup"
    echo "  preprocess  - Preprocess data"
    echo "  train-ann   - Train ANN model"
    echo "  train-tree  - Train tree models (RF + XGBoost)"
    echo "  train-all   - Train all models"
    echo "  predict     - Run prediction with sample data"
    echo "  compare     - Compare model performance"
    echo "  visualize   - Generate visualizations"
    echo "  app         - Run web application"
    echo "  clean       - Clean temporary files"
    echo "  help        - Show this help"
    echo ""
    echo "Example: ./run_project.sh setup"
}

setup() {
    echo "🚀 Running project setup..."
    python scripts/setup.py
}

preprocess() {
    echo "📊 Preprocessing data..."
    cd src
    python preprocessing.py
    cd ..
}

train_ann() {
    echo "🧠 Training ANN model..."
    cd src
    python train_ann.py
    cd ..
}

train_tree() {
    echo "🌳 Training tree models..."
    cd src
    python train_tree_model.py
    cd ..
}

train_all() {
    echo "🏋️ Training all models..."
    cd src
    python train_ann.py
    python train_tree_model.py
    cd ..
}

predict() {
    echo "🔮 Running prediction..."
    cd src
    python predict.py
    cd ..
}

compare() {
    echo "📈 Comparing models..."
    cd src
    python compare_model.py
    cd ..
}

visualize() {
    echo "📊 Generating visualizations..."
    cd src
    python visual_gen.py
    cd ..
}

app() {
    echo "🌐 Starting web application..."
    cd src
    python app.py
    cd ..
}

clean() {
    echo "🧹 Cleaning temporary files..."
    find . -name "*.tmp" -delete 2>/dev/null
    find . -name "*.cache" -delete 2>/dev/null
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    echo "Temporary files cleaned."
}

# Main script logic
case "$1" in
    setup)
        setup
        ;;
    preprocess)
        preprocess
        ;;
    train-ann)
        train_ann
        ;;
    train-tree)
        train_tree
        ;;
    train-all)
        train_all
        ;;
    predict)
        predict
        ;;
    compare)
        compare
        ;;
    visualize)
        visualize
        ;;
    app)
        app
        ;;
    clean)
        clean
        ;;
    help|"")
        show_help
        ;;
    *)
        echo "❌ Invalid command: $1"
        echo "Run './run_project.sh help' for available commands."
        exit 1
        ;;
esac 