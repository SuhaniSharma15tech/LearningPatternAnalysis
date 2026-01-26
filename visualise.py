import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1. Load Data
df = pd.read_csv('dimensionallyReduced.csv')
data_points = df.to_numpy()

# 2. Your Centroids
centroiddict = {
    'cluster1': np.array([0.7054, 0.4618, 0.5365, 0.5921, 0.2946, 0.3319, 0.6724]),
    'cluster2': np.array([0.6190, 0.6829, 0.4978, 0.5221, 0.3390, 0.5220, 0.3622]),
    'cluster3': np.array([0.6501, 0.2939, 0.4782, 0.2972, 0.4520, 0.5311, 0.5003]),
    'cluster4': np.array([0.6825, 0.7067, 0.4865, 0.4366, 0.6816, 0.4835, 0.5587]),
    'cluster5': np.array([0.6605, 0.3252, 0.5337, 0.6655, 0.6448, 0.5231, 0.4281])
}
centroids_matrix = np.array(list(centroiddict.values()))

# 3. Assign Points to Clusters
distances = np.linalg.norm(data_points[:, np.newaxis] - centroids_matrix, axis=2)
cluster_labels = np.argmin(distances, axis=1)

# 4. Dimensionality Reduction (PCA)
pca = PCA(n_components=2)
# Fit PCA on combined data for consistent projection
all_2d = pca.fit_transform(np.vstack([data_points, centroids_matrix]))
data_2d = all_2d[:-5]
centroids_2d = all_2d[-5:]

# 5. Plotting Scatter
plt.figure(figsize=(10, 6))
for i in range(5):
    idx = (cluster_labels == i)
    plt.scatter(data_2d[idx, 0], data_2d[idx, 1], s=10, alpha=0.5, label=f'Cluster {i+1}')
    plt.scatter(centroids_2d[i, 0], centroids_2d[i, 1], s=200, marker='*', edgecolors='black')

plt.title("Cluster Visualization (7D projected to 2D)")
plt.legend()
plt.savefig('clusters_2d.png')