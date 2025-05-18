# 🤖 File QA RAG Chatbot App
A multi-modal visual QnA app using Google Gemini Pro and Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

A Streamlit-based Retrieval-Augmented Generation (RAG) chatbot that allows users to upload PDF files and ask context-aware questions using OpenAI GPT-3.5 and LangChain.

## 🔗 Live App
👉 [Launch App](https://your-app-name.streamlit.app)

## 🧠 Features
- Upload multiple PDF files
- Extracts content and embeds using OpenAI Embeddings
- Retrieves relevant context using FAISS
- Streams GPT-3.5 answers based on your questions

## 🚀 Tech Stack
- Streamlit UI
- LangChain (Embeddings, Retriever, Prompting)
- OpenAI GPT-3.5 Turbo API
- FAISS (vector similarity search)

## 📦 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 API Key
Add your OpenAI API key in the sidebar input field or securely via Streamlit Secrets:

Streamlit Cloud → Settings → Secrets:
```
OPENAI_API_KEY = "your-openai-api-key"
```

## 📄 License
MIT License © 2025 Sanjana Shah

## 👤 Author
shahsanjanav
*ML/AI Enthusiast*

---
