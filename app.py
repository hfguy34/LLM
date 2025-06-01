import streamlit as st
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import requests





# Set your HF API key here
HF_API_KEY = st.secrets["api"]["hf_api_key"]


# Select a suitable LLM from Hugging Face Hub
HF_MODEL = "google/gemma-3n-E4B-it-litert-preview"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

HF_API_URL = "https://api-inference.huggingface.co/models/google/gemma-3n-E4B-it-litert-preview"

st.title("హెల్త్ రిపోర్ట్ తెలుగులో విశ్లేషణ")
st.markdown("మీ మెడికల్ రిపోర్ట్‌ను అప్‌లోడ్ చేసి, ఫలితాన్ని తెలుగులో తెలుసుకోండి.")

uploaded_file = st.file_uploader("Upload Health Report (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

def extract_text(file):
    if file.type == "application/pdf":
        images = convert_from_bytes(file.read())
        return "\n".join(pytesseract.image_to_string(img) for img in images)
    else:
        image = Image.open(file)
        return pytesseract.image_to_string(image)

def query_llm_telugu(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 700}
    }
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()[0]['generated_text'].split(prompt)[-1].strip()
        except:
            return response.json()[0]['generated_text']
    else:
        return f"Error: {response.status_code} - {response.text}"

if uploaded_file:
    with st.spinner("Reading and analyzing the report..."):
        extracted_text = extract_text(uploaded_file)

        prompt = f"""
        క్రింది మెడికల్ టెస్ట్ రిపోర్ట్ ఆధారంగా తెలుగు భాషలో వివరించండి. 
        ప్రతి టెస్ట్ పేరు, విలువ, సాధారణ శ్రేణి మరియు ఆరోగ్య సూచనను వివరించండి.

        రిపోర్ట్ వివరాలు:
        {extracted_text}
        """

        telugu_response = query_llm_telugu(prompt)

        st.subheader("తెలుగు వివరాలు:")
        st.write(telugu_response)

        if st.checkbox("Show Extracted Text (English)"):
            st.text_area("Extracted Report Text", extracted_text, height=200)
