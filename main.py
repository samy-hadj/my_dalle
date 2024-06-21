import streamlit as st
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import requests
from io import BytesIO

def main():
    load_dotenv()
    client = OpenAI()

    st.set_page_config(page_title="DALL-E 3 Image Generator", layout="wide", initial_sidebar_state="expanded")

    # Sidebar Configuration
    st.sidebar.title("Configuration")
    theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])
    image_size = st.sidebar.selectbox("Image Size", ["256x256", "512x512", "1024x1024"])
    quality = st.sidebar.selectbox("Quality", ["Standard", "hd"])

    # Apply Theme
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .reportview-container {
                background: #333;
                color: white;
            }
            .sidebar .sidebar-content {
                background: #444;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    st.title("🤖🎨 DALL-E 3 Image Generator")
    st.markdown("---")

    user_input = st.text_input("Enter text:", "DALL-E Prompt")
    st.markdown("---")

    if st.button("Generate Image"):
        with st.spinner("Generating your image. This may take a few seconds..."):
            response = client.images.generate(
                model="dall-e-3",
                prompt=user_input,
                size=image_size,
                quality=quality.lower(),
                n=1,
            )
            image_url = response.data[0].url

        if image_url:
            st.image(image_url, caption="Generated Image", use_column_width=True)
            st.markdown("---")
            st.markdown(get_image_download_link(image_url), unsafe_allow_html=True)

            # Preview and Download
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))

            st.sidebar.image(img, caption="Preview", use_column_width=True)
            if st.sidebar.button("Download Image"):
                download_image(image_url)

            # Recent Images Gallery
            if 'generated_images' not in st.session_state:
                st.session_state.generated_images = []
            st.session_state.generated_images.append(image_url)

            st.subheader("Gallery of Recently Generated Images")
            cols = st.columns(4)
            for idx, img_url in enumerate(st.session_state.generated_images[-8:]):
                with cols[idx % 4]:
                    st.image(img_url, use_column_width=True)

def get_image_download_link(image_url):
    return f'<a href="{image_url}" download="generated_image.png">Click here to download the image</a>'

def download_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save("generated_image.png")
    st.success("Image downloaded successfully!")

if __name__ == "__main__":
    main()
