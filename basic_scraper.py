#!/usr/bin/env python
#####################################################################################################################################
# imports ###########################################################################################################################
#####################################################################################################################################
import os
import logging
import re
import json
from contextlib import closing
from requests import get 
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

#####################################################################################################################################
# Helper functions ##################################################################################################################
#####################################################################################################################################

def simple_get(url):
    """
    Attempts to get the content at 'url' by making a HTTP GET request. 
    If the content-type of response is some kind of HTML/XML, return the 
    text content, otherwise return None. 
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url,str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise
    """
    content_types = ("html","json","csv")
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and any(ct in content_type for ct in content_types))

def log_error(e):
    """
    It is always a good idea to log errors
    This function just prints them, but you can 
    make it do anything.
    """
    print(e)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################


# url we want to scrape
url = 'https://archives.library.illinois.edu/archon/?p=collections/findingaid&id=4719&q=correspondence&rootcontentid=83972#id83972'

# Get the site content
response = simple_get(url)

# Parse the site content
soup = BeautifulSoup(response, 'html.parser')

# Get the description list (e.g. Series 2: Amateurism)
description_list = soup.find('div', {"id": "famain"} ).dl
data_tag = description_list.dt
data_tag_title = data_tag.text

# All boxes for this series
data_boxes = description_list.dd.dl

# A list of all the box titles
box_titles = data_boxes.findChildren(['dt'], recursive=False)

# a list (of lists) of all boxes content 
box_contents = data_boxes.find_all(['dd'], recursive=False)

file_name = "data.csv"
if os.path.exists(file_name):
  os.remove(file_name)

print("Writing data file...")
f = open(file_name, "w+")
# set the CSV seperation character
f.write("sep=|\n")

# loop over all the box titles and the box content
for box_title, box_content in zip(box_titles, box_contents):
    box_title_text = box_title.text # get the box title text
    box_items = box_content.dl.findChildren(['dt'], recursive = False) # a list of all the top level items
    for box_item in box_items:
        item_text = box_item.text
        line = "{} | {} | {} \n".format(data_tag_title, box_title_text, item_text)
        f.write(line)

f.close()
print("Done!")