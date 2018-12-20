from typing import Optional

import bs4

from .err import ParseException


class Card:

    @staticmethod
    def elems(html):
        soup = bs4.BeautifulSoup(html, 'lxml')
        return soup.select('div.jobsearch-SerpJobCard')

    def __init__(self, elem):
        self.elem = elem

    def to_dict(self):
        funcs = (
            ('jk', lambda: self.elem.get('data-jk')),
            ('employer', self._employer),
            ('loc', self._location),
            ('title', self._title),
            ('summary', self._summary),
            ('sponsored', self._sponsored))
        ret = {}
        for key, func in funcs:
            try:
                ret[key] = func()
            except AttributeError as e:
                msg = "AttributeError(%s): %s" % (key, e)
                raise ParseException(msg, html=str(self.elem))

        return ret

    def _employer(self) -> Optional[str]:
        span = self.elem.find('span', class_='company')
        if span:
            return span.get_text().strip()

    def _location(self) -> Optional[str]:
        span = self.elem.find('span', class_='location')
        if span:
            return span.get_text().strip()

    def _title(self) -> str:
        elem = self.elem.select('.jobtitle').pop()
        return elem.get_text().strip()

    def _summary(self) -> str:
        span = self.elem.find('span', class_='summary')
        return span.get_text().strip()

    def _sponsored(self) -> bool:
        span = self.elem.find('span', class_='sponsoredGray')
        return bool(span)
