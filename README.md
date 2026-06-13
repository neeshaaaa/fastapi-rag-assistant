# Palm Mind RAG Backend

Hey there! This is a custom Retrieval-Augmented Generation (RAG) backend built from scratch using FastAPI. I built this to handle document ingestion and power a conversational AI assistant that can actually book interviews for you. 

The goal here was to avoid bloated wrapper libraries like LangChain's `RetrievalQAChain` and keep the architecture clean, modular, and easy to maintain. 

## Features

* **Document Ingestion API**: Upload `.pdf` or `.txt` files. The system extracts the text and applies your choice of two specific chunking strategies:
  * **Fixed Chunking**: Splits text into strict, uniform sizes for consistent retrieval.
  * **Recursive Chunking**: Smartly splits text by paragraphs and sentences to preserve the natural context.
  It then generates embeddings and securely stores them.
* **Custom Conversational RAG API**: A clean, custom RAG pipeline that handles multi-turn queries. It pulls chat history and vector context to generate accurate responses.
* **Interview Booking System**: The Gemini LLM is hooked up with function calling. If you chat with it and ask to book an interview, it will automatically collect your name, email, date, and time, and save the booking directly to the database.
* **Resilient Memory**: Uses Redis for chat session memory, with built-in fallbacks so the app won't crash if the Redis server goes offline.

## Core Architecture Constraints Met

To ensure this backend represents industry-standard best practices, the following constraints were strictly adhered to:
* **No Bloated Wrappers**: Completely custom RAG implementation without relying on `RetrievalQAChain`.
* **Alternative Vector Database**: Avoided standard defaults like FAISS or Chroma in favor of a robust Qdrant integration.
* **Clean & Modular**: Separated concerns into dedicated `routers`, `services`, `schemas`, and `models` directories.
* **Strict Typing**: Implemented Pydantic V2 schemas and comprehensive Python type hints for maintainability.

## Tech Stack

* **Framework**: FastAPI (Python)
* **LLM / AI**: Google Gemini API (`google-genai`)
* **Vector Database**: Qdrant (Local file storage)
* **Relational Database**: SQLite (via SQLAlchemy) for metadata and booking storage
* **Memory**: Redis

## Getting Started

1. **Clone the repo** and set up your virtual environment.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables**: Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
4. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

Once the server is running, head over to `http://127.0.0.1:8000/docs` to see the Swagger UI.

* **POST `/ingest/upload`**: Upload your documents here to populate the Qdrant vector database.
* **POST `/chat/query`**: The main chat endpoint. Pass a `session_id` and your `question`. Ask it about the uploaded documents or tell it to book an interview!

## Project Structure

* `app/api/`: FastAPI route handlers (ingestion and chat).
* `app/db/`: SQLAlchemy models and SQLite database config.
* `app/schemas/`: Pydantic models for strict data validation.
* `app/services/`: The core logic (LLM integrations, Redis memory, chunking, and PDF parsing).
* `app/vectorstore/`: Qdrant client initialization and storage logic.

---
*Built with ❤️ focusing on clean code and industry standards.*
