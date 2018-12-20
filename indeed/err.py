class IndeedException(Exception):
    """"""


class CrawlException(IndeedException):
    """Indeed Crawl Exception"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def __repr__(self, code, message):
        return "CrawlException({code}): {message}".format(
            code=code, message=message)


class ParseException(IndeedException):
    """Indeed Parse Exception"""

    def __init__(self, msg, html=''):
        self.msg = msg
        self.html = html

    def __repr__(self):
        return "ParseException({msg}): {html}".format(
            msg=self.msg, html=self.html)
