import pandas as pd
from urllib.parse import urljoin
from scrapling import StealthyFetcher

BASE_URL = "https://qatarsale.com"


def get_showroom_links():
    print("Fetching showroom list...")

    page = StealthyFetcher.fetch(
        "https://qatarsale.com/ar/showroom-list/cars_for_sale",
        headless=True,
        network_idle=True,
        timeout=60000,
        wait_for_idle_network_timeout=10000
    )
    
    all_links = []

    def extract_links(page):
        links = []
        for i in page.css("[data-testid='at-showroom-item-link-title'] a"):
            href = i.attrib.get("href", "")
            if href:
                links.append(urljoin(BASE_URL, href))
        return links
    
    all_links.extend(extract_links(page))

    all_links = list(dict.fromkeys(all_links))
    print(f"Found {len(all_links)} showrooms")
    return all_links
