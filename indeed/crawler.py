import re

import bs4
import requests

import util


class Indeed:
    """Crawl Indeed.com job search pages"""

    log = util.get_logger("indeed.crawler.Indeed")

    home = "https://www.indeed.com"

    headers = {
        'accept': ('text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,image/webp,image/apng,*/*;q=0.8'),
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/'
                       '537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36')
    }

    csrf = re.compile(r"var\s+indeedCsrfToken\s+=\s+'(.+?)'")

    def __init__(self, args):
        self._args = args
        self._session = util.requests_retry_session()
        self._resp = None
        self._csrftoken = None
        self._next = None
        self._cookies = None

    def search(self, what, where=''):
        """Perform initial job search"""
        url = f"{self.home}/jobs"
        params = {'q': what, 'l': where}
        self._resp = self._session.get(url, headers=self.headers, params=params)
        self.log.info("[%d] %s", self._resp.status_code, self._resp.url)
        if self._resp.status_code == 200:
            return self._resp.content

    def has_next(self) -> bool:
        """Check if page has 'Next' button"""
        soup = bs4.BeautifulSoup(self._resp.text, 'lxml')
        anchors = soup.find_all('a')
        for anchor in anchors:
            if 'Next' in anchor.text and anchor.get('data-pp'):
                self._next = f"{self.home}{anchor['href']}&pp={anchor['data-pp']}"
                return True
        return False

    def next(self):
        """Query next page with csrftoken cookie"""
        match = self.csrf.search(self._resp.text)
        if match:
            self._csrftoken = match.group(1)
        self._cookies = {'INDEED_CSRF_TOKEN': self._csrftoken}
        self._resp = self._session.get(self._next, headers=self.headers, cookies=self._cookies)
        self.log.info("[%d] %s", self._resp.status_code, self._resp.url)
        return self._resp.content
