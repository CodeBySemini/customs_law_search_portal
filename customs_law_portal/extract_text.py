#24ada019 Adithya
import pandas as pd
import requests
import os
from PyPDF2 import PdfReader

PDF_FOLDER = "pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

df = pd.read_csv("laws.csv")
law_texts = []

for index, row in df.iterrows():
    pdf_url = row['pdf_url']
    title = row['title'].replace("/", "_")  # avoid invalid filename chars
    filename = f"{PDF_FOLDER}/{title}.pdf"
    
    # Download PDF if not exists
    if not os.path.exists(filename):
        r = requests.get(pdf_url)
        with open(filename, "wb") as f:
            f.write(r.content)
    
    # Extract text with PyPDF2
    text = ""
    with open(filename, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    law_texts.append({
        "title": row['title'],
        "category": row['category'],
        "pdf_url": pdf_url,
        "text": text
    })

df_text = pd.DataFrame(law_texts)
df_text.to_pickle("laws_text.pkl")
print("PDF text extraction complete! Data saved for search.")

