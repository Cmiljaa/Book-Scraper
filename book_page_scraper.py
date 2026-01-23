import requests
from bs4 import BeautifulSoup
def get_data(url):
	
	response = requests.get(url, headers=HEADERS, timeout=10)

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

