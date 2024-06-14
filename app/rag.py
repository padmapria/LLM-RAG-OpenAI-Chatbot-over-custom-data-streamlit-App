import os
from dotenv import load_dotenv
import streamlit as st
import openai
from datasets import load_dataset
import pandas as pd
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Elasticsearch configuration
ELAST_SEARCH_PWD = os.getenv('ELASTIC_SEARCH_PWD')
es_connection = Elasticsearch("http://localhost:9200", basic_auth=('elastic', ELAST_SEARCH_PWD))
index_name = "wiki_qa_questions"


# Connect to Elasticsearch
def connect_to_es():
    for _ in range(10):  # Retry up to 10 times
        try:
            es = Elasticsearch("http://elasticsearch:9200", basic_auth=('elastic', ELAST_SEARCH_PWD))
            if es.ping():
                print("Connected to Elasticsearch")
                return es
        except Exception as e:
            print(f"Connection failed, retrying... ({e})")
            time.sleep(10)
    raise Exception("Failed to connect to Elasticsearch after several retries")


# Retrieve documents from Elasticsearch
def retrieve_documents(query, index_name, max_results=5):
    es = connect_to_es()
    search_query = {
        "size": max_results,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "answer", "document_title"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }
    response = es.search(index=index_name, body=search_query)
    documents = [hit['_source'] for hit in response['hits']['hits']]
    return documents

# Build context for the prompt
def build_context(documents):
    """
    Create a string of information from documents to help the AI understand the question.
    This string includes document titles, questions, and answers.
    """
    context = ""
    for doc in documents:
        doc_str = f"Title: {doc['document_title']}\nQuestion: {doc['question']}\nAnswer: {doc['answer']}\n\n"
        context += doc_str
    return context.strip()

# Augment the prompt with context
def augment_prompt(user_question, documents):
    """
    Create a message for the AI model that includes the user's question and detailed context
    from documents. This helps the AI provide a more accurate answer.
    """
    context = build_context(documents)
    return f"""
    You're an AI assistant.
    Answer the user QUESTION based on CONTEXT - the documents retrieved from our FAQ database.
    Don't use other information outside of the provided CONTEXT.

    QUESTION: {user_question}

    CONTEXT:

    {context}
    """.strip()

# Generate response from OpenAI
def generate_response(prompt, model="gpt-3.5-turbo"):
    """
    Send the prompt to OpenAI and get the model's response. This uses detailed context
    to improve the quality of the AI's answer.
    """
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
    
    
# RAG pipeline
def qa_bot(user_question, doc_index=index_name):
    context_docs = retrieve_documents(user_question, doc_index)
    prompt = augment_prompt(user_question, context_docs)
    return generate_response(prompt)

# Streamlit UI
st.set_page_config(
    page_title="GPT Chat",
    page_icon="💭",
    layout="centered"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🗣️ OpenAI GPT - ChatBot")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask GPT...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Use qa_bot to generate response
    assistant_response = qa_bot(user_prompt)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
