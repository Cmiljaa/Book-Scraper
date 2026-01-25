import requests
from bs4 import BeautifulSoup
import config

def extract_detailed_book_data(book):
	description_div = book.find("div", id="product_description")
	if description_div: 
		description_p = description_div.find_next_sibling("p")
		description = description_p.get_text(strip=True) if description_p else 'N/A'
	else:
		description = 'N/A'
	return {
		'description': description
	}

def get_data(url):
	
	response = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT)

	if response.status_code != 200:
		print(f"Failed to receive the data. Status code: {response.status_code}")
		return []
	
	soup = BeautifulSoup(response.text, "html.parser")

	return soup.find('article', class_="product_page")
	

def main():
	print('main')
	data = get_data(url)
	detailed_book_data = extract_detailed_book_data(data)
	print(f"Description: {detailed_book_data['description']}")

main()

