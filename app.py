import streamlit as st
st.set_page_config(page_title="🩺 AI Medical Assistant🤖", page_icon=":robot:", layout="wide")

from pathlib import Path
import google.generativeai as genai
from google.generativeai import types
api_key = st.secrets["GOOGLE_API_KEY"]

# Custom CSS for professional medical styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            padding: 0.5rem 2rem;
            font-size: 1.1rem;
            border-radius: 30px;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        .upload-section {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
        }
        h2 {
            color: #34495e;
            font-size: 1.8rem;
        }
    </style>
""", unsafe_allow_html=True)

#configure api key
genai.configure(api_key = api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

system_prompt = """You are a professional medical AI assistant with expertise in analyzing medical images and providing detailed medical insights. Your role is to:
1. Analyze medical images with high accuracy and attention to detail
2. Provide clear, professional medical observations
3. Highlight any concerning findings that require attention
4. Use medical terminology appropriately while ensuring explanations are understandable
5. Maintain patient confidentiality and medical ethics
6. Remind users that your analysis should not replace professional medical opinions

Please analyze the provided medical image and provide your insights."""

chat_session = model.start_chat(
  history=[
    {"role": "user", "parts": system_prompt},
    {"role": "model", "parts": "I understand my role as a medical AI assistant. I will analyze medical images professionally while maintaining ethical standards and providing clear, detailed insights. I will always remind users that my analysis should complement, not replace, professional medical opinions."}
  ]
)

# Header Section with columns for centering
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🩺 AI Medical Image Analyzer – Smart Diagnostics with AI 👩‍⚕️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Empowering Healthcare with AI – Smarter Image Analysis for Better Patient Outcomes 🏥📡</p>", unsafe_allow_html=True)

# Main content in container
with st.container():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
        st.markdown("### 📤 Upload Medical Image")
        st.markdown("Support formats: JPEG, PNG, JPG")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            
        if st.button("Generate the Analysis..."):
            if uploaded_file is not None:
                with st.spinner('Analyzing image... Please wait.'):
                    image_data = uploaded_file.getvalue()
                    response = chat_session.send_message(
                        {
                            "role": "user",
                            "parts": [
                                {"text": "Please analyze this medical image:"},
                                {"inline_data": {"mime_type": uploaded_file.type, "data": image_data}}
                            ]
                        }
                    )
                    st.markdown("<div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
                    st.markdown("### 📋 Analysis Results")
                    st.write(response.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.info('⚠️ Disclaimer: This analysis is generated by AI and should not be considered as a replacement for professional medical advice.')
            else:
                st.warning("⚠️ Please upload an image before requesting analysis.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Developed for Healthcare Professionals | Powered by Advanced AI Technology</p>
        <p style='margin-top: 0.5rem;'>Developed with ❤️ by Fatima Nazeer</p>
    </div>
""", unsafe_allow_html=True)
