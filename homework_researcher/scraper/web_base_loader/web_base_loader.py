from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from ..utils import get_relevant_images, extract_title


class WebBaseLoaderScraper:

    def __init__(self, link, session=None):
        self.link = link
        self.session = session or requests.Session()

    def scrape(self) -> tuple:
        """
        This Python function scrapes content from a webpage using a WebBaseLoader object and returns the
        concatenated page content.

        Returns:
          The `scrape` method is returning a string variable named `content` which contains the
        concatenated page content from the documents loaded by the `WebBaseLoader`. If an exception
        occurs during the process, an error message is printed and an empty string is returned.
        """
        try:
            from langchain_community.document_loaders import WebBaseLoader

            loader = WebBaseLoader(self.link)
            loader.requests_kwargs = {"verify": False}
            docs = loader.load()
            content = ""

            for doc in docs:
                content += doc.page_content

            response = self.session.get(self.link)
            soup = BeautifulSoup(response.content, "html.parser")
            image_urls = get_relevant_images(soup, self.link)

            # Extract the title using the utility function
            title = extract_title(soup)

            return content, image_urls, title

        except Exception as e:
            print("Error! : " + str(e))
            return "", [], ""
