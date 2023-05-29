import streamlit as st
import openai
import requests
import time
from PIL import Image
from io import BytesIO

def generate_image(prompt):
    if prompt != '':
        # image_placeholder = st.empty()
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
                )
            image_url = response['data'][0]['url']

            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            content_type = response.headers["content-type"]
            file_extension = content_type.split("/")[-1]
            file_name = f"image.{file_extension}"

            
            col1, col2 = st.columns([2, 1])
            with col1:
                image_placeholder = st.empty()
                time.sleep(0.5)
                image_placeholder.image(image_url, width=400, caption=prompt)
            with col2:
                st.download_button("Download Image",
                            data=response.content,
                            file_name=file_name,
                            mime=content_type)
        except Exception as e:
            st.error('Please Enter your Openai API key in Home page.', icon="🚨")

st.set_page_config(page_title='Generate Images', page_icon=':bulb:', layout='wide')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title('🤖 :blue[A.I] Image Generator')
title = st.text_area('',placeholder='Enter a prompt to generate an image...')
with st.spinner('Generating Image...'):
    generate_image(title)
