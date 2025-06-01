import streamlit as st
import requests

# WARNING: Hardcoding API keys is NOT secure, only do this for quick local testing
API_KEY = "sk-3aa2884c5e144181ac166d11665e7a02"
DEESEEK_API_URL = "https://api.deepseek.ai/chat"  # Replace with actual Deepseek API endpoint

def get_deepseek_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": user_input,
    }
    try:
        response = requests.post(DEESEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        answer = data.get("answer") or data.get("response") or "No response found."
        return answer
    except Exception as e:
        return f"Error: {e}"

st.title("Deepseek Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("You:")
    submit = st.form_submit_button("Send")

if submit and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_response = get_deepseek_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Deepseek:** {msg['content']}")
