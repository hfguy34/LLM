import streamlit as st
import requests

# Set your Hugging Face API token here or use Streamlit secrets
HF_API_TOKEN = st.secrets["HF_API_TOKEN"]

# Define the DeepSeek-R1-0528 model endpoint
MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/deepseek-ai/DeepSeek-R1-0528"

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the app title
st.title("Chat with DeepSeek-R1-0528")

# Input field for user messages
user_input = st.text_input("You:", "")

# Send button to submit the message
if st.button("Send") and user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare the conversation history for the model
    conversation = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]

    # Define headers for the API request
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Define the payload for the API request
    payload = {
        "inputs": conversation
    }

    # Make the API request to Hugging Face
    response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload)

    # Check if the response is successful
    if response.status_code == 200:
        # Extract the assistant's reply from the response
        assistant_reply = response.json()[0]["generated_text"]
        # Append assistant's reply to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    else:
        # Display error message if the API request fails
        st.error(f"API error: {response.status_code} - {response.text}")

# Display the chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**DeepSeek:** {msg['content']}")
