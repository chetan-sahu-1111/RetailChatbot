# 🛒 Retail AI Chatbot (LLM + SQL + Dashboard)

An AI-powered retail chatbot that converts natural language into SQL queries, executes them on a MySQL database, and displays results in a user-friendly interface.

---

## 🚀 Live Architecture

- **Frontend** → Streamlit Cloud  
- **Backend** → FastAPI deployed on Render  
- **Database** → MySQL hosted on Railway  
- **LLM** → Groq API (LLama models)

---

## 🧠 Project Overview

This system allows a shop owner to:

- Ask questions in natural language  
- Automatically convert queries into SQL  
- Execute SQL on a real database  
- View results in structured format  
- Get insights from their data  

---

## 🏗️ System Architecture

User (Streamlit UI)
      -->
FastAPI Backend (Render)
      -->
LLM (Groq API)
      -->
SQL Generation & Validation
      -->
MySQL Database (Railway)
      -->
Results returned to UI

---

## ✨ Features

- 🧠 Natural Language → SQL conversion
- 🔒 SQL safety validation
- 🔁 Self-healing query system (auto-fix SQL)
- 📊 Tabular result display
- 🧾 SQL query visibility
- ⚡ Fast inference using Groq API
- ☁️ Fully cloud-deployed system

---

## 🧰 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PyMySQL
- Groq API

### Frontend
- Streamlit

### Database
- MySQL (Railway)

### Deployment
- Render (Backend)
- Railway (Database)
- Streamlit Cloud (Frontend)

---

## 📁 Project Structure

RetailChatbot/
│
├── app/
│ ├── api/ # API routes
│ ├── core/ # Config & logger
│ ├── db/ # DB connection & execution
│ ├── models/ # Request models
│ ├── services/ # SQL generation, validation, LLM logic
│ ├── utils/ # Helper functions
│ └── main.py # FastAPI entry point
│
├── requirements.txt
├── .env.example
├── README.md

