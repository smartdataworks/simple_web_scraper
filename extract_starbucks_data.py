#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 00:05:14 2020

@author: emanuel
"""

import requests
from bs4 import BeautifulSoup
import re
import itertools
import json
import pandas as pd

def remove_single_quotes(text):
    """
    Simple helper function that replaces single quotes with double quotes
    at the beginnig of the key and value fields.
    """
#    pattern = re.compile("(?<!\\\\)\'")
    pattern_1 = re.compile(r"(?<=[\{|,|, |:])\'")
    pattern_2 = re.compile(r"\'(?=:|,|\})")
    step_1 = pattern_1.sub('\"', text)
    return pattern_2.sub('\"', step_1)



def remove_newlines(text):
    return re.sub("\n", " ", text)


def remove_html_tags(text):
    regex = re.compile(r"<[^>]+>")
    return regex.sub(" ", text)


def find_data_section(text):
    regex = re.compile(r"var data = \[([^\]]+)\]")
    return regex.search(str(text))


def find_individual_records(text):
    regex = re.compile(r"(\{[^\}]+\})")
    return regex.findall(text)


def extract_zip_code(text):
    regex = re.compile(r"CA [\d]{5}")
    return regex.search(text).group()


def extract_dictionary_items(record):
    return {'zip_code' if k == 'desc' else k:
            extract_zip_code(v) if k =='desc' else v
            for k, v in record.items()}


def extract_data(response):
    html = response.text
    soup = BeautifulSoup(html, 'html5lib')
    script_tags = soup.find("script", string=re.compile("starbucks")).string

    data_section = find_data_section(script_tags)
    if data_section is None:
        return
    data_section = data_section.group(1)
    data_section = remove_single_quotes(data_section)
    data_section = remove_newlines(data_section)
    data_section = remove_html_tags(data_section)

    output = list()
    for record in find_individual_records(data_section):
        data_dict = json.loads(record)
        if data_dict is not None:
            output.append(extract_dictionary_items(data_dict))

    return output

base_url = "http://www.city-data.com/locations/Starbucks/Los-Angeles-California"
ending = ".html"
output = list()

for i in itertools.count(1):
    if i == 1:
        page_number = ""
    else:
        page_number = f"-{i}"

    url = base_url + page_number + ending
    response = requests.get(url)
    if response.status_code != 200:
        break
    else:
        output += extract_data(response)

starbucks = pd.DataFrame(output)
print(starbucks)

for col in ['lat', 'lon']:
    starbucks[col] = pd.to_numeric(starbucks[col])

starbucks.to_csv("starbucks.csv")
