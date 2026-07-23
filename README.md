# Production-Grade Secure RAG PDF Chatbot Service

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tech: FastAPI](https://img.shields.io/badge/Tech-FastAPI-brightgreen.svg)](#)

A secure Retrieval-Augmented Generation (RAG) service allowing users to chat with uploaded PDF documents via Streamlit UI or FastAPI endpoints.

---

## 🚀 Features

* Encapsulates FastAPI REST backend and Streamlit interactive frontend interfaces
* Validates user session directories using strict UUID verification checks
* Saves vector database caches and session history logs persistently on disk
* Supports instant local deployment using Docker and Docker Compose
* Configured to respect API keys via environment variable `.env` configs

---

## 🛠️ Tech Stack & Libraries
* **Language:** Python 3.8+
* **Libraries:** FastAPI, Streamlit, LangChain, FAISS, OpenAI, Docker, Python

---

## 📦 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/vivekrana-031122/rag-pdf-chatbot.git
   cd rag-pdf-chatbot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Additional Setup (if applicable):**
   * If using Playwright:
     ```bash
     playwright install chromium
     ```

---

## 💻 Usage Example

Run the main scraper entry point:
```bash
docker-compose up --build
```

---

## 🛡️ Disclaimer & Robots.txt Compliance

This project is created for educational and professional demonstration purposes. By using this tool, you agree to:
* Respect the target website's `robots.txt` directives.
* Avoid making aggressive requests that could disrupt target servers (configure appropriate sleep intervals/throttling).
* Comply with local web data protection regulations and the platform's terms of service.
