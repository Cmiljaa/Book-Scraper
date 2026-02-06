import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas
import book_page_scraper
import config
from session import session

def generate_urls():
	generated_urls = []
	for i in range(1, 51):
		generated_urls.append(f"https://books.toscrape.com/catalogue/page-{i}.html")
	return generated_urls

def get_data(url):
	response = session.get(url, timeout=config.TIMEOUT)
	if response.status_code != 200:
		print(f"Failed to receive the data. Status code: {response.status_code}")
		return []
	
	soup = BeautifulSoup(response.text, "html.parser")

	return soup.find_all('article', class_="product_pod")

def save_img(full_img_url):
	try:
		img_data = session.get(full_img_url, timeout=config.TIMEOUT, stream=True)
		
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
    name_tag = book.find("h3")
    link_tag = name_tag.find("a") if name_tag else None
    if not link_tag:
        return None

    book_link = urljoin(
        "https://books.toscrape.com/catalogue/",
        link_tag["href"]
    )

    book_page = book_page_scraper.get_book_page_data(book_link)
    if not book_page:
        description = "N/A"
    else:
        book_data = book_page_scraper.extract_detailed_book_data(book_page)
        description = book_data.get("description", "N/A")

    title = link_tag.get_text(strip=True)

    price_tag = book.find("p", class_="price_color")
    price = price_tag.get_text(strip=True).replace("Â£", "") if price_tag else "N/A"

    in_stock_tag = book.find("p", class_="instock availability")
    in_stock = in_stock_tag.get_text(strip=True) if in_stock_tag else "N/A"

    rating_tag = book.find("p", class_=["star-rating"])
    rating = rating_tag.text.strip() if rating_tag else 'N/A'
    classes = rating_tag.get("class", [])
    rating_class = [c for c in classes if c != "star-rating"][0]
    rating_map = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}
    rating = rating_map.get(rating_class, 0)
	
    img_tag = book.find("img")
    img_url = urljoin(url, img_tag["src"]) if img_tag else None

    return {
        "title": title,
        "price": price,
        "in_stock": in_stock,
        "rating": rating,
        "description": description,
        "image_url": img_url
    }

def export_books_data(book_data):
	data_frame = pandas.DataFrame(book_data)
	data_frame.to_csv('books.csv', index=False)
	data_frame.to_json('books.json', orient='records', indent=4)
	data_frame.to_excel('Book_Data.xlsx', index=False)

def main():
	generated_urls = generate_urls()
	book_data = []
	for url in generated_urls:
		all_books = get_data(url)
		if all_books:
			for book in all_books:
				data = extract_book_data(book, url)
				if data:
					book_data.append(data)
					print(f'{data["title"]}')
					print(f'{data["price"]}')
					print(f'{data["in_stock"]}')
					print(f'{data["rating"]}')
					print(f'{data["description"]}')
					print(f'{data["image_url"]}')
					if data["image_url"]:
						save_img(data["image_url"])
					print('-' * 100)
				else:
					print('No data at all')
	export_books_data(book_data)

main()