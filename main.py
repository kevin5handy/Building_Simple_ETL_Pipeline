import time
import datetime 
import pandas as pd
import requests
from bs4 import BeautifulSoup
from transform import transform_to_df, clean_dirty_data, transform_data
from load import upload_to_csv, upload_to_postgre, upload_to_gsheet
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}
 
 
def fetching_content(url):
    """Mengambil konten HTML dari URL."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi ERROR ketika melakukan requests terhadap {url}: {e}")
        return None
 
 
def extract_book_data(article):
    """Mengambil data buku berupa Title, Price, Rating, Colors, Size, dan Gender dari WEB."""
    prod_title = article.find("h3", class_="product-title").text.strip()
    price_container = article.find("div", class_="price-container")
    price = price_container.find("span", class_="price").text.strip() if price_container else "Price not found"
    
    detail = article.find_all("p")
    rating = colors = size = gender = "Data Not found"
    for p in detail:
        text = p.text.strip()
        if "Rating:" in text:
            rating = text.replace("Rating:", "").strip()
        elif "Colors" in text:
            colors = text.strip()
        elif "Size:" in text:
            size = text.replace("Size:", "").strip()
        elif "Gender:" in text:
            gender = text.replace("Gender:", "").strip()
 
    products = {
        "Title": prod_title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender
    }
 
    return products
 
 
def scrape_book(base_url, start_page=1, delay=2):
    """Data Collecting."""
    data = []
    page_number = start_page
 
    while True:
        if page_number == 1:
            url = base_url  
        else:
            url = f"{base_url}page{page_number}.html"

        print(f"Scraping halaman: {url}")
        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles_element = soup.find_all("div", class_="product-details")
            for article in articles_element:
                prod = extract_book_data(article)
                prod["Timestamp"] = datetime.datetime.now().isoformat()
                data.append(prod)
 
            next_button = soup.find("li", class_="next")
            if next_button:
                page_number += 1
                time.sleep(delay) 
            else:
                break 
        else:
            break 
 
    return data
 
 
def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = "https://fashion-studio.dicoding.dev/"
    all_books_data = scrape_book(BASE_URL)
    if all_books_data:
        # to DataFrame
        df = transform_to_df(all_books_data)  
        
        # to Transform Data
        df = clean_dirty_data(df)
        df = transform_data(df, 16000)
        
        # Load Data in CSV, PostgreSQL, and Google Sheet
        upload_to_csv(df)
        db_url = 'postgresql+psycopg2://dev:Caoimhin_160902@localhost:5432/productdb_3'
        upload_to_postgre(df, db_url)
        upload_to_gsheet(df)

        print(df)
    else:
        print("Not Found.")
 
 
if __name__ == '__main__':
    main()