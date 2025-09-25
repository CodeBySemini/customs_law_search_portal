import streamlit as st
import pandas as pd
from table_scraper import get_exchange_rates
from util import format_table
from datetime import datetime, timedelta



PAGES = {
    "LAWS": "laws",
    "IPR": "ipr",
    "Revenue": "revenue",
    "Travel": "travel",
    "Exchange Rates": "exchange"
}

st.set_page_config(
    page_title="Sri Lanka Customs Data Viewer",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Sri Lanka Customs Data Viewer")
selected_route = st.sidebar.radio("Select a Page", list(PAGES.values()))

today = datetime.today()
yesterday = today - timedelta(days=1)

if selected_route == "laws":
# Load preprocessed PDF text
    df = pd.read_pickle("laws_text.pkl")
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

elif selected_route == "exchange":
    st.subheader("CBSL Daily Exchange Rates")
    
    # Sidebar filters
    start_date = st.sidebar.date_input("Start Date", yesterday)
    end_date = st.sidebar.date_input("End Date", today)
    all_currencies = [
        "AUD~Australian Dollar",
        "CAD~Canadian Dollar",
        "CHF~Swiss Franc",
        "CNY~Renminbi",
        "EUR~Euro",
        "GBP~British Pound",
        "JPY~Yen",
        "SGD~Singapore Dollar",
        "USD~United States Dollar"
    ]
    selected_currencies = st.sidebar.multiselect(
        "Select Currencies",
        options=all_currencies,
        default=all_currencies
    )
    
    if st.sidebar.button("Fetch Exchange Rates"):
        with st.spinner("Fetching data..."):
            try:
               
                exchange_data = get_exchange_rates(
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    currencies=selected_currencies
                )
                
              
                tabs = st.tabs(list(exchange_data.keys()))
                
                for tab, (currency_name, df) in zip(tabs, exchange_data.items()):
                    with tab:
                        st.write(f"### {currency_name}")
                        st.dataframe(df, use_container_width=True)

                       
                        plot_df = df.copy()
                        plot_df = plot_df.rename(columns=lambda x: x.strip())
                        if "Date" in plot_df.columns:
                            plot_df["Date"] = pd.to_datetime(plot_df["Date"].str.strip())
                            plot_df.set_index("Date", inplace=True)

                       
                            for col in plot_df.columns:
                                plot_df[col] = plot_df[col].astype(str).str.replace(",", "").astype(float)

                    
                            st.line_chart(plot_df)
                
                st.markdown("[Source Link](https://www.cbsl.gov.lk/cbsl_custom/exratestt/exrates_resultstt.php)")
            except Exception as e:
                st.error(f"Error fetching exchange rates: {e}")

