#!/usr/bin/env python
#####################################################################################################################################
# imports ###########################################################################################################################
#####################################################################################################################################
import os
from requests import get 
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# import cusotm helper libary 
from basic_request import *


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