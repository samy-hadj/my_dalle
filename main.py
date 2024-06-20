import streamlit as st
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

def main():

    load_dotenv()

    client = OpenAI()

    st.title("🤖🎨 DALL-E 3 Image Generator")

    # Text Input
    user_input = st.text_input(label="Enter text:", placeholder="DALL-E Prompt")

    # Button
    if st.button("Submit"):
        with st.spinner("Generating your image. It may take couple seconds..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=user_input,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

        if image_url is not None:
            st.image(image_url, caption="Image from URL", use_column_width=True)

            download_button = st.download_button(
                data=image_url,
                label="Download Image",
                key="download_button",
                on_click=download_image,
            )

def download_image():
    # This function can be customized to download the image from the URL
    # and save it to the user's machine.
    # In this example, it just prints a message.
    st.success(f"Downloading generated image...")

if __name__ == "__main__":
    main()