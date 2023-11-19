import requests
from bs4 import BeautifulSoup
import time
import os

BASE_URL = "https://www.findamasters.com/masters-degrees/msc-degrees/"
OUTPUT_FILE = "masters_urls.txt"
number_of_pages = 400


def get_course_urls(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    course_links = soup.find_all("a", class_="courseLink text-dark")
    urls = [
        "https://www.findamasters.com" + link["href"]
        for link in course_links
        if "href" in link.attrs
    ]
    return urls


def main():
    for page in range(number_of_pages):
        # Progress bar
        if (page + 1) % 25 == 0 or page == 0:
            print(f"Scraping page {page + 1}")

        # String of page_url, in the first page only get the BASE_URL
        if page == 0:
            page_url = f"{BASE_URL}"
        else:
            page_url = f"{BASE_URL}?PG={page + 1}"
        urls = get_course_urls(page_url)

        if urls:
            # Append to the file so it remembers the previous entries
            with open(OUTPUT_FILE, "a") as file:
                for url in urls:
                    file.write(f"{url}\n")

        # Sleeping to not have too many requests
        time.sleep(1)

    with open(OUTPUT_FILE, "r") as file:
        for count, line in enumerate(file):
            pass
    # This needs to be 6000
    print("Total Lines", count + 1)


if __name__ == "__main__":
    main()
