# app.py
import streamlit as st
from google import genai
from PIL import Image
import io

# -------------------------------
# 1. Configure Gemini client
# -------------------------------
client = genai.Client(api_key="###########################")
MODEL_NAME = "models/gemini-3-flash-preview"  # free-tier model

# -------------------------------
# 2. System prompt (fixed)
# -------------------------------
SYSTEM_PROMPT = """
You are a historical reasoning assistant.
Explain historical places using evidence-based reasoning.
If an image is provided, analyze architecture, materials, symbols,
and condition before answering.
Focus on WHY, not just facts.
"""

# -------------------------------
# 3. Streamlit UI
# -------------------------------
st.title("🕰️ Historic Places Explorer")
st.write("Ask questions about historic places with or without uploading images.")

# Text input
user_query = st.text_input("Enter your question:")

# Optional image upload
uploaded_file = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg"])

# Button to submit
if st.button("Ask Gemini"):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        # Load image if uploaded
        image = None
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
        
        # Call Gemini
        try:
            contents = [SYSTEM_PROMPT]
            if image:
                contents.append(image)
            contents.append(user_query)

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents
            )
            
            st.subheader("Answer:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
