import requests
from bs4 import BeautifulSoup
import time
import os
from concurrent.futures import ThreadPoolExecutor

def download_html(url_and_folder):
    url, folder = url_and_folder
    while True:
        response = requests.get(url)
        if "Just a moment..." in response.text:
            time.sleep(2)
        else:
            filename = url.split("/")[-2] + url.split("/")[-1] + ".html"
            path = os.path.join(folder, filename)
            with open(path, "w") as file:
                file.write(response.text)
            break

def main():
    with open("masters_urls.txt", "r") as file:
        urls = [url.strip() for url in file.readlines()]

    url_and_folder_pairs = []
    for i, url in enumerate(urls):
        page_number = i // 15 + 1
        folder = f"HTML/Page_{page_number}"
        os.makedirs(folder, exist_ok=True)
        url_and_folder_pairs.append((url, folder))

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_html, url_and_folder_pairs)

if __name__ == '__main__':
    main()