import requests
from bs4 import BeautifulSoup
import urllib.parse


class FandomQueryService:
    def __init__(self):
        self.base_url = "https://community.fandom.com/wiki/Special:Search?scope=cross-wiki&ns%5B0%5D=0&ns%5B1%5D=4&ns%5B2%5D=12&ns%5B3%5D=110&ns%5B4%5D=112&ns%5B5%5D=118&ns%5B6%5D=500&ns%5B7%5D=502&ns%5B8%5D=2900&"

    def get_search_results(self, query: str):
        url = self.base_url + urllib.parse.urlencode({"query": f'"{query}"'})

        r = requests.get(url,  allow_redirects=True)
        print(url, flush=True)

        soup = BeautifulSoup(r.content, "html.parser")
        # Get all <a> tags with href
        # Find the <ul> containing search results
        ul = soup.find("ul", class_="unified-search__results")

        # Find all <a> tags inside that <ul>
        links = [a.get("href") for a in ul.find_all("a") if a.get("href")]

        for i in links[:]:  # iterate over a copy so removal is safe
            if "/wiki/User" in i:
                links.remove(i)


        return links

    def get_page_image_links(self, link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        # Find the <figure> that contains the main image

        aside = soup.find("aside")

        if aside:
            img = aside.find("img")
            if img and img.parent.name == "a" and img.parent.get("href"):
                image_links = [img.parent["href"]]
                return image_links


        figure = soup.find("figure")
        if figure:
            img = figure.find("img")
            if img and img.parent.name == "a" and img.parent.get("href"):
                image_links = [img.parent["href"]]
                return image_links

        table = soup.find("table")
        if table:
            img = table.find("img")
            if img and img.parent.name == "a" and img.parent.get("href"):
                image_links = [img.parent["href"]]
                return image_links


        figures = soup.select("figure a[href] img")

        image_links = [
            img.parent["href"]
            for img in figures
        ]

        return image_links

    def get_page_paragraphs(self, link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

        return paragraphs
