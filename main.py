import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas

url = 'https://books.toscrape.com/index.html'

def get_data(url):
	response = requests.get(url)

	if response.status_code != 200:
		print(f"Failed to receive the data. Status code: {response.status_code}")
		return []
	
	soup = BeautifulSoup(response.text)

	return soup.find_all('article', class_="product_pod")

def extract_book_data(book):
	name_tag = book.find('h3')
	title = name_tag.findChild().text if name_tag else 'N/A'

	price_tag = book.find('p', class_='price_color')
	price = price_tag.text if price_tag else 'N/A'

	in_stock_tag = book.find('p', class_='instock availability')
	in_stock = in_stock_tag.text.strip() if in_stock_tag else 'N/A'

	img_tag = book.find('img', class_='thumbnail')
	img_url = img_tag['src']
	full_img_url = urljoin(url, img_url)

	return {
		"title": title,
        "price": price,
        "in_stock": in_stock,
        "image_url": full_img_url
	}
