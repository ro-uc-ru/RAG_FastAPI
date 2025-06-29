import streamlit as st
import requests

QUERY_URI ="http://localhost:8080/query"


#this class is to show the chat with the assistant
class Chat:
    #accepting user input and saving it to messages
    def _accept_input(self):
        if prompt := st.chat_input():
            st.session_state.messages.append({
                "role": 'user',
                "content": prompt
            })
            with st.chat_message('user'):
                st.write(prompt)
    
    #generating response, requesting the query to the agent and saving and showing the answer
    def generate_response(self):
        self._accept_input()
        if st.session_state.messages[-1]['role'] != 'assistant':
            with st.chat_message('assistant'):
                with st.spinner("Loading model response, please wait..."):
                    try:
                        response = requests.post(QUERY_URI, json = {'query': st.session_state.messages[-1]['content']})
                        st.write(response.json().get('answer'))
                        #we only want the answer
                        message = {
                            'role': 'assistant',
                            'content': response.json().get('answer')
                        }
                        st.session_state.messages.append(message)
                    except Exception as e:
                        st.error(str(e))
    
    def __init__(self):
        self.generate_response()
    
