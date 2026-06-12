import pandas as pd

# Read CSV files
df_conference = pd.read_csv("conference_paper.csv")
df_dataset = pd.read_csv("dataset_logging.csv")

columns = ["year", "title", "venue", "venue_type"]

lookup = df_conference.set_index("paper_id")

for col in columns:
    df_dataset[col] = df_dataset["paper_id"].map(lookup[col])

df_dataset.to_csv("dataset_logging.csv", index=False, quoting=1)
