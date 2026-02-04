import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
import pandas as pd

# ---------------- SETUP ----------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("📊 Sentiment Analysis (Per-File Results)")

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = """
You are a sentiment classification engine.

Task:
Classify sentiment ONLY.

Input:
A JSON array of objects.
Each object has keys: id and text.

Output rules (STRICT):
1. Output ONE record per line.
2. Format exactly as:
   id_no:<id>|text:<text>|sentiment:<positive|negative|neutral>
3. Do NOT output explanations.
4. Do NOT output code.
5. Do NOT output HTML, tables, or colors.
6. Do NOT add extra text.

After all records:
Output ONE final line in this exact format:
counts|positive:<number>|negative:<number>|neutral:<number>
"""

# ---------------- FILE UPLOADER ----------------
uploaded_files = st.file_uploader(
    "Upload files (.txt, .json, .csv, .xlsx)",
    type=["txt", "json", "csv", "xlsx"],
    accept_multiple_files=True
)

# ---------------- CHUNK HELPER ----------------
def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

CHUNK_SIZE = 10  # safe for Groq free/on-demand tier

# ---------------- ANALYZE BUTTON ----------------
if uploaded_files and st.button("Analyze Sentiment"):

    for uploaded_file in uploaded_files:
        st.markdown("---")
        st.markdown(f"## 📁 File: `{uploaded_file.name}`")

        ext = uploaded_file.name.split(".")[-1].lower()
        records = []
        local_id = 1

        # -------- READ FILE --------
        try:
            if ext == "txt":
                raw_text = uploaded_file.read().decode("utf-8").strip()

                records = []

                # Case 1: txt contains JSON-like data (data = [...] or [...])
                if raw_text.startswith("data") or raw_text.startswith("["):
                    # Remove 'data =' if present
                    if raw_text.startswith("data"):
                        raw_text = raw_text.split("=", 1)[1].strip()


                    data = json.loads(raw_text)

                    for item in data:
                        records.append({
                            "id": local_id,
                            "text": item["text"]
                        })
                        local_id += 1

                # Case 2: plain text (one sentence per line)
                else:
                    for line in raw_text.splitlines():
                        if line.strip():
                            records.append({
                                "id": local_id,
                                "text": line.strip()
                            })
                            local_id += 1


            elif ext == "json":
                data = json.load(uploaded_file)
                for item in data:
                    records.append({"id": local_id, "text": item["text"]})
                    local_id += 1

            elif ext == "csv":
                df = pd.read_csv(uploaded_file, engine="python", on_bad_lines="skip")
                for _, row in df.iterrows():
                    records.append({"id": local_id, "text": str(row["text"])})
                    local_id += 1

            elif ext == "xlsx":
                df = pd.read_excel(uploaded_file)
                for _, row in df.iterrows():
                    records.append({"id": local_id, "text": str(row["text"])})
                    local_id += 1

            else:
                st.error("Unsupported file type")
                continue

        except Exception as e:
            st.error(f"Error reading file: {e}")
            continue

        if not records:
            st.warning("No valid text found in this file.")
            continue

        # -------- LLM ANALYSIS (CHUNKED) --------
        all_outputs = []

        with st.spinner(f"Analyzing `{uploaded_file.name}` ..."):
            for chunk in chunk_list(records, CHUNK_SIZE):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": json.dumps(chunk, indent=2)}
                    ],
                    temperature=0.5
                )
                all_outputs.append(response.choices[0].message.content)

        combined_output = "\n".join(all_outputs)

        # -------- PARSE OUTPUT --------
        rows = []

        for line in combined_output.split("\n"):
            line = line.strip()
            if not line or line.startswith("counts"):
                continue

            parts = line.split("|")
            if len(parts) < 3:
                continue

            rows.append({
                "ID": parts[0].split(":")[-1].strip(),
                "Text": parts[1].replace("text:", "").strip(),
                "Sentiment": parts[2].replace("sentiment:", "").strip()
            })

        df_result = pd.DataFrame(rows)

        # -------- DISPLAY --------
        def color_sentiment(val):
            if val == "positive":
                return "color: green; font-weight:bold"
            elif val == "negative":
                return "color: red; font-weight:bold"
            else:
                return "color: white; font-weight:bold"

        st.subheader("✅ Sentiment Result")

        if not df_result.empty:
            st.dataframe(
                df_result.style.applymap(color_sentiment, subset=["Sentiment"]),
                use_container_width=True
            )
        else:
            st.warning("No sentiment output for this file.")

        st.subheader("📊 Sentiment Counts")
        st.write(df_result["Sentiment"].value_counts())
