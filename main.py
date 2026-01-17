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

