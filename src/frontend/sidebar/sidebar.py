import streamlit as st
from .uploader import upload_file


class Sidebar:
    def __init__(self) -> None:
        with st.sidebar:
            st.title("PDF LOADER")
            upload_file()
