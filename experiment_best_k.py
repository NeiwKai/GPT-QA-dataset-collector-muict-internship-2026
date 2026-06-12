from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv("merged_dataset_logging.csv")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        df["question"].tolist(),
        normalize_embeddings=True
    )

    scores = []

    for k in range(3, 11):
        kmeans = KMeans(
            n_clusters=k,
            random_state=42,
            n_init="auto"
        )

        labels = kmeans.fit_predict(embeddings)

        score = silhouette_score(embeddings, labels)

        scores.append((k, score))

        print(f"k={k:2d}  silhouette={score:.4f}")


    # Plot the figure
    ks = [k for k, score in scores]
    sils = [score for k, score in scores]

    plt.figure(figsize=(8, 5))

    scatter = plt.scatter(
        ks,
        sils,
        c=sils,
        cmap="viridis",
        s=100
    )

    plt.plot(ks, sils, alpha=0.5)
    plt.colorbar(scatter, label="Silhouette Score")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Silhouette Score")
    plt.title("Silhouette Scores")
    plt.show()
