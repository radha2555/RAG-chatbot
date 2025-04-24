
###*RAG Chatbot with LangChain + Groq + Gradio*

```
# 🤖 Smart RAG Chatbot – Powered by Groq + LangChain

Ever wish you could drop a bunch of `.txt` files into a box and instantly ask questions about them? Well, you're in luck.

This chatbot uses **RAG (Retrieval-Augmented Generation)** to read your files, understand the content, and answer your questions with scary accuracy. It’s built using:

- 🚀 Groq’s lightning-fast LLaMA3-8B model
- 🧱 LangChain for chaining logic
- 🔍 HuggingFace embeddings for document search
- 💬 Gradio for the easy-to-use UI

---

## 🔧 What You Can Do With It

- Upload one or more `.txt` files
- Ask any question based on the content inside
- Get direct, no-nonsense answers thanks to Groq’s LLaMA3 + vector search magic

---

## ⚙️ How to Run This Locally

### Step 1: Clone It

```bash
git clone https://github.com/yourusername/rag-chatbot-groq.git
cd rag-chatbot-groq
```

### Step 2: Install the Requirements

```bash
pip install -r requirements.txt
```

### Step 3: Set Your API Key

Create a `.env` file in the same directory as `app.py` and add your Groq API key like this:

```env
GROQ_API_KEY=gsk_your_key_here
```

👉 Don’t have a key? [Get one from Groq here](https://console.groq.com/keys)

### Step 4: Fire It Up

```bash
python app.py
```

The Gradio interface will open in your browser. Upload some `.txt` files and start asking questions!

---

## 🧠 How It Works (In a Nutshell)

1. You upload `.txt` files.
2. The app breaks the text into chunks and stores them in a vector database.
3. Your question is converted to an embedding, and the top 3 most relevant chunks are pulled.
4. These are sent to Groq’s LLaMA3 model along with your question.
5. You get a nice, concise answer.

---

## 📁 What's Inside

```
📦 rag-chatbot-groq/
├── app.py              # Main application logic
├── .env                # API key goes here (keep it secret!)
├── requirements.txt    # Dependencies
└── README.md           # This file
```

---

## 🛑 Heads-Up!

- This only works with `.txt` files for now. PDFs and others coming soon.
- Don’t commit your `.env` file. Seriously.
- Groq is FAST. Like scary fast.

---
