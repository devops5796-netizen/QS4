import sys
import time
import links_scraper
import products_scraper
import flatten
import excel_writer
from detect_utils import get_last_page
from dotenv import load_dotenv
load_dotenv()

CATEGORIES = {
    "cars_for_rent":
        "https://qatarsale.com/ar/products/cars_for_rent?basic_search:StatusFilter=0",
    "special_numbers-plate_numbers":
        "https://qatarsale.com/ar/products/special_numbers-plate_numbers?basic_search:StatusFilter=0",
    "bikes":
        "https://qatarsale.com/ar/products/bikes?basic_search:StatusFilter=0",
    "caravan":
        "https://qatarsale.com/ar/products/caravan?basic_search:StatusFilter=0",
}


def run_single_category(category: str, start: int, end: int):
    listing_url   = CATEGORIES[category]
    links_csv     = f"links_{category}_{start}_{end}.csv"
    products_json = f"products_{category}_{start}_{end}.jsonl"
    output_excel  = f"{category}_{start}_{end}.xlsx"

    elapsed_start = time.time()
    print(f"QatarSale Scraper - Single Category")
    print(f"Category: {category} | Pages: {start} to {end}")

    s1 = links_scraper.run(listing_url, start, end, links_csv)
    if s1['total_links'] == 0:
        print(f"⚠️ No links found — skipping.")
        return None

    s2 = products_scraper.run(links_csv, products_json, workers=4)
    s3 = flatten.run(products_json)

    df = s3["df"]
    excel_writer.write_single(df, category[:31], output_excel)

    elapsed = time.time() - elapsed_start
    print(f"\nDONE: {s1['total_links']} links | {s2['success']} scraped | {int(elapsed//60)}m {int(elapsed%60)}s")
    return output_excel


def main():
    if len(sys.argv) == 4:
        category = sys.argv[1]
        start    = int(sys.argv[2])
        end      = int(sys.argv[3])
        if category in CATEGORIES:
            run_single_category(category, start, end)
        else:
            print(f"Unknown category: {category}")
            sys.exit(1)
    else:
        print("Usage: python main.py <category> <start_page> <end_page>")
        sys.exit(1)


if __name__ == "__main__":
    main()