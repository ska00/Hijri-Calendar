"""
    Author: Salama Algaz
    Date: October 13, 2024

    Scrapes data from AstroPixels and writes to a readable csv file which is fed to 
    the main python program to compute the Hijri (Islamic) Calendar. The csv file contains
    the headers: datetime,phase,friendlydate.

    If you would like to include eclipse tags check out 'data_scraper_with_eclipses.py'

    This code does not handle errors that may pop up such as not being able to
    access the website.

    Issues with backtracking:
    1. The Julian calendar was in effect.
    2. 10 days were removed, 4 October 4, 1582 led to October 15, 1582
    3. After October 15, 1582 the Gregorian calendar was used.

    I believe the issues have been circumvented. I've used the convertdate package
    to convert Julian to Gregorian so as to be able to manipulate datetime objects and
    so that the dates are consistent. 

    The julian calendar must be converted to Gregorian before use.

    Code takes approxiamately 7.7 seconds to run on my PC.
"""

# ----------- Choose start year and end year (Gregorian) of the data to be read --------

START_YEAR = 601        # AD
END_YEAR = 2100         # AD


"""------------------ PACKAGES -------------------"""
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, timedelta
from convertdate import julian, gregorian
import csv
import pytz
import requests
import sys
import time

print("Packages imported successfully")


"""------------------ CONSTANTS -------------------"""

DATE_FORMAT = '%b %d %H:%M' 

ECLIPSES = [" T", " A", " H", " P", " t", " p", " n"]

HEADER = ['Year', 'New Moon', 'First Quarter', 'Full Moon', 'Last Quarter']

MONTH_ABB = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12 }

PHASE_HEADERS = {
    0 : "New Moon", 
    1: "First Quarter", 
    2:"Full Moon", 
    3:"Last Quarter" }


# This is to act as though a user is accessing the website
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}


"""------------------ FUNCTIONS-------------------"""

def get_page_content(url):
    """
        Scrapes data from a page on the wesbite 'astropixels.com'
        Returns a list of rows read from the table 'Phases of the Moon'
    """
    # Send a GET request to the webpage
    page = requests.get(url, headers=REQUEST_HEADERS)

    soup = BeautifulSoup(page.text, "html.parser")

    data = soup.find_all('pre') 

    # Remove first and last element
    data.pop(0); data.pop(-1)

    rows = []
    for entry in data:
        # Use StringIO to treat the string as a file
        csv_file = StringIO(entry.text)

        # Read the data using csv.reader
        reader = csv.reader(csv_file)
        rows += list(reader)

    print("Data scraped successfully")
    return rows


def write_to_csv(rows, filename):
    """
        Takes in a list of rows scraped from the table on the website, parses it and writes
        it to a csv file.
    """

    parsed_data = []    # A list of dicitonaries for the date and the moon phase
    year = 0            # The year the data belongs to

    for row in rows:
        # Ensure the row isn't empty
        if row != []:

            items = row[0].split("   ")
            new_items = []
            contains_year = False
            
            for i in items:
                # Ensure the string isn't empty
                if i.strip():   
                    i = i.strip()

                    if i[-2:] in ECLIPSES:    # Remove eclipse markings
                        i = i[:-2]

                    if i.isdigit():           # If it's a number then it's the year (do not add it to list)
                        year = int(i)
                        contains_year = True
                        continue

                    new_items.append(i)

            if new_items == HEADER: # Ignore headers
                continue

            length = len(new_items)
            moon_phase = 0

            if contains_year:
                # This depends at which position it appears in the table
                moon_phase = 4 - length   
                contains_year = False 
            
            for i in range(length):
                
                dictionary = {}

                # Parse the date
                date_list = new_items[i].split()
                month = MONTH_ABB[date_list[0]]
                day = int(date_list[1])
                hour, minute = date_list[2].split(":")
                hour = int(hour)
                minute = int(minute)

                # Julian calendar is used before Oct 15, 1582
                if year < 1582 or (year == 1582 and month < 10) or (year==1582 and month==10 and day<15):
                    
                    # print(f"Date {new_items[i]}, {year} is Julian")
                    julian_date = (year, month, day)
                    time = timedelta(hours=hour, minutes=minute)  # Time component

                    gregorian_date = julian.to_gregorian(*julian_date)
                    date = datetime(gregorian_date[0], gregorian_date[1], gregorian_date[2], tzinfo=pytz.utc) + time
                
                else:
                    # print(f"Date {new_items[i]}, {year} is Gregorian")
                    date = datetime(year, month, day, hour, minute, tzinfo=pytz.utc)

                # Add to dictionary
                dictionary["datetime"] = date.strftime('%Y-%m-%d %H:%M:%S')
                dictionary["phase"] = PHASE_HEADERS[moon_phase]
                dictionary["friendlydate"] = date.strftime("%B %d, %Y")

                parsed_data.append(dictionary)
                moon_phase += 1


    # Append to csv file
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        # Create a DictWriter object
        writer = csv.DictWriter(file, fieldnames = parsed_data[0].keys())

        # Write the data
        writer.writerows(parsed_data)

    print(f"Data written successfully\n")
    return


"""--------------------- MAIN --------------------"""
def main():

    filename = f'moon-phases-{START_YEAR}-to-{END_YEAR}-UT.csv'

    # Get pages that need to be scraped
    pages = [str(number).zfill(4) for number in range(START_YEAR, END_YEAR + 100, 100)]

    # Write header of file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        file.write("datetime,phase,friendlydate\n")

    for page in pages:
        print(f"\nCompiling date for the year: {page}")

        url = f"https://astropixels.com/ephemeris/phasescat/phases{page}.html"

        rows = get_page_content(url) 

        write_to_csv(rows, filename)
        
    print("Success")



if __name__ == "__main__":
    main()