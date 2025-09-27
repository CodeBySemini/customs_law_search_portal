import pandas as pd
from bs4 import BeautifulSoup
import requests

def fetch_cbsl_exchange_rates(start_date, end_date, currencies=None):

    if currencies is None:
        currencies = [
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
    
    url = "https://www.cbsl.gov.lk/cbsl_custom/exratestt/exrates_resultstt.php"
    payload = {
        "lookupPage": "lookup_daily_exchange_rates.php",
        "startRange": "2006-11-11",
        "rangeType": "dates",
        "txtStart": start_date,
        "txtEnd": end_date,
        "chk_cur[]": currencies,
        "submit_button": "Submit"
    }
    
    response = requests.post(url, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    currency_headers = soup.find_all("h2")
    currency_headers = currency_headers[1:] 
    tables = soup.find_all("table")

    if not tables or not currency_headers:
        raise ValueError("No tables found. Check date range or payload.")

    exchange_data = {}
    for header, table in zip(currency_headers, tables):
        currency_name = header.text.strip()
        df = pd.read_html(str(table))[0]
        exchange_data[currency_name] = df

    return exchange_data

def fetch_tables(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    tables = soup.find_all("table")
    dfs = []
    for table in tables:
        html_table = str(table)
        dataframes = pd.read_html(html_table)
        df = dataframes[0]
        dfs.append(df)
    return dfs

def get_ipr_data():
    url = "https://www.customs.gov.lk/wp-content/uploads/2025/03/ipr_table_data_2025.html"
    return fetch_tables(url)

def get_revenue_data():
    url = "https://www.customs.gov.lk/business/revenue-collected-by-sri-lanka-customs/"
    return fetch_tables(url)

def get_travellers_data():
    url = "https://www.customs.gov.lk/personal/travellers/"
    return fetch_tables(url)

def get_exchange_rates(start_date="2025-06-25", end_date="2025-09-25", currencies=None):
    return fetch_cbsl_exchange_rates(start_date, end_date, currencies)
