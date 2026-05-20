import requests

def shorten_url(url):
    response = requests.get(url)
    return response.text

url = "https://python1c.ru/catalogs/api?format=json"
short_url = shorten_url(url)
print(f"The shortened URL is: {short_url}")