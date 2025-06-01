import streamlit as st
import requests

HF_API_TOKEN = "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"
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 150, "do_sample": True, "top_p": 0.9, "temperature": 0.7},
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]['generated_text']
        else:
            return str(data)
    else:
        return f"HTTP Error: {response.status_code} {response.text}"

st.title("F1 Expert Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Ask me anything about Formula 1:")
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = f"You are a Formula 1 expert. Answer the question clearly and accurately.\nQuestion: {user_input}\nAnswer:"
    bot_response = query_huggingface(prompt)

    if bot_response.startswith(prompt):
        bot_response = bot_response[len(prompt):].strip()

    st.session_state.messages.append({"role": "bot", "content": bot_response})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**F1 Bot:** {msg['content']}")
