import requests
import config

session = requests.Session()
session.headers.update(config.HEADERS)