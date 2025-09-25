import streamlit as st
import pandas as pd

# Load preprocessed PDF text
df = pd.read_pickle("laws_text.pkl")

st.title("Sri Lanka Customs Law Search Portal")
st.write("Search for laws by keyword and find relevant PDFs.")

# Keyword search
keyword = st.text_input("Enter keyword:")

# Category filter
categories = ["All"] + sorted(df["category"].unique())
selected_category = st.selectbox("Filter by category:", categories)

# Filter by keyword and category
results = df.copy()
if keyword:
    results = results[results["text"].str.contains(keyword, case=False)]
if selected_category != "All":
    results = results[results["category"] == selected_category]

# Display results
if not results.empty:
    st.write(f"Found {len(results)} document(s):")
    for _, row in results.iterrows():
        st.markdown(f"**{row['title']}** ({row['category']})")
        st.markdown(f"[Download PDF]({row['pdf_url']})")
else:
    st.write("No documents found for this keyword/category.")
