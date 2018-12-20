import logging
import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys


def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.propagate = False
    f = logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", 
        datefmt="%Y-%m-%dT%H:%M:%SZ")
    hdlr = logging.StreamHandler(sys.stdout)
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(f)
    log.addHandler(hdlr)
    return log


def slug(s: str) -> str:
    match = re.search(r'[A-Za-z0-9\s,.-]+', s)
    r = match.group(0)
    r = r.lower()
    for char in (' ', ',', '.'):
        r = r.replace(char, '-')
    return r


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
