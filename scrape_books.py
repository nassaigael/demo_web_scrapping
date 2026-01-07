import requests
from bs4 import BeautifulSoup
import json
from tabulate import tabulate
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def scrape_products(base_url, category_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.0.0 Safari/537.36"
    }

    url = base_url + category_url
    print(Fore.CYAN + f"Sending request to {url}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(Fore.RED + f"Error retrieving the page (Status code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")

    data = []
    for product in products:
        title = product.h3.a["title"]
        price = product.find("p", class_="price_color").text
        availability = product.find("p", class_="instock availability").text.strip()
        category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
        data.append({
            "title": title,
            "price": price,
            "availability": availability,
            "category": category
        })

    print(Fore.GREEN + f"{len(data)} products found.")
    return data

def save_json(data, filename="products.json"):
    print(Fore.YELLOW + f"Saving data to {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(Fore.GREEN + "JSON file successfully created.")

def display_table(data):
    print(Fore.MAGENTA + "\nPreview of the first 5 products:\n")
    headers = ["Title", "Price", "Availability", "Category"]
    table = tabulate([ [p["title"], p["price"], p["availability"], p["category"]] for p in data[:5] ],
                     headers, tablefmt="fancy_grid")
    print(Fore.CYAN + table)

def main():
    base_url = "http://books.toscrape.com/catalogue/category/books/"
    category_url = "travel_2/index.html"  # Travel category
    
    products = scrape_products(base_url, category_url)
    if products:
        save_json(products)
        display_table(products)

if __name__ == "__main__":
    main()
