# Indeed Job Scraper

![license MIT](https://s3-us-west-1.amazonaws.com/bryand1/images/badges/license-MIT-blue.svg)
![Python 3.6 | 3.7](https://s3-us-west-1.amazonaws.com/bryand1/images/badges/python-3.6-3.7.svg)

![Indeed.com](https://github.com/bryand1/indeedscraper/blob/master/docs/gis-technician.png)

![Indeed.com job search results](https://github.com/bryand1/indeedscraper/blob/master/docs/gis-techician-2.png)

## Getting started

```bash
git clone https://github.com/bryand1/indeedscraper
cd indeedscraper
# activate virtual environment
pip install -r requirements.txt
python main.py "gis technician" [--where "Santa Monica"] [--out .] \
  [--limit 100] [--sleep] [--download | --parse] [--clean]
```

### Arguments

| argument | default value | description |
| -------- | ------------- | ----------- |
| `what` | **required** user must provide value | search term(s) |
| `--where` | all locations | city, state, or zip code |
| `--out` | `.` | directory to output CSV file |
| `--limit` | `10` | page limit |
| `--sleep` | `2` | seconds in between http requests |
| `--download` | `false` | only download html files, but do not parse |
| `--parse` | `false` | only parse html files that match query |
| `--clean` | `false` | remove html files after scraping is over |
| `--gzip` | `on` | compress html files |

### Usage

```bash
# Find job postings that match the search term
# 'gis technician' in any location and output
# results to the file ./gis-technician-all.csv
python main.py "gis technician"
```

### Geographic search

```bash
# Find job postings that match the search term
# 'business analyst' in 'New York' and output
# results to the file /jobhunt/jobs.csv
python main.py "business analyst" --where "New York" --out "/jobhunt/jobs.csv"
```

### Issues

Please report any issues. Feel free to fork and contribute patches. :smile:
