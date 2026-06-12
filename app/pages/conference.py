import streamlit as st

from core import LLM, DatasetManager

def append_conference():
    df_conference = st.session_state.manager.conference_paper_df

    paper_id = df_conference["paper_id"].iloc[-1] + 1
    year = st.session_state.year
    title = st.session_state.title
    venue = st.session_state.venue
    venue_type = st.session_state.venue_type
    abstract = st.session_state.abstract
    filepath = st.session_state.filepath

    df_conference.loc[len(df_conference)] = {
        "paper_id": paper_id,
        "year": year,
        "title": title,
        "venue": venue,
        "venue_type": venue_type,
        "abstract": abstract,
        "filepath": filepath
    }

    df_conference.to_csv(f"../{st.session_state.conference_paper_csv.name}", index=False, quoting=1)

    st.session_state.conference_source = ""
    st.session_state.filepath = ""
    st.session_state.abstract = ""

st.title("Conference Paper")

if st.button("Back"):
    st.switch_page("home.py")


if "manager" in st.session_state and st.session_state.manager.is_upload_all():
    df_conference = st.session_state.manager.conference_paper_df

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: 
        st.text_input("year:", key="year", placeholder="Year; e.g. 2018")
    with col2:
        st.text_input("title:", key="title", placeholder="Title; e.g. PyTorch")
    with col3:
        st.text_input("venue:", key="venue", placeholder="e.g. acl")
    with col4:
        st.text_input("venue_type", key="venue_type", placeholder="e.g. conference")
    with col5:
        st.text_input("filepath:", key="filepath", placeholder="./paper/xxx.pdf; e.g. ./paper/pytorch.pdf")
    st.text_area("abstract:", key="abstract")

    if st.button("Submit", on_click=append_conference):
        st.success("Append new conference source!")

    container = st.container()
    with container:
        st.subheader("Conference Paper List")
        st.markdown(f":blue-background[Total Conference: {len(df_conference)}]")
        st.dataframe(df_conference)

else:
    st.warning("There is a problem with previous state")
