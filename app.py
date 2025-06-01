import streamlit as st
import requests

# Hardcoded Hugging Face API token (replace with yours)
HF_API_TOKEN = "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"
HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-3n-E4B-it-litert-preview"  # example model

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # GPT2 returns a list of generated texts
        return data[0]['generated_text']
    else:
        return f"Error: {response.status_code} {response.text}"

st.title("Hugging Face Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:")
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    payload = {
        "inputs": user_input,
        "parameters": {"max_length": 100, "do_sample": False}
    }
    bot_response = query_huggingface(payload)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
