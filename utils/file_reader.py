
import pandas as pd
import fitz  # PyMuPDF

def parse_uploaded_files(files):
    content = []
    for file in files:
        if file.name.endswith(".pdf"):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
            content.append(text)
        elif file.name.endswith(".csv"):
            df = pd.read_csv(file)
            content.append(df.to_string(index=False))
    return "\n\n".join(content)
