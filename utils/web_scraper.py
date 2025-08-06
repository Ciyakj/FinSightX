
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_company_financial_urls(company_name):
    slug_map = {
        "infosys": "IT", "tcs": "TCS", "titan": "TI01"
    }
    slug = slug_map.get(company_name.lower(), "IT")
    base = f"https://www.moneycontrol.com/financials/{company_name.lower()}/"
    return {
        "balance_sheet": base + f"balance-sheetVI/{slug}",
        "profit_loss": base + f"profit-lossVI/{slug}"
    }

def scrape_financial_tables(urls: dict):
    results = []
    try:
        for key, url in urls.items():
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")
            tables = pd.read_html(str(soup))
            results.extend(tables)
    except Exception as e:
        results.append(f"Scrape error: {str(e)}")
    return results
