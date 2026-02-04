Sentiment Analysis Dashboard (GUVI Project)

This project was developed during the **GUVI training program**.  
It is a **Streamlit-based Sentiment Analysis application** that classifies text sentiment
(Positive / Negative / Neutral) using the **Groq LLM API**.



 Features

- Upload and analyze **multiple files**
- Supports file formats:
  - `.txt`
  - `.json`
  - `.csv`
  - `.xlsx`
- Handles:
  - Plain text files
  - JSON-like text inside `.txt`
- Per-file sentiment analysis
- Batch (chunked) processing to avoid API token limits
- Color-coded sentiment output
- Sentiment count summary for each file

---

How It Works

1. User uploads one or more files
2. Each file is processed independently
3. Text is converted into structured `{id, text}` records
4. Data is sent to Groq LLM in chunks
5. Sentiment is classified as:
   - `positive`
   - `negative`
   - `neutral`
6. Results are displayed in a table with sentiment counts

---

 Project Structure
├── streamlit_sentiment.py
├── requirements.txt
├── README.md
└── .env (not pushed to GitHub)

---

Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here


