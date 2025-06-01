import streamlit as st
import requests

HF_API_TOKEN = st.secrets["HF_API_TOKEN"]
MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/google/gemma-3n-E4B-it-litert-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chat with Google Gemma Model")

user_input = st.text_input("Ask your question:", key="input")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 100}
    }

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        assistant_reply = result[0]["generated_text"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    else:
        st.error(f"API Error {response.status_code}: {response.text}")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
