from acl_anthology import Anthology
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

years = ["2020", "2021", "2022", "2023", "2024", "2025"]
venues = {
    "acl": "conference",
    "emnlp": "conference",
    "tacl": "journal",
    "naacl": "conference",
    "cl": "journal"
}

anthology = Anthology.from_repo()
random.seed(42)

df_merged = pd.read_csv("./merged_dataset_logging_cluster.csv")
sample_counts = (
    df_merged
    .groupby(["year", "venue"])
    .size()
    .to_dict()
)

stats = []

for y in years:
    for v, t in venues.items():
        collection = anthology.get(f"{y}.{v}")

        if collection is None:
            continue

        papers = []

        for volume in collection.volumes():
            papers.extend(list(volume.papers()))

        if not papers:
            continue

        sampled_count = sample_counts.get(
            (int(y), v.upper()),
            0
        )

        stats.append({
            "year": int(y),
            "venue": v.upper(),
            "total_papers": len(papers),
            "sampled_papers": sampled_count
        })
stats_df = pd.DataFrame(stats)



# Plot stacked bar
stats_df = stats_df.copy()

stats_df["remaining"] = (
    stats_df["total_papers"]
    - stats_df["sampled_papers"]
)

# Make sure ordering works
stats_df["venue"] = stats_df["venue"].str.upper()
stats_df["year"] = stats_df["year"].astype(int)

venue_order = ["ACL", "EMNLP", "NAACL", "TACL", "CL"]

stats_df["venue"] = pd.Categorical(
    stats_df["venue"],
    categories=venue_order,
    ordered=True
)

stats_df = stats_df.sort_values(["year", "venue"])

x = np.arange(len(stats_df))

fig, ax = plt.subplots(figsize=(15, 7))

ax.bar(
    x,
    stats_df["sampled_papers"],
    label="Sampled Papers"
)

ax.bar(
    x,
    stats_df["remaining"],
    bottom=stats_df["sampled_papers"],
    label="Not Sampled"
)

# Counts
for i in range(len(stats_df)):
    sampled = stats_df.iloc[i]["sampled_papers"]
    total = stats_df.iloc[i]["total_papers"]

    # sample count
    ax.text(
        i,
        sampled + total * 0.01,
        f"n={sampled}",
        ha="center",
        fontsize=8
    )

    # total count
    ax.text(
        i,
        total + total * 0.03,
        f"{total}",
        ha="center",
        fontsize=8
    )

# Venue labels
ax.set_xticks(x)
ax.set_xticklabels(stats_df["venue"])

# Year labels
years = sorted(stats_df["year"].unique())

for year in years:
    idx = stats_df.index[stats_df["year"] == year]

    start = np.where(stats_df["year"] == year)[0][0]
    end = np.where(stats_df["year"] == year)[0][-1]

    center = (start + end) / 2

    ax.text(
        center,
        -0.10,
        str(year),
        ha="center",
        transform=ax.get_xaxis_transform(),
        fontsize=12,
        fontweight="bold"
    )

    # Optional separator line
    ax.axvline(end + 0.5, linestyle="--", alpha=0.3)

ax.set_ylabel("Number of Papers")
ax.set_title(
    "ACL Anthology Papers and 5% Sampled Dataset by Venue and Year (for 800 sample)"
)

ax.legend()

plt.tight_layout()
plt.show()
