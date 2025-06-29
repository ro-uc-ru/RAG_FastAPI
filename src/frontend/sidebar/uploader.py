import streamlit as st
import requests

#request to post pdf for the assistant
url = 'http://localhost:8080/post-pdf'

def upload_file():
    file = st.file_uploader("Upload your PDF for the assistant", type = "pdf")

    if file:
        try:
            #while the request is being processed, we include a spinner
            with st.spinner("Uploading file"):
                files = {"file": (file.name, file.getvalue(), "application/pdf")}
                response = requests.post(url, files = files)
                if response.status_code == 200:
                    st.success(response.json().get('message'))
                else:
                    st.error(f"Error {response.status_code}")
        except Exception as e:
            st.error(f"Error uploading file {str(e)}")

