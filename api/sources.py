import requests
from bs4 import BeautifulSoup

class TabSource:
    def __init__(self, url: str):
        self.url = url

    def _get_and_parse(self, url):
        request = requests.get(url)
        if (request.status_code != 200):
            raise TabFetchingException(f"Tab source returned with status code {request.status_code}. URL: f{url}")
        content = request.text
        return BeautifulSoup(content)

    def _find_best_tab(self, query: str):
        pass

    def _get_download_url(self):
        pass

    def fetch(self, query):
        tab = self._find_best_tab(query)
        return self._get_download_url(tab)



class GPTSource(TabSource):
    def _find_best_tab(self, query):
        soup = self._get_and_parse(self._create_search_query(query))

        best_match = None
        most_downloads = 0
        rows = soup.findAll("tr")[1:-1]
        if (len(rows)) == 0:
            raise TabFetchingException(f"No tabs were found for query '{query}'")
        
        for tr in rows:
            downloads = int(tr.find_all("span", class_="badge")[0].text.replace(",",""))
            if downloads >= most_downloads:
                most_downloads = downloads
                best_match = tr.find_all("a")[0]["href"]
        return best_match

    def _get_download_url(self, file_url):
        return f"{file_url}download/"

    def _create_search_query(self, query):
        return f"{self.url}search.php?search={query.replace(' ','+')}&in=songs&page=1"


class TabFetchingException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
