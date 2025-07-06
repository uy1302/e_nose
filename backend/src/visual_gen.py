"""
E-Nose Dataset Visualization using T-SNE
"""
import argparse
from sklearn.manifold import TSNE
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from config import config

def create_viz(args):
    """Create T-SNE visualization of sensor data"""
    
    # Use config paths if default arguments
    if args.dataset_path == 'default':
        dataset_path = config.get_path('paths', 'data', 'processed') / 'esp32_data.csv'
    else:
        dataset_path = args.dataset_path
        
    if args.output_image_path == 'default':
        output_path = config.get_path('paths', 'docs') / f'{args.project_name}_tsne.png'
    else:
        output_path = args.output_image_path

    print(f"Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    # Get sensor features from config
    sensor_features = config.sensor_features
    print(f"Using sensor features: {sensor_features}")

    # Separate out class from features - use 'label' column
    y = df['label']
    X = df[sensor_features]
    
    print(f"Dataset shape: {X.shape}")
    print(f"Classes found: {y.unique()}")

    # Apply T-SNE
    print("Applying T-SNE transformation...")
    tsne = TSNE(
        n_components=2, 
        verbose=1, 
        random_state=123, 
        perplexity=args.perplexity, 
        n_iter=args.n_iter
    )
    z = tsne.fit_transform(X)
    
    # Create visualization dataframe
    df_viz = pd.DataFrame()
    df_viz["label"] = y
    df_viz["t-SNE 1"] = z[:, 0]
    df_viz["t-SNE 2"] = z[:, 1]

    # Create plot
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df_viz,
        x="t-SNE 1", 
        y="t-SNE 2", 
        hue="label",
        palette="tab10",
        s=50,
        alpha=0.7
    )
    
    plt.title(f"E-Nose Sensor Data T-SNE Visualization\n{len(y)} samples, {len(sensor_features)} features", 
              fontsize=14, fontweight='bold')
    plt.xlabel("t-SNE Component 1", fontsize=12)
    plt.ylabel("t-SNE Component 2", fontsize=12)
    plt.legend(title="Smell Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Save plot
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    if args.show:
        plt.show()
    
    plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='E-Nose Dataset T-SNE Visualization')

    # General args
    parser.add_argument('--project_name', type=str, default='enose_smell_viz', 
                       help='Name of project for output file')
    parser.add_argument('--dataset_path', type=str, default='default', 
                       help='Path to dataset CSV file (default: use config path)')
    parser.add_argument('--output_image_path', type=str, default='default', 
                       help='Output image path (default: use config docs path)')
    
    # T-SNE parameters
    parser.add_argument('--perplexity', type=int, default=30, 
                       help='T-SNE perplexity parameter')
    parser.add_argument('--n_iter', type=int, default=1000, 
                       help='T-SNE number of iterations')
    parser.add_argument('--show', action='store_true', 
                       help='Show plot window')

    args = parser.parse_args()
    create_viz(args)