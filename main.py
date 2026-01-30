import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas
import book_page_scraper
import config

def get_data(url):
	response = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT)

	if response.status_code != 200:
		print(f"Failed to receive the data. Status code: {response.status_code}")
		return []
	
	soup = BeautifulSoup(response.text, "html.parser")

	return soup.find_all('article', class_="product_pod")

def save_img(full_img_url):
	try:
		img_data = requests.get(full_img_url, headers=config.HEADERS, timeout=config.TIMEOUT, stream=True)
		
		filename = full_img_url.split('/')[-1]
		if not filename:
			filename = 'downloaded_image.jpg'

		with open(f"{config.IMAGES_DIR}/{filename}", 'wb') as f:
			for chunk in img_data.iter_content(chunk_size=8192):
				f.write(chunk)
		print(f"Saved {filename}")
	except requests.exceptions.RequestException as e:
		print(f"Error downloading {full_img_url}: {e}")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")

def extract_book_data(book, url):
	name_tag = book.find('h3')

	book_link = name_tag.find()
	book_link = urljoin('https://books.toscrape.com', book_link['href'])
	book_page = book_page_scraper.get_data(book_link)
	book_data = book_page_scraper.extract_detailed_book_data(book_page)
	description = book_data['description']

	title = name_tag.find().text if name_tag else 'N/A'

	price_tag = book.find('p', class_='price_color')
	price = price_tag.text.strip().replace("Â£","")

	in_stock_tag = book.find('p', class_='instock availability')
	in_stock = in_stock_tag.text.strip() if in_stock_tag else 'N/A'

	rating_tag = book.find("p", class_=["star-rating"])
	rating = rating_tag.text.strip() if rating_tag else 'N/A'
	classes = rating_tag.get("class", [])
	rating_class = [c for c in classes if c != "star-rating"][0]
	rating_map = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
	rating = rating_map.get(rating_class, 0)

	img_tag = book.find('img', class_='thumbnail')
	img_url = img_tag['src']
	full_img_url = urljoin(url, img_url)

	return {
		"title": title,
        "price": price,
        "in_stock": in_stock,
		"rating": rating,
		"description": description,
        "image_url": full_img_url
	}

def export_books_data(book_data):
	data_frame = pandas.DataFrame(book_data)
	data_frame.to_csv('books.csv', index=False)
	data_frame.to_json('books.json', orient='records', indent=4)
	data_frame.to_excel('Book_Data.xlsx', index=False)

def main(generated_urls):
	for url in generated_urls:
		all_books = get_data(url)
		book_data = []
		if all_books:
			for book in all_books:
				data = extract_book_data(book, url)
				book_data.append(data)
				(f'{data["title"]}')
				print(f'{data["price"]}')
				print(f'{data["in_stock"]}')
				print(f'{data["rating"]}')
				print(f'{data["description"]}')
				print(f'{data["image_url"]}')
				save_img(data["image_url"])
				print('-' * 100)
			export_books_data(book_data)

main(config.GENERATED_URLS)