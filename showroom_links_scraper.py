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

    items = page.css("[data-testid='at-showroom-item-link-title'] a")

    links = []
    for i in items:
        href = i.attrib.get("href", "")
        if href:
            links.append(urljoin(BASE_URL, href))
            
    links = list(dict.fromkeys(links))
    print(f"Found {len(links)} of showroom")

    return links