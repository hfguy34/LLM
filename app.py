import streamlit as st
import requests

# Replace with your actual Deepseek API URL and API key if needed
DEESEEK_API_URL = "https://api.deepseek.ai/chat"  # example endpoint
API_KEY = "sk-ebf6cf5d2143487bac8effece0ec2f12"

# Function to send user query to Deepseek and get response
def get_deepseek_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": user_input,
        # add other parameters if Deepseek API requires
    }
    
    try:
        response = requests.post(DEESEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Assuming the response JSON contains an answer field
        answer = data.get("answer") or data.get("response") or "No response found."
        return answer
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Deepseek Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input.strip():
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response from Deepseek
    bot_response = get_deepseek_response(user_input)
    
    # Append bot message
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    
    # Clear input box
    st.session_state.input = ""

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Deepseek:** {msg['content']}")

