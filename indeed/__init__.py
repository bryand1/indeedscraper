import csv
import gzip
import os
from functools import partial
from glob import glob
import re
import sys
import time
from typing import Dict, List

from .err import CrawlException, ParseException
from .crawler import Indeed
from .card import Card
import util


log = util.get_logger('indeed')
    

def download(args):
    """Download html files"""

    # If the command-line option `--parse` is set, then user
    # intends to only parse existing files in `data` directory.
    # Abort the download
    if args.parse:
        return

    start = time.time()

    output_dir = './data'
    os.makedirs(output_dir, mode=0o755, exist_ok=True)

    gzip_on = args.gzip == 'on'

    template = "{what}-{where}-{page:04d}.html"
    if gzip_on:
        template += '.gz'
    what = util.slug(args.what)
    where = 'all' if not args.where else util.slug(args.where)
    page = 1
    mkfilename = partial(_mkfilename, template, what, where)

    log.info("%r ready to crawl up to %d pages", what, args.limit)

    crawler = Indeed(args)
    content = crawler.search(args.what, args.where)
    path = os.path.join(output_dir, mkfilename(page))
    _save(path, content, compress=gzip_on)
    log.info("%r page %d saved to %s", args.what, page, path)
    while crawler.has_next() and page < args.limit:
        time.sleep(args.sleep)
        page += 1
        content = crawler.next()
        path = os.path.join(output_dir, mkfilename(page))
        _save(path, content, compress=gzip_on)
        log.info("%r page %d saved to %s", args.what, page, path)
    
    log.info("download done %.1f sec", time.time() - start)

def parse(args):
    # If the command-line option `--download` is set, then user
    # intends to only download job postings in `data` directory.
    # Abort the parse
    if args.download:
        return

    start = time.time()

    gzip_on = args.gzip == 'on'

    output_dir = './data'
    template = "{what}-{where}-*.html"
    if gzip_on:
        template += '.gz'
        _open = gzip.open
        _decode = lambda x: x.decode('utf-8')
    else:
        _open = open
        _decode = lambda x: x

    what = util.slug(args.what)
    where = 'all' if not args.where else util.slug(args.where)
    glob_expr = os.path.join(output_dir, template.format(what=what, where=where))

    # Parse jobs
    all_jobs = []

    for filepath in sorted(glob(glob_expr)):
        with _open(filepath) as fh:
            html = _decode(fh.read())
        jobs = _parse(html)
        all_jobs.extend(jobs)

    log.info("%r", all_jobs[0])

    # Create CSV filepath
    filename = "{what}-{where}.csv".format(what=what, where=where)
    if os.path.isdir(args.out):
        csvpath = os.path.join(args.out, filename)
    else:
        csvpath = args.out

    # Save parsed jobs
    fh = open(csvpath, 'w', newline='')
    csvwriter = csv.writer(fh, lineterminator='\n')
    header = ['what', 'where', 'rank', 'sponsored', 'employer', 'title', 'loc', 'viewjob', 'summary']
    csvwriter.writerow(header)
    _where = args.where or 'all'
    for job in all_jobs:
        row = [
            args.what, _where, job['rank'], _sponsored(job['sponsored']), job['employer'],
            job['title'], job['loc'], _viewjob(job['jk']), job['summary']]
        csvwriter.writerow(row)
    fh.close()

    log.info("parsing done %.1f sec", time.time() - start)

def clean(args):
    """Remove HTML files"""
    if not args.clean:
        return

    output_dir = './data'
    template = "{what}-{where}-*"

    what = util.slug(args.what)
    where = 'all' if not args.where else util.slug(args.where)
    glob_expr = os.path.join(output_dir, template.format(what=what, where=where))

    for filepath in glob(glob_expr):
        os.remove(filepath)

def _mkfilename(tpl: str, what: str, where: str, page: int):
    """Make filename from template string"""
    return tpl.format(what=what, where=where, page=page)


def _save(path, content, compress=True):
    """Save content as gzip compressed file or utf-8 text"""
    _open = gzip.open if compress else open
    _mode = 'wb' if compress else 'w'
    with _open(path, _mode) as fh:
        fh.write(content if compress else content.decode('utf-8'))
 
rank = 0

def _parse(html: str) -> List[Dict]:
    global rank
    jobs = []
    for elem in Card.elems(html):
        try:
            d = Card(elem).to_dict()
        except ParseException as e:
            log.critical("ParseException: %s %r", e.msg, e.html)
            sys.exit(1)

        rank += 1
        d['rank'] = rank
        jobs.append(d)
    return jobs

def _sponsored(b: bool) -> str:
    return 'Yes' if b else 'No'

def _viewjob(jk: str) -> str:
    return "https://www.indeed.com/viewjob?jk={}".format(jk)
