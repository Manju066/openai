import streamlit as st
import openai

st.set_page_config(page_title='OpenAI apps', page_icon=':house:', layout='wide')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title('🤖 :blue[Wel Come] ')
api_key_input = st.text_input(
                "Enter your OpenAI API Key",
                type="password",
                placeholder="Paste your OpenAI API key here (sk-...)",
                help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            )
            
if api_key_input:
    openai.api_key = api_key_input