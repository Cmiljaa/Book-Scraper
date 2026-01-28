def generate_urls():
	generated_urls = []
	for i in range(1, 51):
		generated_urls.append(f"https://books.toscrape.com/catalogue/page-{i}.html")
	return generated_urls

GENERATED_URLS = generate_urls()

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

TIMEOUT = 10

IMAGES_DIR = "images"