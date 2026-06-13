import pandas as pd
import hdbscan
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from sentence_transformers import SentenceTransformer
import plotly.express as px

if __name__ == '__main__':
    df = pd.read_csv("merged_dataset_logging.csv")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        df["question"].tolist(),
        normalize_embeddings=True
    )


    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init="auto"
    )

    clusters = kmeans.fit_predict(embeddings)


    df["question_type"] = clusters

    for cluster_id in sorted(df["question_type"].unique()):
        if cluster_id == -1:
            continue

        print(f"\n=== Cluster {cluster_id} ===")

        samples = (
            df[df["question_type"] == cluster_id]
            .sample(min(50, len(df[df["question_type"] == cluster_id])))
        )

        for q in samples["question"]:
            print("-", q)

    df.to_csv("merged_dataset_logging_cluster.csv", index=False, quoting=1)
