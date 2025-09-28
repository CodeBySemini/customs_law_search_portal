# together using large language model
import streamlit as st
import pandas as pd
from table_scraper import get_exchange_rates, get_ipr_data, get_revenue_data, get_travellers_data
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

elif selected_route == "ipr":
    st.subheader("Registered Trademarks and Contact Information in Sri Lanka")
    ipr_tables = get_ipr_data()
    ipr_table_titles = [
        "Trademark Holders & Contact Details",
        "Agent Details",
        "Trademark Classes"
    ]
    for idx, df in enumerate(ipr_tables):
        title = ipr_table_titles[idx] if idx < len(ipr_table_titles) else f"Table {idx+1}"
        st.write(f"### {title}")
        st.dataframe(format_table(df), use_container_width=True)
    st.markdown("[Source Link](https://www.customs.gov.lk/wp-content/uploads/2025/03/ipr_table_data_2025.html)")

# -----------------------------
# Revenue Page
# -----------------------------
elif selected_route == "revenue":
    st.subheader("Revenue Information")
    revenue_tables = get_revenue_data()
    revenue_titles = [
        "Annual Original Revenue Estimates (Rs. Bn) for 2024 and 2025",
        "Monthly Estimated vs Actual Revenue (Rs. Mn) for 2025",
        "Cumulative Monthly Revenue (Rs. Mn) for 2025"
    ]
    for idx, df in enumerate(revenue_tables):
        title = revenue_titles[idx] if idx < len(revenue_titles) else f"Table {idx+1}"
        st.write(f"### {title}")
        formatted_df = format_table(df)
        st.dataframe(formatted_df, use_container_width=True)
    st.markdown("[Source Link](https://www.customs.gov.lk/business/revenue-collected-by-sri-lanka-customs/)")

# -----------------------------
# Travel Page
# -----------------------------
elif selected_route == "travel":
    st.subheader("Personal Travel Information")
    travel_tables = get_travellers_data()
    travel_titles = [
        "Exemption Baggage for Adults",
        "Exemption Baggage for Minors (<18 years)",
        "Passenger Baggage – Duty Free Allowances"
    ]
    for idx, df in enumerate(travel_tables):
        title = travel_titles[idx] if idx < len(travel_titles) else f"Table {idx+1}"
        st.write(f"### {title}")
        st.dataframe(format_table(df), use_container_width=True)
    st.markdown("[Source Link](https://www.customs.gov.lk/personal/travellers/)")


