"""
Reads the html file of `https://afdc.energy.gov/vehicle-registration` and
returns a dictionary of tables by year
"""
import pandas as pd
import requests as rq  # used to get .html file from url
from io import StringIO


def html_to_txt(url):
    html = rq.get(url).text
    return html


def parse_html(html):
    table = pd.read_html(StringIO(html))[0]
    return table


def merge_by_year(url):
    tables = {}
    for i in range(2016, 2026):
        html = html_to_txt(f"{url}?year={i}")
        tables[i] = (parse_html(html))
    return tables

def main():
    url = 'https://afdc.energy.gov/vehicle-registration'
    all_tables = merge_by_year(url)
    return all_tables
        


if __name__ == "__main__":
    main()