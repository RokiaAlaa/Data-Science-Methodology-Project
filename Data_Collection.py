import requests
from bs4 import BeautifulSoup
import csv
import time

print("1.Data Collection")

# ------------ SETTINGS ------------
BASE_URL = "https://www.jumia.com.eg/catalog/?q=mobile&page={}"
PAGES = 30   # 30 pages × avg 45 products ≈ 1350 products
OUTPUT_FILE = "jumia_1500_raw_fast.csv"
# ----------------------------------

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

products = []

print("Starting FAST scraping...")

for page in range(1, PAGES + 1):
    print(f"Scraping page {page}...")
    url = BASE_URL.format(page)

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except:
        print(f"⚠ Error loading page {page}, skipping...")
        continue

    if response.status_code != 200:
        print("Failed to load page", page)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("article", {"class": "prd"})

    # fallback لو جوميا غيرت ال HTML
    if len(items) < 20:
        items = soup.select("article")

    for item in items:
        try:
            name = item.find("h3", {"class": "name"}).get_text(strip=True)
        except:
            name = None

        brand = name.split()[0] if name else None

        try:
            price = item.find("div", {"class": "prc"}).get_text(strip=True)
        except:
            price = None

        try:
            old_price = item.find("div", {"class": "old"}).get_text(strip=True)
        except:
            old_price = None

        try:
            discount_percent = item.find("div", {"class": "bdg _dsct"}).get_text(strip=True)
        except:
            discount_percent = None

        try:
            rating = item.find("div", {"class": "stars"}).get_text(strip=True)
        except:
            rating = None

        try:
            num_reviews = item.find("div", {"class": "rev"}).get_text(strip=True)
        except:
            num_reviews = None

        try:
            link = "https://www.jumia.com.eg" + item.find("a")["href"]
        except:
            link = None

        # NEW FAST FIELDS (لا يدخل داخل صفحة المنتج)
        try:
            image_url = item.find("img")["data-src"]
        except:
            image_url = None

        try:
            badge = item.find("div", {"class": "bdg _xs"}).get_text(strip=True)
        except:
            badge = None

        category = "Mobile"

        products.append([
            name, brand, price, old_price, discount_percent,
            rating, num_reviews, link,
            category, image_url, badge
        ])

    time.sleep(0.08)  # صغير جدًا لتسريع الرن

print(f"\nDONE! Total products collected: {len(products)}")

# -------- SAVE CSV --------
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "name", "brand", "price", "old_price", "discount_percent",
        "rating", "num_reviews", "link",
        "category", "image_url", "badge"
    ])
    writer.writerows(products)

print(f"\nSaved DATA to: {OUTPUT_FILE}")