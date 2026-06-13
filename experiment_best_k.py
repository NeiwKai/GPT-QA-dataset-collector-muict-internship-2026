from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from umap import UMAP
from sklearn.manifold import TSNE

df = pd.read_csv("merged_dataset_logging.csv")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    df["question"].tolist(),
    normalize_embeddings=True
)

# Reduce to 2D for visualization
'''
reducer = UMAP(
    n_components=2,
    n_neighbors=30,
    min_dist=0.1,
    metric="cosine",
    random_state=42
)
'''
reducer = TSNE(
    n_components=2, 
    perplexity=30, 
    init='pca', 
    random_state=42
)

embeddings_2d = reducer.fit_transform(embeddings)


fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for ax, k in zip(axes.ravel(), range(3, 11)):
    labels = KMeans(
        n_clusters=k,
        random_state=42,
        n_init="auto"
    ).fit_predict(embeddings)

    ax.scatter(
        embeddings_2d[:, 0],
        embeddings_2d[:, 1],
        c=labels,
        cmap="tab20",
        s=10
    )

    ax.set_title(f"k={k}")
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.show()
