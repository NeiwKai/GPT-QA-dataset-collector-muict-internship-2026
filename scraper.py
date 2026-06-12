from acl_anthology import Anthology
import pandas as pd
import random

years = [ "2023", "2024", "2025" ]
venues = { "acl": "conference", "emnlp": "conference", "tacl": "journal", "naacl": "conference", "cl": "journal" } # { "venue": "type" }


if __name__ == '__main__':
    anthology = Anthology.from_repo()
    random.seed(42)
    df_conference = pd.read_csv("./conference_paper.csv")

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

            sample_size = max(1, int(len(papers) * 0.05))
            sampled_papers = random.sample(papers, sample_size)

            print(
                f"\nYear: {y}, "
                f"Total Papers: {len(papers)}, "
                f"Sampled: {sample_size}"
            )

            for paper in sampled_papers:
                if paper is None or paper.year is None or paper.title is None or paper.abstract is None or paper.pdf.url is None:
                    continue
                df_conference.loc[len(df_conference)] = {
                    "paper_id": df_conference["paper_id"].iloc[-1]+1,
                    "year": paper.year,
                    "title": paper.title,
                    "venue": v,
                    "venue_type": t,
                    "abstract": paper.abstract,
                    "filepath": paper.pdf.url
                }
    df_conference.to_csv("./conference_paper.csv", index=False, quoting=1)
        
        


