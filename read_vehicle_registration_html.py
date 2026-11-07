"""
Reads the html file of `https://afdc.energy.gov/vehicle-registration` as a .csv
"""
import pandas as pd
import requests as rq  # used to get .html file from url
from bs4 import BeautifulSoup  # used to parse .html

def get_html(url: str):
    site = rq.get(url)
    return site.text

def filter_tabular(html: str):
    if '<table' in html:
        start = html.index('<table')
        end = html.index('</table>') + 8
    else:
        return None
    return html[start:end]

def read_caption(table):
    if table is None:
        return None
    caption_start = table.index('<caption>') + 9
    caption_end = table.index('</caption>')
    caption = table[caption_start:caption_end]
    return caption

def read_columns(table):
    pass

def read_state_data(table, columns):
    pass


if __name__ == "__main__":
    url = 'https://afdc.energy.gov/vehicle-registration'