# Sentiment Analysis Dashboard

This project is a **Streamlit-based Sentiment Analysis application** that classifies text sentiment  
(**Positive / Negative / Neutral**) using the **Groq LLM API**.

The application supports multiple file formats and processes each file independently to provide clear and structured sentiment insights.

---

## Features

- Upload and analyze **multiple files**
- Supported file formats:
  - `.txt`
  - `.json`
  - `.csv`
  - `.xlsx`
- Intelligent handling of:
  - Plain text files
  - JSON-like content inside `.txt` files
- **Per-file sentiment analysis**
- Batch (chunked) processing to handle API token limits
- Color-coded sentiment results
- Sentiment count summary for each file

---

## How It Works

1. Users upload one or more files
2. Each file is processed independently
3. Text data is converted into structured `{id, text}` records
4. Data is sent to the Groq LLM in manageable chunks
5. Sentiment is classified as:
   - `positive`
   - `negative`
   - `neutral`
6. Results are displayed in a table along with sentiment counts

---

## Project Structure
.

├── streamlit_sentiment.py

├── requirements.txt

├── README.md

└── .env (not pushed to GitHub)


---

## Environment Setup

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here



