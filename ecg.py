from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Set the Google API key
GOOGLE_API_KEY = "AIzaSyDtmbph6NJPYz5u3yHwiZBnQCitWiW7jQU"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to set up input image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="ECG Analysis App")
st.header("Jio Health")

# User inputs
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an ECG graph image...", type=["jpg", "jpeg", "png"])

# Additional input field for doctor's questions
doctor_question = st.text_input("Doctor's Question:")

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded ECG Graph Image.", use_column_width=True)

# Button to trigger action
submit_button = st.button("Analyze ECG Graph")

# Input prompt for Gemini
input_prompt = """
You are an expert cardiologist tasked with analyzing the provided ECG graph and providing insights. Please interpret the ECG graph and provide details of any abnormalities detected, including the type of abnormality and its severity if applicable. Additionally, suggest any necessary follow-up actions or treatments based on your analysis in detail. Note: if you see any other image then say it is {name} of image.

Please use the following format to report your findings:

1. Abnormality 1 - Description of abnormality (if applicable), severity (mild/moderate/severe)
2. Abnormality 2 - Description of abnormality (if applicable), severity (mild/moderate/severe)
   ...

"""

# If submit button is clicked
if submit_button:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_text, image_data, input_prompt)
    st.subheader("Analysis Result:")
    st.write(response)

# Processing doctor's question
if doctor_question:
    st.subheader("Doctor's Question:")
    st.write(doctor_question)
    # Process the doctor's question here and provide a response using the Gemini Pro Vision API
    # You can call the function get_gemini_response with appropriate parameters
    st.write("Placeholder response to doctor's question.")
