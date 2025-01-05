import json
import requests
from bs4 import BeautifulSoup
from src.utils.scraper.creds import api_key
from src.utils.definitions import DATA_DIRECTORY
from pathlib import Path


class FragranceReviewScraper:
    def __init__(self, url):
        self.url = url
        self.api_key = api_key
        self.soup = self.get_soup_using_api()
        self.paragraphs = self.extract_paragraphs()
        self.write_dir = Path.joinpath(DATA_DIRECTORY, "documents")

    def get_soup_using_api(self):
        payload = {"api_key": self.api_key, "url": self.url, "autoparse": True}
        response = requests.get("https://api.scraperapi.com/", params=payload)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def extract_paragraphs(self):
        p_tags = self.soup.select("div.card-section p")
        paragraphs = [p.get_text().strip() for p in p_tags]
        paragraphs = [paragraph for paragraph in paragraphs if len(paragraph) > 0]
        return paragraphs

    def extract_main_content(self):
        return self.paragraphs[1:]

    def extract_metadata(self):
        title = [p.get_text().strip() for p in self.soup.select("h1")][0]
        meta = [s.strip() for s in self.paragraphs[0].split("\n")]
        return {
            "Source": self.url,
            "Title": title,
            "Author": meta[1],
            "Published": meta[2],
        }

    def extract_comments(self):
        sections = self.soup.find_all("div", class_="flex-child-auto")
        texts = [section.get_text(separator=" ", strip=True) for section in sections]
        return texts

    def write_to_json(self):
        # Extract paragraphs and other data
        content = self.extract_main_content()
        metadata = self.extract_metadata()
        comments = self.extract_comments()

        # Prepare data to write to JSON
        data = {"Content": content, "Comments": comments, "Metadata": metadata}

        # Write data to JSON file
        title = metadata["Title"] if metadata["Title"] else self.url
        with open(Path.joinpath(self.write_dir, f"{title}.json"), "w") as json_file:
            json.dump(data, json_file, indent=4)
