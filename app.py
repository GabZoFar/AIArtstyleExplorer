import streamlit as st
from PIL import Image
import base64
import requests
# from io import BytesIO

# Setting up the title of the application
st.title('Art Style Explorer')

# Input for the API key
API_KEY = st.text_input("Enter your DeepInfra API Key:", type="password")

# Input for the image URL
image_url = st.text_input("Enter the URL of the image:")

# File uploader allows the user to upload an image
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

#d ef encode_image_to_base64(image):
    # """Encode image to base64."""
    # buffered = BytesIO()
    # image.save(buffered, format="JPEG")
    # return base64.b64encode(buffered.getvalue()).decode("utf-8") 

def call_deepinfra_api(base64_image, api_key):
    """Send the base64 encoded image to DeepInfra for inference."""
    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
     }
    data = {
        "model": "llava-hf/llava-1.5-7b-hf",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": "use json format to describe the image. 1. colours, 2. art types, 3. objects in the image, 4. artistic style, 5. image_url"
                    }
                ]
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("API request failed with status code: " + str(response.status_code))

if image_url and API_KEY:
    if st.button('Analyze Image'):
        try:
            result = call_deepinfra_api(image_url, API_KEY)
            if result:
                inference_result = result.get('choices', [{}])[0].get('message', {}).get('content', 'No inference result available')
                st.write(f"Inference Result: {inference_result}")
        except Exception as e:
            st.error(f"Failed to process image due to: {str(e)}")

# Add footer or additional UI elements below if necessary
