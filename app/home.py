import streamlit as st
import pandas as pd

from core import LLM, DatasetManager


if __name__ == '__main__':
    st.title("Dataset Maker for AI Hallucination")

    
    if "manager" not in st.session_state:
        st.session_state.manager = DatasetManager()

    if not st.session_state.manager.is_upload_all():
        st.session_state.dataset_logging_csv = st.file_uploader("Choose csv file for keeping chat answer", type="csv") 
        if st.session_state.dataset_logging_csv is not None:
            if st.session_state.manager.load_dataset_logging(st.session_state.dataset_logging_csv):
                st.warning("Wrong format!")
            else:
                st.success("Upload complete!")

        st.session_state.question_list_csv = st.file_uploader("Choose csv file containing list of question", type="csv") 
        if st.session_state.question_list_csv is not None:
            match st.session_state.manager.load_question_list(st.session_state.question_list_csv):
                case 1:
                    st.warning("Fail to load csv")
                case 2:
                    st.warning("Wrong format!")
                case _:
                    st.success("Upload complete!")

        st.session_state.conference_paper_csv = st.file_uploader("Choose csv file containing list of conference paper", type="csv") 
        if st.session_state.conference_paper_csv is not None:
            match st.session_state.manager.load_conference_paper(st.session_state.conference_paper_csv):
                case 1:
                    st.warning("Fail to load csv")
                case 2:
                    st.warning("Wrong format!")
                case _:
                    st.success("Upload complete!")
    else:
        st.subheader("All files are uploaded!")

    st.header(f"Current sample: {st.session_state.manager.get_num_sample() if st.session_state.manager.is_upload_all() else 'None'}")

    if st.session_state.manager.is_upload_all():
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Question"):
                st.switch_page("pages/question.py")
        with col2:
            if st.button("Conference"):
                st.switch_page("pages/conference.py")

        


