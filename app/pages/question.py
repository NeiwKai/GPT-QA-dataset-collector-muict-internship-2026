import streamlit as st

from core import LLM, DatasetManager



def gen_answer():
    df_conference = st.session_state.manager.conference_paper_df
    df_question = st.session_state.manager.question_list_df

    paper_id = st.session_state.paper_id
    matched_row = df_conference[
        df_conference["paper_id"] == paper_id
    ].iloc[0]


    question_id = df_question["question_id"].iloc[-1] + 1
    abstract = matched_row["abstract"]
    filepath = matched_row["filepath"]

    year = matched_row["year"]
    title = matched_row["title"]
    venue = matched_row["venue"]
    venue_type = matched_row["venue_type"]

    df_log = st.session_state.manager.dataset_logging_df

    prompt = f"""
    ABSTRACT:
    {abstract}

    ---------------------------------------------------------------------------
    INSTRUCTION: 
    Answer user question based on given abstract.
    """
    llm = st.session_state.llm
    question = st.session_state.question
    question_type = st.session_state.question_type
    annotator = st.session_state.annotator
    model_generated = st.session_state.model_generated
    q_prompt = st.session_state.q_prompt
    answer = llm.gen_answer(prompt, question)

    # Update Dataset
    df_log.loc[len(df_log)] = {
        "question_id": question_id,
        "model": llm.get_name(),
        "year": year,
        "title": title,
        "venue": venue,
        "venue_type": venue_type,
        "paper_id": paper_id,
        "abstract": abstract,
        "filepath": filepath,
        "question": question,
        "question_type": question_type,
        "annotator": annotator,
        "model_generated": model_generated,
        "q_prompt": q_prompt,
        "answer": answer
    }
    df_log.to_csv(f"../{st.session_state.dataset_logging_csv.name}", index=False, quoting=1)

    # Update Question List
    df_question.loc[len(df_question)] = {
        "question_id": question_id,
        "paper_id": paper_id,
        "question": question,
        "question_type": question_type,
        "annotator": annotator,
        "model_generated": model_generated,
        "q_prompt": q_prompt
    }
    df_question.to_csv(f"../{st.session_state.question_list_csv.name}", index=False, quoting=1)

    # Clear text_input
    #st.session_state.paper_id = ""
    st.session_state.question = ""
    st.session_state.question_type = ""


st.title("Question")

if st.button("Back"):
    st.switch_page("home.py")


if "manager" in st.session_state and st.session_state.manager.is_upload_all():
    df_question = st.session_state.manager.question_list_df

    if "model_given" not in st.session_state:
        st.session_state.model_given = False
    if "model_loaded" not in st.session_state:
        st.session_state.model_loaded = False
   

    if not st.session_state.model_given:
        st.session_state.model_path = st.file_uploader("Upload a llm model file", type="gguf")

        if st.session_state.model_path is not None:
            st.session_state.model_given = True
            if "llm" not in st.session_state:
                try:
                    st.session_state.llm = LLM(st.session_state.model_path)
                    st.success("Upload complete!")
                    llm = st.session_state.llm
                    st.write(f"Current Model: {llm.get_name()}")
                    st.session_state.model_loaded = True
                except Exception as e:
                    print(f"Error: {e}")
                    st.warning("Failed to load model, please use .gguf")



    if st.session_state.model_loaded and st.session_state.model_given:
        if st.button("Change Model"):
            st.session_state.model_given = False
            st.rerun()

        df_conference = st.session_state.manager.conference_paper_df
        # Show paper
        if "paper_id" in st.session_state:
            container = st.container()
            if st.session_state.paper_id != "":
                with container:
                    paper_id = st.session_state.paper_id
                    matched_row = df_conference[df_conference["paper_id"]==paper_id].iloc[0]
                    st.subheader(f"{matched_row['title']}, {matched_row['year']}")

                    col1_a, col2_a = st.columns(2)
                    with col1_a:
                        st.markdown(f":yellow-background[**Venue:** {matched_row['venue']}]")
                    with col2_a:
                        st.markdown(f":green-background[**Venue Type:** {matched_row['venue_type']}]")

                    col1_b, col2_b = st.columns(2)
                    with col1_b:
                        st.markdown(f":red-background[**Paper ID:** {matched_row['paper_id']}]")
                    with col2_b:
                        st.markdown(f":orange-background[**Filepath:** `{matched_row['filepath']}`]")
                    st.write(matched_row["abstract"])

                    num_question = len(st.session_state.manager.question_list_df[st.session_state.manager.question_list_df["paper_id"]==paper_id])
                    st.markdown(f":blue-background[**Number of question:** {num_question}]")
        # --------------

        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Paper ID:", df_conference["paper_id"].unique(), key="paper_id")
        with col2:
            st.selectbox("Annotator:", ["New", "Hall", "Pun"], key="annotator")
        with col3:
            st.selectbox("Model Generated:", [0, 1], key="model_generated")

        st.text_input("Question Type:", key="question_type", placeholder="e.g. verrify, or Leave it empty if cannot come up with.")
        st.text_area("Question:", key="question")
        st.text_area("Question Prompt:", key="q_prompt", placeholder="Leave it empty if the question is not generated")


        if st.button("Submit", on_click=gen_answer):
            st.success("Append new dataset!")

    container = st.container()
    with container:
        st.subheader("Dataset List")
        st.markdown(f":blue-background[Total Question: {len(st.session_state.manager.dataset_logging_df)}]")
        st.dataframe(st.session_state.manager.dataset_logging_df)

else:
    st.warning("There is a problem with previous state")
