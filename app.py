import streamlit as st
from PIL import Image
import base64
import requests
from io import BytesIO

# Setting up the title of the application
st.title('Image Inference with DeepInfra')

# Input for the API key
API_KEY = st.text_input("Enter your DeepInfra API Key:", type="password")

# File uploader allows the user to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

def encode_image_to_base64(image):
    """Encode image to base64."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def call_deepinfra_api(base64_image, api_key):
    """Send the base64 encoded image to DeepInfra for inference."""
    url = "https://api.deepinfra.com/v1/inference/llava-hf/llava-1.5-7b-hf"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "llava-hf/llava-1.5-7b-hf",
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "image_base64",
                    "image_base64": base64_image
                }
            },
            {
                "role": "system",
                "content": {
                    "type": "text",
                    "text": "Analyze this image."
                }
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed with status code: " + str(response.status_code))

if uploaded_file is not None and API_KEY:
    if st.button('Analyze Image'):
        try:
            img = Image.open(uploaded_file)
            img = img.convert("RGB")  # Convert image to RGB
            encoded_image = encode_image_to_base64(img)  # Encode the image to base64
            result = call_deepinfra_api(encoded_image, API_KEY)  # Send the encoded image for inference
            inference_result = result.get('choices', [{}])[0].get('message', {}).get('content', 'No inference result available')
            st.write(f"Inference Result: {inference_result}")  # Display the inference result as plain text
        except Exception as e:
            st.error(f"Failed to process image due to: {str(e)}")

# Add footer or additional UI elements below if necessary
