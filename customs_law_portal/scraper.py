# 24ada027 Semini
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.customs.gov.lk"
URL = f"{BASE_URL}/about-us/customs-law/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

laws = []
seen_urls = set()  # track duplicates

sections = soup.find_all("div", class_="elementor-widget-wrap")

for section in sections:
    # Title from <h2>
    h2_tag = section.find("h2", class_="elementor-heading-title")
    if not h2_tag:
        continue
    title = h2_tag.get_text(strip=True)
    
    # Category + PDF link
    ul = section.find("ul", class_="elementor-icon-list-items")
    if not ul:
        continue
    
    lis = ul.find_all("li", class_="elementor-icon-list-item")
    if len(lis) < 2:
        continue
    
    category = lis[0].find("span", class_="elementor-icon-list-text").get_text(strip=True)
    a_tag = lis[1].find("a")
    if a_tag and a_tag.get("href", "").endswith(".pdf"):
        pdf_url = BASE_URL + a_tag.get("href")
        # Skip duplicates
        if pdf_url not in seen_urls:
            seen_urls.add(pdf_url)
            laws.append({
                "title": title,
                "category": category,
                "pdf_url": pdf_url
            })

# Save CSV
df = pd.DataFrame(laws)
df.to_csv("laws.csv", index=False)
print("Scraping complete! laws.csv created without duplicates.")

