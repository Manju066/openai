import streamlit as st
from PIL import Image
from io import BytesIO
import openai


st.set_page_config(page_title='Image Variations', page_icon=':recycle:', layout='wide')
st.title('🤖 :blue[A.I] Generate Variations of Image')
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])
    with col1:
        image = Image.open(uploaded_file)
        st.image(image, width=256, caption="Uploaded Image")
    with col2:
        with st.spinner(''):
            image = Image.open(uploaded_file)
            width, height = 512, 512
            image = image.resize((width, height))
            # Convert the image to a BytesIO object
            byte_stream = BytesIO()
            image.save(byte_stream, format='PNG')
            byte_array = byte_stream.getvalue()
            try:
                response = openai.Image.create_variation(
                    image=byte_array,
                    n=1,
                    size="1024x1024"
                )
                image_url = response['data'][0]['url']
                st.image(image_url, width=300, caption="Variation Image")
            except Exception as e:
                st.error('Please Enter your Openai API key in Home page.', icon="🚨")