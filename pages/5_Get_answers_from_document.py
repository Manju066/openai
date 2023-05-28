import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import openai
import tiktoken
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity

st.set_page_config(page_title='Question Answers', page_icon=':memo:', layout='wide')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.title('🤖 :blue[A.I] Get Answers from Doc')

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191
top_n = 1000
encoding = tiktoken.get_encoding(embedding_encoding)

spinner_style = """
    <style>
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
"""

def read_file(file):
    reader = PdfReader(file)
    
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap = 200,
        length_function = len,
    )

    texts = text_splitter.split_text(raw_text)

    embeddings = {}

    try:
        for tex in texts:
            response = get_embedding(tex, engine=embedding_model)
            # Store the embedding in the dictionary
            embeddings[tex] = response
    except Exception as e:
        st.error('Please Enter your Openai API key in Home page.', icon="🚨")

    return embeddings

st.markdown(spinner_style, unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a file", type=["pdf", "text"])
if uploaded_file is not None:
    with st.spinner(''):
        docsearch = read_file(uploaded_file)
        if len(docsearch) > 0:
            query = st.text_input('',placeholder='Ask a question...')
            if query != '':
                query_embedding = get_embedding(query, engine=embedding_model)
                similarities = {}
                for text, embedding in docsearch.items():
                    similarity = cosine_similarity(embedding, query_embedding)
                    similarities[text] = similarity
                sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
                context = sorted_similarities[0][0]
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Use below context to generate an answer for the question. If you can't generate an answer out of it just say \"I don't know.\"\n\ncontext : \n{context}\n\nquestion : {query}\nanswer : ",
                    temperature=0.25,
                    max_tokens=400,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                st.write(response.choices[0]['text'])
