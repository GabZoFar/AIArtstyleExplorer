import streamlit as st
from PIL import Image
import base64
import requests
import json

# Setting up the title of the application
st.title('Art Style Explorer')

# Input for the API key
API_KEY = st.text_input("Key:", type="password")

# Input for the image URL
image_url = st.text_input("Enter the URL of the image:")

# Input for the prompt sent to the API with automatic resizing
prompt = st.text_area("What would you like the model to tell you from this image?", height=400, max_chars=4000, key="textarea")
st.markdown(
    """
    <style>
    #textarea {
        resize: vertical;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Model selection
model_choice = st.radio("Choose the model:", ("Llava", "Stability-AI"))

def call_deepinfra_api(image_url, prompt, api_key, model_choice):
    """Send the image URL and prompt to DeepInfra for inference."""
    if model_choice == "Llava":
        url = "https://api.deepinfra.com/v1/openai/chat/completions"
        model = "llava-hf/llava-1.5-7b-hf"
    else:
        url = "https://api.deepinfra.com/v1/inference/stability-ai/sdxl"
        model = "stability-ai/sdxl"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
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
        return response.json() if model_choice == "Llava" else response.content
    else:
        st.error(f"API request failed with status code: {response.status_code} and message: {response.text}")
        return None

if image_url and API_KEY and prompt:
    if st.button('Analyze Image'):
        try:
            result = call_deepinfra_api(image_url, prompt, API_KEY, model_choice)
            if result:
                if model_choice == "Llava":
                    # Convert the dictionary to JSON formatted string and display it
                    json_result = json.dumps(result, indent=2)  # Beautify the JSON response
                    st.json(json_result)  # Use st.json to render the JSON in the UI
                else:
                    # Display the returned image
                    st.image(result, caption='Generated Image', use_column_width=True)
        except Exception as e:
            st.error(f"Failed to process image due to: {str(e)}")