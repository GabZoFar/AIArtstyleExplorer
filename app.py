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

# Input for the prompt sent to the API
prompt = st.text_input("What would you like the model to tell you from this image?")

# File uploader allows the user to upload an image
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

#d ef encode_image_to_base64(image):
    # """Encode image to base64."""
    # buffered = BytesIO()
    # image.save(buffered, format="JPEG")
    # return base64.b64encode(buffered.getvalue()).decode("utf-8") 

def call_deepinfra_api(image_url, prompt, api_key):
    """Send the image URL and prompt to DeepInfra for inference."""
    url = "https://api.deepinfra.com/v1/inference/"
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
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API request failed with status code: {response.status_code} and message: {response.text}")
        return None

if image_url and API_KEY and prompt:
    if st.button('Analyze Image'):
        try:
            result = call_deepinfra_api(image_url, API_KEY, prompt)
            if result:
                # Convert the dictionary to JSON formatted string and display it
                json_result = json.dumps(result, indent=2)  # Beautify the JSON response
                st.json(json_result)  # Use st.json to render the JSON in the UI
        except Exception as e:
            st.error(f"Failed to process image due to: {str(e)}")