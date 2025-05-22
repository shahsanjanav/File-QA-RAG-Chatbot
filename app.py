import streamlit as st
import tempfile
import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Setup Streamlit UI
st.set_page_config(page_title='File QA RAG Chatbot', page_icon='🤖')
st.title('Welcome to File QA RAG Chatbot 🤖')

API_KEY = st.secrets["OPENAI_API_KEY"]
os.environ['OPENAI_API_KEY'] = API_KEY

def configure_retriever(uploaded_files):
    docs = []
    temp_dir = tempfile.TemporaryDirectory()

    for uploaded_file in uploaded_files:
        temp_path = os.path.join(temp_dir.name, uploaded_file.name)
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        loader = PyPDFLoader(temp_path)
        loaded_docs = loader.load()
        if loaded_docs:
            docs.extend(loaded_docs)
        else:
            print(f"Failed to load {uploaded_file.name}")

    embeddings_model = OpenAIEmbeddings()
    print(f"Total number of documents loaded: {len(docs)}")
    return docs, embeddings_model

uploaded_files = st.sidebar.file_uploader(
    label="Upload PDF files", type=["pdf"], accept_multiple_files=True
)

if not uploaded_files:
    st.info("Please upload PDF documents to continue.")
    st.stop()

docs, embeddings_model = configure_retriever(uploaded_files)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
doc_chunks = text_splitter.split_documents(docs)

if len(doc_chunks) == 0:
    st.error("No documents were split. Ensure your files are properly loaded.")
    st.stop()

vectordb = FAISS.from_documents(doc_chunks, embeddings_model)
retriever = vectordb.as_retriever()

chatgpt = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1, streaming=True)

def generate_response(user_prompt, retriever, chatgpt, qa_prompt):
    context_docs = retriever.get_relevant_documents(user_prompt)
    context_text = "\n\n".join([d.page_content for d in context_docs])
    prompt_input = qa_prompt.format(context=context_text, question=user_prompt)
    response = chatgpt.predict(prompt_input)
    return response, context_docs

qa_template = """Use only the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know.
Keep the answer as concise as possible.

{context}

Question: {question}"""

qa_prompt = ChatPromptTemplate.from_template(qa_template)

if user_prompt := st.chat_input():
    st.chat_message("human").write(user_prompt)

    with st.chat_message("ai"):
        response, context_docs = generate_response(user_prompt, retriever, chatgpt, qa_prompt)
        st.write(response)
