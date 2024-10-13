"""
Adapted from ChatGPT
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://astropixels.com/ephemeris/phasescat/phases0601.html"
# url = "https://en.wikipedia.org/wiki/Winston_Churchill"

# This is to act as though a user accessed the website
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# Send a GET request to the webpage
page = requests.get(url, headers=headers)

# Soup (don't know what that does yet)
soup = BeautifulSoup(page.text, "html")

data = soup.find_all('pre') 

data.pop(0); data.pop(-1)

# Both work
# data = soup.find_all('div', class_ = 'pbox1a')
