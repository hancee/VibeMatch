import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv
from src.utils.definitions import DATA_DIRECTORY


class PerfumeScraper:
    def __init__(self, url):
        self.url = url
        try:
            self.api_key = SCRAPERAPI_API_KEY
        except NameError:
            from src.utils.scraper.creds import api_key

            self.api_key = api_key
        self.soup = self.get_soup_using_api()
        self.id = self.extract_id()
        self.gender = self.extract_gender()
        self.description = self.extract_description()
        self.accords = self.extract_accords()
        self.notes = self.extract_notes()
        self.top_notes = self.notes["top"]
        self.middle_notes = self.notes["middle"]
        self.base_notes = self.notes["base"]
        self.rating = self.extract_rating_info()["Rating"]
        self.n_rating = self.extract_rating_info()["Rating Count"]
        self.reviews = self.extract_reviews()

    def get_soup_using_api(self):
        payload = {"api_key": self.api_key, "url": self.url, "autoparse": True}
        response = requests.get("https://api.scraperapi.com/", params=payload)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def extract_id(self):
        return re.search(r':perfume_id="([\d]*)">', str(self.soup)).group(1)

    def extract_gender(self):
        return self.soup.find_all("small")[0].get_text(strip=True)[4:]

    def extract_description(self):
        return (
            self.soup.find("div", class_="cell", itemprop="description")
            .find_all("p")[0]
            .get_text(strip=False)
        )

    def extract_accords(self):
        accord_bars = self.soup.find_all("div", class_="accord-bar")
        accords = {}
        for accord_bar in accord_bars:
            width, accord = re.findall(
                r'width: ([\d\.]*)%;">(.*)</div>', str(accord_bar)
            )[0]
            accords[accord] = width
        return accords

    def extract_notes(self):
        levels = {"top": [], "middle": [], "base": []}
        for level in levels.keys():
            match = self.soup.find("pyramid-level", {"notes": level})
            if match:
                text_content = match.get_text(strip=True)
                levels[level] = re.split(r"(?<=[a-z])(?=[A-Z])", text_content)
        return levels

    def extract_rating_info(self):
        try:
            return {
                "Rating": self.soup.find("span", itemprop="ratingValue").get_text(
                    strip=False
                ),
                "Rating Count": self.soup.find("span", itemprop="ratingCount").get_text(
                    strip=False
                ),
            }
        except:
            return {"Rating": None, "Rating Count": 0}

    def extract_reviews(self):
        divs = self.soup.find_all("div", itemprop="reviewBody")
        reviews = []
        for div in divs:
            paragraphs = div.find_all("p")
            reviews.append(" ".join([p.get_text(strip=True) for p in paragraphs]))
        return reviews
