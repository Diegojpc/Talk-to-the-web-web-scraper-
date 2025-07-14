# client.py

import requests
import streamlit as st

st.title("Web Scraping Assistant with FastAPI")

if "messages" not in st.session_state:
    st.session_state.messages = []

#--------------- TEXT GENERATION -----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter a URL or text to scrape and summarize:"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)

    try:
        response = requests.post(
            "http://localhost:8000/generate/text",
            json={"prompt": prompt, "model": "v2/en_speaker_1", "temperature": 0.7},
        )
        response.raise_for_status()
        result = response.json()["content"]

        st.session_state.messages.append({"role": "assistant", "content": result})

        with st.chat_message("assistant"):
            st.markdown(result)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")