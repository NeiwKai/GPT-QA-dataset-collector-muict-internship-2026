# GPT-QA-dataset-collector-muict-internship-2026
About This is a repository that contains an implementation of GPT-based QA dataset collector, jointly conducted with internship student from MUICT in May 2026.

### Prerequisite
-   python version `3.11.9`
-   `pip3 install -r requirements.txt`

### GUI Tool
1.  Navigate into `app` directory. (**_IMPORTANT STEP!!!_**)
2.  `streamlit run home.py`

### Structure
```
.
├── dataset_logging.csv
├── question_list.csv
├── conference_paper.csv
├── llm
│   └── gemma-3-4b-it-q4_k_m.gguf
└── app
    ├── home.py
    ├── core.py
    └── pages
```

#### Additional tools
`main.py`
-   Old pipeline version.
-   Read `question_list.csv`, `conference_paper.csv` and update `dataset_logging.csv`.

`scraper.py`
-   An `acl-anthology` api calling for scraping conference paper from different years, events, etc.
-   Give the range of years and list of venue. It will scrape 5% of each years.
-   Will update the `conference_paper.csv`.

`clustering.py`
-   An clustering technique using k-means for generating "question_type" columns.
-   Will update the `question_type.csv`.

#### File explanation
`merged_dataset_logging.csv`
-   A merge version of New and Hall `dataset_logging.csv`.
-   "question_type" is still empty.

`merged_question_list.csv`
-   A merge version of New and Hall `question_list.csv`.
-   "question_type" is still empty.

`merged_conference_paper.csv`
-   A merge version of New and Hall `conference_paper.csv`.
