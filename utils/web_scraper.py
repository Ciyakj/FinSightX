# utils/web_scraper.py

import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_moneycontrol_financials(company_name_or_url):
    try:
        if company_name_or_url.startswith("http"):
            url = company_name_or_url
        else:
            slug = company_name_or_url.lower().replace(" ", "")
            url = f"https://www.moneycontrol.com/financials/{slug}/balance-sheetVI/{slug}"

        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        tables = pd.read_html(str(soup))

        if not tables:
            return "No readable tables found."

        return tables
    except Exception as e:
        return f"Web scrape error: {str(e)}"
