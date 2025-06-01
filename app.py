import streamlit as st
import requests

st.set_page_config(page_title="LLM Health Chatbot", layout="wide")

# Load API key securely
HF_API_KEY = st.secrets["api"]["hf_api_key"]
HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

st.title("💬 హెల్త్ LLM చాట్‌బాట్ (Health LLM Chatbot in Telugu)")
st.markdown("మీ ఆరోగ్య నివేదికలపై తెలుగులో చాట్ చేయండి!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Function to call LLM
def query_llm(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 700,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            output = response.json()[0]['generated_text']
            return output.split(prompt)[-1].strip()
        except:
            return response.json()[0]['generated_text']
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Handle user input
user_prompt = st.chat_input("మీ ప్రశ్నను తెలుగులో టైప్ చేయండి...")
if user_prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("సమాధానం రూపొందించబడుతుంది..."):
            reply = query_llm(user_prompt)
            st.markdown(reply)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
