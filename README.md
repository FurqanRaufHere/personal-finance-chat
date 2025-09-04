# Personal Finance Chatbot

A **persona-driven AI chatbot** that helps users learn personal finance in multiple ways. Built with **Streamlit** and **Groq API**, the app allows users to interact with three distinct personas: Professional, Creative, and Technical.

---

## Project Overview

This project aims to make **personal finance education more approachable**. Users can chat with different AI personas:

- **Professional Assistant:** Provides clear, actionable tips on budgeting, saving, and beginner investing.  
- **Creative Companion:** Uses stories, metaphors, and analogies to explain finance concepts in a fun, memorable way.  
- **Technical Expert:** Breaks down finance questions with formulas, calculations, and detailed steps.

The chat history is maintained for context, and users can export conversations in **TXT** format for reference.

---

## 🛠 Features

- Persona selector (Professional, Creative, Technical)  
- Clean Streamlit UI with sidebar navigation  
- Chat history with user/assistant bubbles  
- Input box + send button (Enter to send)  
- Optional streaming response  
- Export conversation as JSON or TXT  

---

## Setup Instructions

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/personal-finance-chat.git
cd personal-finance-chat
```

2. **Create a virtual environment:**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**
   - **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```
   - **Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Set up your Groq API key:**
   - Create a `.env` file in the project root
   - Add your API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
   - Replace `your_api_key_here` with your actual Groq API key

6. **Run the Streamlit app:**
```bash
streamlit run src/web_app.py
```

