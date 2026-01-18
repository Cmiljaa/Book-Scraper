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

def save_img(full_img_url):
	try:
		img_data = requests.get(full_img_url, stream=True)
		
		filename = full_img_url.split('/')[-1]
		if not filename:
			filename = 'downloaded_image.jpg'

		with open(f"images/{filename}", 'wb') as f:
			for chunk in img_data.iter_content(chunk_size=8192):
				f.write(chunk)
		print(f"Saved {filename}")
	except requests.exceptions.RequestException as e:
		print(f"Error downloading {full_img_url}: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")

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

def export_books_data(book_data):
	data_frame = pandas.DataFrame(book_data)
	data_frame.to_csv('books.csv', index=False)
	data_frame.to_json('books.json', orient='records', indent=4)
	data_frame.to_excel('Book_Data.xlsx', index=False)

def main(url):
	all_books = get_data(url)
	book_data = []
	if all_books:
		for book in all_books:
			data = extract_book_data(book)
			book_data.append(data)
			(f'{data['title']}')
			print(f'{data['price']}')
			print(f'{data['in_stock']}')
			print(f'{data['image_url']}')
			save_img(data['image_url'])
			print('-' * 100)
		export_books_data(book_data)

main(url)