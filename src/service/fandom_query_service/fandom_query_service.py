import re
from difflib import SequenceMatcher
import numpy as np

from PIL import Image
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import urllib.parse


class FandomQueryService:
    TARGET_RATIO = 1
    MIN_WIDTH = 500
    MIN_HEIGHT = 500

    def __init__(self):
        self.base_url = "https://community.fandom.com/wiki/Special:Search?scope=cross-wiki&ns%5B0%5D=0&ns%5B1%5D=4&ns%5B2%5D=12&ns%5B3%5D=110&ns%5B4%5D=112&ns%5B5%5D=118&ns%5B6%5D=500&ns%5B7%5D=502&ns%5B8%5D=2900&"

    def get_search_results(self, query: str):
        url = self.base_url + urllib.parse.urlencode({"query": f'"{query}"'})

        r = requests.get(url,  allow_redirects=True)

        soup = BeautifulSoup(r.content, "html.parser")
        # Get all <a> tags with href
        # Find the <ul> containing search results
        ul = soup.find("ul", class_="unified-search__results")

        # Find all <a> tags inside that <ul>
        links = [a.get("href") for a in ul.find_all("a") if a.get("href")]

        # for i in links[:]:  # iterate over a copy so removal is safe
        #     if "/wiki/User" in i:
        #         links.remove()


        links = self.filter_links(links, query)


        return links


    def filter_links(self, links, query):
        pattern = re.compile(
            r"^https://([a-zA-Z0-9\-]+)\.fandom\.com/wiki/([^#?]+)$"
        )

        def similar(a, b):
            a = a.lower().strip()
            a = re.sub(r"[\s_\-\(\)\[\]:]+", " ", a)
            a.strip()

            b = b.lower().strip()
            b = re.sub(r"[\s_\-\(\)\[\]:]+", " ", b)
            b.strip()

            if a in b:
                return 1.0

            return SequenceMatcher(None, a, b).ratio()

        filtered = []

        for link in links:
            # 1. Skip /wiki/User*
            if "/wiki/User" in link:
                continue

            # 2. Must match the fandom wiki format
            match = pattern.match(link)
            if not match:
                continue

            # Extract the wiki page title part
            page_title = match.group(2).replace("_", " ")

            # 3. Check similarity to query
            if similar(query, page_title) < 0.4:  # tweak threshold if needed
                continue

            filtered.append(link)

        return filtered

    def get_page_image_links(self, link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        # # Find the <figure> that contains the main image
        #

        if "This article is a disambiguation page" in soup.get_text().lower():
            print(f"Found disambiguation: {link}")
            return []
        #
        # image_links = []
        #
        # aside = soup.find("aside")
        #
        # if aside:
        #     img = aside.find("img")
        #     if img and img.parent.name == "a" and img.parent.get("href"):
        #         image_links.append(img.parent["href"])
        #
        # figure = soup.find("figure")
        # if figure:
        #     imgs = figure.select("img")
        #     for img in imgs:
        #         if img and img.parent.name == "a" and img.parent.get("href"):
        #             image_links.append(img.parent["href"])
        #
        # tables = soup.select("table")
        # for table in tables:
        #     imgs = table.select("img")
        #     for img in imgs:
        #         if img and img.parent.name == "a" and img.parent.get("href"):
        #             image_links.append(img.parent["href"])
        #
        # # if len(image_links) > 0:
        # #     image_links.sort(key=self.get_image_ratio_score)
        # #     return image_links
        #
        # images = soup.select("img")
        #
        # for img in images:
        #     image_links.append(img["src"])
        #

        image_links = []
        main = soup.find("main")

        images = main.select("img")
        for i, img in enumerate(images):
            if img.get("src"):
                image_links.append(img["src"])


        # Remove duplicates while preserving order
        image_links = list(dict.fromkeys(image_links))

        image_links.sort(key=self.get_image_ratio_score)

        # print(f"Sorted image links {image_links}")
        return image_links


    def get_image_ratio_score(self, url: str):
        """Lower score = better. Penalises small size, bad ratio, and grayscale."""
        try:

            resp = requests.get(url, timeout=5)
            img = Image.open(BytesIO(resp.content)).convert("RGB")
            w, h = img.size

            # --- ratio & size scoring ---
            ratio_score = abs((w / h) - self.TARGET_RATIO)
            size_score = 1 / max(w * h, 1)  # big images => small penalty

            # penalise too-small images
            if w < self.MIN_WIDTH or h < self.MIN_HEIGHT:
                size_score *= 4

            # --- grayscale detection ---
            # If the three channels are almost identical -> grayscale
            arr = np.array(img)
            channel_std = arr.std(axis=(0, 1))  # std per channel: (R_std, G_std, B_std)
            color_variation = channel_std.mean()

            # typical threshold: 3–10 depending on image type
            is_grayscale = color_variation < 5

            # --- final score ---
            final_score = max(ratio_score, 0.001) * pow(size_score, 2)

            # penalise grayscale images
            if is_grayscale:
                final_score *= 3     # adjust weight as needed

            return final_score

        except Exception as e:
            print("Error:", e)
            return 99999

    def get_page_paragraphs(self, link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

        return paragraphs
