from llama_cpp import Llama
import pandas as pd

class LLM:
    def __init__(self, model_path):
        self.model_raw_name = model_path.name
        self.model_path = f"../llm/{model_path.name}"
        self.llm = Llama(model_path=self.model_path, n_ctx=2048, verbose=False)

    def get_name(self):
        return self.llm.metadata.get("general.name", self.model_raw_name)
    
    def gen_answer(self, prompt, question):
        response = self.llm.create_chat_completion(
            messages = [
                { "role": "system", "content": prompt },
                { "role": "user", "content": question }
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        self.llm.reset()
        return answer




class DatasetManager:
    def __init__(self):
        self.dataset_logging_df = None
        self.question_list_df = None
        self.conference_paper_df = None

    # ----------------------------------------------------------------------
    # Dataset Logging

    def load_dataset_logging(self, path: str) -> int:
        COLUMNS=[
            "question_id",
            "model",
            "year",
            "title",
            "venue",
            "venue_type",
            "paper_id",
            "abstract",
            "filepath",
            "question",
            "question_type",
            "annotator",
            "model_generated",
            "q_prompt",
            "answer"
        ]

        try:
            self.dataset_logging_df = pd.read_csv(path)

        except FileNotFoundError:
            self.dataset_logging_df = pd.DataFrame(
                columns=COLUMNS
            )

            print("There is no content, creating a new one...")

            self.dataset_logging_df.to_csv(
                path,
                index=False,
                quoting=1
            )

        if list(self.dataset_logging_df.columns) != COLUMNS:
            return 1

        return 0

    def get_num_sample(self) -> int:
        if self.dataset_logging_df is None:
            return 0

        return self.dataset_logging_df.shape[0]

    # ----------------------------------------------------------------------
    # Question List

    def load_question_list(self, path) -> int:
        COLUMNS=[
            "question_id",
            "paper_id",
            "question",
            "question_type",
            "annotator",
            "model_generated",
            "q_prompt"
        ]

        try:
            self.question_list_df = pd.read_csv(path)

        except Exception as e:
            print(f"Question List Error: {e}")
            return 1

        if list(self.question_list_df.columns) != COLUMNS:
            return 2

        return 0

    # ----------------------------------------------------------------------
    # Conference Paper

    def load_conference_paper(self, path) -> int:
        COLUMNS = [
            "paper_id",
            "year",
            "title",
            "venue",
            "venue_type",
            "abstract",
            "filepath"
        ]

        try:
            self.conference_paper_df = pd.read_csv(path)

        except Exception as e:
            print(f"Conference Paper Error: {e}")
            return 1

        if list(self.conference_paper_df.columns) != COLUMNS:
            return 2

        return 0


    def is_upload_all(self) -> bool:
        return (
            self.dataset_logging_df is not None
            and self.question_list_df is not None
            and self.conference_paper_df is not None
        )
















