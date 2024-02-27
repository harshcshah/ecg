import os
import google.generativeai as genai
from PIL import Image

# Set the Google API key
GOOGLE_API_KEY = "-----------------------------"
genai.configure(api_key=GOOGLE_API_KEY)

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Function to set up input image
def input_image_setup(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            bytes_data = f.read()
        image_parts = [{"mime_type": "image/jpeg", "data": bytes_data}]  # Adjust mime type if needed
        return image_parts
    else:
        raise FileNotFoundError("Image file not found")

# Path to the ECG graph image in the Colab environment
image_path = "/content/heart-analysis-electrocardiogram-graph-ecg-vector-2046911.jpg"

# Read the image from the file path
image = Image.open(image_path)

# Input prompt for Gemini

input_prompt = """
You are a cardiologist tasked with analyzing the provided ECG graph and providing insights. Please interpret the ECG graph and provide details of any abnormalities detected, including the type of abnormality and its severity if applicable. Additionally, suggest any necessary follow-up actions or treatments based on your analysis in detail.

Please use the following format to report your findings:

1. Abnormality 1 - Description of abnormality (if applicable), severity (mild/moderate/severe)
2. Abnormality 2 - Description of abnormality (if applicable), severity (mild/moderate/severe)
   ...

"""

# Get the Gemini response
image_data = input_image_setup(image_path)
response = get_gemini_response(input_text, image_data, input_prompt)

# Display the analysis result
print("Analysis Result:")
print(response)
