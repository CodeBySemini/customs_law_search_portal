A simple Python-based project that scrapes Sri Lanka Customs Law PDFs, extracts text from them, and builds a searchable interface where users can find which document(s) to refer to by typing a keyword.

✅ Web Scraping – Scrapes the Sri Lanka Customs Law page
 for:
Law title
Category (e.g., Management, Port Dues, Levying of Customs Duties)
PDF URL

✅ PDF Download & Text Extraction – Automatically downloads all 18 PDFs and extracts text using PyPDF2.

✅ Searchable Web App –
Users can search for a keyword (e.g., “duties”, “re-imported”)
Filter results by category
See which document(s) contain the keyword
Click to download the PDF

✅ Ethical Scraping – Only collects public information, does not overload the server, and credits the source.

Folder Structure
customs_law_portal/
│
├── scraper.py          # Scrapes title, category, and PDF URLs from website
├── extract_text.py     # Downloads PDFs & extracts text into a pickle file
├── app.py              # Streamlit app for keyword-based search
├── laws.csv            # Stores scraped metadata
├── laws_text.pkl       # Stores extracted text for fast searching
├── pdfs/               # Folder where PDFs are stored
├── requirements.txt    # List of required dependencies
└── README.md           # This file

Setup Instructions
1 - Clone or Create Project (Create a folder and open it in VS Code.)
2 - Create Virtual Environment (python -m venv .venv) and Activate it.
3 - Install Dependencies (pip install -r requirements.txt)

How to Run

Step 1: Scrape the Website
Run the scraper to collect all laws:
python scraper.py (in terminal)
This will create laws.csv with law titles, categories, and PDF URLs.

Step 2: Download PDFs & Extract Text
Run the text extractor:
python extract_text.py (in  terminal)
This will:
Download all PDFs into the pdfs/ folder
Extract text and save it to laws_text.pkl

Step 3: Run the Web App
Run the Streamlit search portal:
streamlit run app.py (in terminal)
Open the URL shown in the terminal (usually http://localhost:8501) in your browser.
