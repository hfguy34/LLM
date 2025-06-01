import streamlit as st
import requests

st.title("Chat with Deepseek (Hugging Face)")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare the input for Deepseek huggingface model
    # Usually the input is a string or JSON depending on the model
    # Let's join all previous messages to form the context:
    conversation = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"
    conversation += "Assistant: "
    
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": conversation
    }
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/deepseek/deepseek-chat",  # replace with actual model repo
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        data = response.json()
        # Usually the Hugging Face text-generation models return:
        # [{"generated_text": "..."}]
        generated_text = data[0]["generated_text"]
        
        # Extract only the new assistant reply by removing conversation prompt
        assistant_reply = generated_text[len(conversation):].strip()
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    else:
        st.error(f"API error {response.status_code}: {response.text}")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Deepseek:** {msg['content']}")
