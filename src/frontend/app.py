import streamlit as st
from sidebar.sidebar import Sidebar
from chat import Chat

st.title("PDF Expert Assistant")

#starting the app, the Assistant greets the user 
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{
        "role": 'assistant',
        "content": 'Hi, I am a PDF Expert Assistant, how can I help you?'
                   ' You may upload a PDF file'
                   ' so I can answer your questions about it!'
    }]

#we write every message on the UI
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

Chat()      
Sidebar()

