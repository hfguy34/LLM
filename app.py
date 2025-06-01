import streamlit as st
import requests

# Your Hugging Face API token
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

# Google FLAN-T5 Large model endpoint on Hugging Face
MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/google/flan-t5-large"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chat with Google FLAN-T5 Large Model")

user_input = st.text_input("Ask your question:", key="input")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare prompt for FLAN-T5: just the user input (FLAN-T5 is instruction tuned)
    # We only send the latest user message for simplicity here
    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 100}
    }

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

    response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        # FLAN-T5 returns list of dicts with 'generated_text'
        assistant_reply = result[0]["generated_text"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    else:
        st.error(f"API Error {response.status_code}: {response.text}")

# Show conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
