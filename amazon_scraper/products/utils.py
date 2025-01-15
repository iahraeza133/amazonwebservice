import requests
from bs4 import BeautifulSoup

def scrape_amazon(amazon_code):
    url = f"https://www.amazon.com/dp/{amazon_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    try:
        name = soup.select_one("#productTitle").text.strip()
        price = float(soup.select_one(".a-price .a-offscreen").text.replace("$", ""))
        rating = float(soup.select_one(".a-icon-alt").text.split()[0])
        reviews_count = int(soup.select_one("#acrCustomerReviewText").text.split()[0].replace(",", ""))
        return {
            "amazon_code": amazon_code,
            "name": name,
            "price": price,
            "rating": rating,
            "reviews_count": reviews_count,
        }
    except Exception:
        return None
