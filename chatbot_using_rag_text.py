import os
import warnings
import logging
import gradio as gr
from dotenv import load_dotenv
from io import StringIO
import tempfile

# Load environment variables from .env
load_dotenv()

# Phase 2 libraries
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA

# Phase 3 libraries
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

# Disable warnings and info logs
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)

# Function to extract text content from uploaded files
def extract_text_from_files(files):
    texts = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            texts.append(file.read())
    return "\n".join(texts)

# Initialize the vectorstore (retriever)
def get_vectorstore(files):
    document_text = extract_text_from_files(files)

    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(document_text)
        temp_file_path = temp_file.name

    loaders = [TextLoader(file_path=temp_file_path)]
    index = VectorstoreIndexCreator(
        embedding=HuggingFaceEmbeddings(model_name='all-MiniLM-L12-v2'),
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    ).from_loaders(loaders)

    os.remove(temp_file_path)
    return index.vectorstore

# Function to process the user query and generate a response using RAG
def get_answer(files, prompt):
    try:
        vectorstore = get_vectorstore(files)
        if vectorstore is None:
            return "Failed to load documents from the uploaded files."

        system_prompt = ChatPromptTemplate.from_template(
            """You are very smart at everything, you always give the best,
            the most accurate and most precise answers. Answer the following Question: {user_prompt}.
            Start the answer directly. No small talk please"""
        )

        groq_chat = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )

        chain = RetrievalQA.from_chain_type(
            llm=groq_chat,
            chain_type='stuff',
            retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True
        )

        result = chain({"query": prompt})
        return result["result"]

    except Exception as e:
        return f"Error: {str(e)}"

# Gradio Interface function
def chatbot_interface(files, prompt):
    return get_answer(files, prompt)

# Create the Gradio interface
interface = gr.Interface(
    fn=chatbot_interface,
    inputs=[
        gr.Files(label="Upload your .txt files", type="filepath"),
        gr.Textbox(label="Enter your question", lines=2)
    ],
    outputs=gr.Textbox(label="Answer"),
    title="RAG-Based Chatbot",
    description="This chatbot answers questions based on the context extracted from .txt files using the Retrieval-Augmented Generation (RAG) method."
)

# Launch the interface
interface.launch()
