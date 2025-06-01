import streamlit as st
import requests

st.set_page_config(page_title="LLM Health Chatbot", layout="wide")

# Load API key securely
HF_API_KEY = st.secrets["api"]["hf_api_key"]
HF_API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-0528"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

st.title("💬 హెల్త్ LLM చాట్‌బాట్ (Health LLM Chatbot in Telugu)")
st.markdown("మీ ఆరోగ్య నివేదికలపై తెలుగులో చాట్ చేయండి!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to build prompt with conversation history
def build_prompt():
    conversation = (
        "ఈ సంభాషణలో మీరు ఆరోగ్య సహాయకుడిగా వ్యవహరిస్తున్నారు. "
        "దయచేసి మీ సమాధానాలను తెలుగులోనే ఇవ్వండి.\n\n"
    )
    for msg in st.session_state.messages[-6:]:  # last 6 messages for context
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    conversation += "Assistant:"
    return conversation

# Function to query the LLM API
def query_llm():
    prompt = build_prompt()
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 700,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
    except Exception as e:
        return f"❌ API request failed: {e}"

    if response.status_code == 200:
        try:
            output = response.json()[0]["generated_text"]
            # Remove prompt part to get only new response
            return output[len(prompt):].strip()
        except Exception as e:
            return f"❌ Response parsing error: {e}"
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Display existing chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("మీ ప్రశ్నను తెలుగులో టైప్ చేయండి...")
if user_prompt:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("సమాధానం రూపొందించబడుతుంది..."):
            reply = query_llm()
            st.markdown(reply)

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
