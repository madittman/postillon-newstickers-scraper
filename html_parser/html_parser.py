import json
import requests
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class HtmlParser:
    urls: dict[int, str]

    def read_json(self):
        """Load the JSON file 'urls.json'."""
        with open("urls.json", "r", encoding="utf-8") as json_file:
            self.urls: dict[int, str] = json.load(json_file)

    def parse_url(self):
        # 1. Fetch the webpage content
        url = "https://www.der-postillon.com/2017/09/newsitcker-1104.html"
        response = requests.get(url)

        # 2. Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # 3. Locate the main article content
        # Der Postillon uses Blogger, so the content is usually in a div with class 'post-body'
        content_div = soup.find('div', class_='post-body')

        if content_div:
            # Get the text from the div
            text = content_div.get_text()

            # 4. Extract sentences between +++
            # We use a regex to find text between +++ delimiters.
            # The pattern matches '+++' followed by non-greedy content until the next '+++'
            # We strip whitespace to clean up the results.

            # Method A: Using Split (Simple and handles shared delimiters like +++ A +++ B +++)
            raw_segments = text.split('+++')

            # Filter and clean the segments
            sentences = []
            for segment in raw_segments:
                clean_segment = segment.strip()
                # Filter out empty strings and short fragments (like navigation artifacts)
                if len(clean_segment) > 10:
                    sentences.append(clean_segment)

            # Output the results
            for i, sentence in enumerate(sentences, 1):
                print(f"{i}: {sentence}")

        else:
            print("Could not find the content area.")