import pandas as pd

# Read CSV
df_conference = pd.read_csv("conference_paper.csv")
df_dataset = pd.read_csv("dataset_logging.csv")

# Split into title and year
df_conference[["title", "year"]] = df_conference["conference_source"].str.rsplit(
    ",", n=1, expand=True
)
df_dataset[["title", "year"]] = df_dataset["conference_source"].str.rsplit(
    ",", n=1, expand=True
)

# Remove leading/trailing whitespace
df_conference["title"] = df_conference["title"].str.strip()
df_dataset["year"] = df_dataset["year"].str.strip()

df_dataset["title"] = df_dataset["title"].str.strip()
df_dataset["year"] = df_dataset["year"].str.strip()


df_conference = df_conference.drop(columns=["conference_source"])
df_dataset = df_dataset.drop(columns=["conference_source"])

# Save result
df_conference.to_csv("conference_paper.csv", index=False, quoting=1)
df_dataset.to_csv("dataset_logging.csv", index=False, quoting=1)
