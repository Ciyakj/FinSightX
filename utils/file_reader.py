# utils/file_reader.py

import pandas as pd
import fitz  # PyMuPDF
import os

def read_financial_files(uploaded_files):
    try:
        all_texts = []

        for file in uploaded_files:
            filename = file.name.lower()
            if filename.endswith(".csv"):
                df = pd.read_csv(file)
                all_texts.append(df.to_string(index=False))

            elif filename.endswith(".pdf"):
                doc = fitz.open(stream=file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                all_texts.append(text)

            else:
                all_texts.append(file.read().decode("utf-8"))

        return "\n\n".join(all_texts)

    except Exception as e:
        return f"[Error reading financial files]: {str(e)}"
