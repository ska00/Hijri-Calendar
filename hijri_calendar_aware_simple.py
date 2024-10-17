'''
Author: Salama Algaz
Date: 10/11/2024

This the observation-based Hijri calendar. The days of each month vary each year in an unpredictable way.
However, each month always starts 1 day after the full moon occurs. Ramadan is sometimes 29 or 30 days.
This is identical to the Islamic calendar with the exception of adding a 13th month occasionally.

Note: 
The data on Astropixels.com has one error where the year 3869 has two januarys. I manually had to change
the year of the second January to 3870. Keep this in mind when using the data_scraper_with_eclipses.py file

Note:
The data used is in UTC/UT timezone, however the output displays 
the dates in AST timezone which is the timezone of Mecca, Saudi Arabia. 

Credits:
Some tables retrieved from https://www.somacon.com/p570.php
Moon Phases Table courtesy of Fred Espenak, www.Astropixels.com. Thank you Fred!
'''


'''	--------- PACKAGES ------------ '''
import csv
import math
import pytz
import sys
from datetime import datetime, timedelta


print("Packages imported successfully")


'''	--------- UTILITIES ------------ '''

def is_fullmoon(row):
	return row["phase"] == "Full Moon"


'''	--------- CONSTANTS ------------ '''

AVG_SYNODIC_MONTH = 29 + 12 / 24 + (44/60 / 24)	# 29 days, 12 hours, 44 minutes -> 29.530594 days

DATEFORMAT = "%Y-%m-%d %H:%M:%S"

FILES = [ 
		{"start_year":  601, "end_year": 2100, "filename": "moon-phases-601-to-2100-UT.csv"},
		{"start_year": 1900, "end_year": 2100, "filename": "moon-phases-1900-to-2100-UTC.csv"},
		{"start_year": 1902, "end_year": 1998, "filename": "moon-phases-1902-to-1998-UTC.csv"},
		{"start_year": 1980, "end_year": 2077, "filename": "moon-phases-1980-to-2077-UTC.csv"},
		{"start_year": 2023, "end_year": 2024, "filename": "moon-phases-2023-to-2024-UTC.csv"},
		{"start_year": 2024, "end_year": 2027, "filename": "moon-phases-2024-to-2027-UTC.csv"},
		{"start_year": 2024, "end_year": 2040, "filename": "moon-phases-2024-to-2040-UTC.csv"},
		{"start_year": 2024, "end_year": 2044, "filename": "moon-phases-2024-to-2044-UTC.csv"},
		{"start_year": 2024, "end_year": 2055, "filename": "moon-phases-2024-to-2055-UTC.csv"},
		]

FILES_W_ECLIPSES = [
		{"start_year":  601, "end_year": 700, "filename": "moon-phases-601-to-700-with-eclipses-UT.csv"},
		{"start_year":  601, "end_year": 2100, "filename": "moon-phases-601-to-2100-with-eclipses-UT.csv"},
		{"start_year":  601, "end_year": 4000, "filename": "moon-phases-601-to-4000-with-eclipses-UT.csv"},
		]

<<<<<<< Updated upstream
HIJRI_MONTHS = {0: "Muharram",
=======
HIJRI_MONTHS = { 0: "Muharram",
>>>>>>> Stashed changes
		1: "Safar I", 2: "Safar II", 3: "Rabi I\t", 
		4: "Rabi II", 5: "Jumada I", 6: "Jumada II",
		7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 
		10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hij."
		}

HIRJI_START_YEAR = 622 # AD

# Add the 13th month: Muharram
HIJRI_MONTHS[13] = "Muharram"  		# Muharram is placed at end of year

MUHARRAM_YEARS = [3, 6, 8, 11, 14, 17, 19] #[1, 4, 6, 9, 12, 15, 17]

MECCA_TIMEZONE = pytz.timezone('Asia/Riyadh')


'''	-------- FUNCTIONS ------------ '''
def get_filename(start_year, end_year, contains_eclipse = False):
	""" Returns filename of the csv file with the given starting and ending year """
	
	_files = FILES_W_ECLIPSES if contains_eclipse else FILES

	for file in _files:
		if file["start_year"] == start_year and file["end_year"] == end_year:
			return file["filename"]

	raise FileNotFoundError

def parse_file(start_year, end_year):
	""" Reads file, recording entries only when it's a full moon """

	filename = "Moon phases CSV files/" + get_filename(start_year, end_year)

	entries = []
	with open(filename, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		entries = list(filter(is_fullmoon, reader))

	print("\nFile parsed successfully\n")
	return entries

def parse_file_with_eclipses(start_year, end_year):
	""" Reads file, recording entries only when it's a full moon """

	filename = "Moon phases CSV files w eclipses/" + get_filename(start_year, end_year, True)

	entries = []
	eclipses = []

	with open(filename, "r") as csvfile:
		
		reader = csv.DictReader(csvfile)
		for row in reader:
			
			if row["phase"] != "Full Moon":
				if eclipse := row["eclipse"]:
					eclipses.append(eclipse)
				continue

			if eclipses != []:
				if entries[-1]["eclipse"] == "":
					entries[-1]["eclipse"] = ", ".join(eclipses)
				else:
					entries[-1]["eclipse"] = entries[-1]["eclipse"] + ", " + ", ".join(eclipses)
				eclipses = []
			
			entries.append(row)

			
	print("\nFile parsed successfully\n")
	return entries


'''	----------- MAIN -------------- '''

def main():

	'''	--------- GLOBALS* (*not really..) ------------ '''
	start_year = 601
	end_year = 4000
	# entries = parse_file(start_year, end_year)
	entries = parse_file_with_eclipses(start_year, end_year)
	entries_length = len(entries)


	def get_muharram_position(index, year):
		"""
			This checks if the given year contains a blue moon (or 13 full moons) and returns
			the position (1) if the blue moon occurs in the months 1 - 6 inclusive, 13 if in the 
			months 7 - 12 inclusive. Otherwise, if there is no Muharram month it will return -1.

			Note: This is defined within main so that it can access the variable 'entries'.
				It is not ideal to nest this function within main but it is less ideal to pass in the 
				large list 'entries'. It significantly slows down the program.
		"""
		_month_count = 1
		_index = index

		while(_month_count < 14):
			try:
				_start_month = datetime.strptime(entries[_index]["datetime"], DATEFORMAT).month
				_end_month = datetime.strptime(entries[_index + 1]["datetime"], DATEFORMAT).month
				_year = datetime.strptime(entries[_index]["datetime"], DATEFORMAT).year
			except:
				return -1

			if _year > year:
				return -1

			if _start_month == _end_month:
				return 1 if _month_count <= 6 else 13

			_month_count += 1
			_index += 1

		return -1	


	'''	--------- VARIABLES ------------ '''

	hijri_month_lens = {29: 0, 30: 0}
	hirji_year = 1  					# Hirji year
	month_count = 0 					# Which month we're in, look at 'HIJRI_MONTHS'
	muharram_position = -1  			# The position the month 'Muharram' falls into


	for i in range(entries_length):

		# If loop just started set start of month to Gregorian full moon date.
		start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT) + timedelta(days = 1)
		end_month = datetime.strptime(entries[i + 1]["datetime"], DATEFORMAT)

		start_month.replace(hour = 0, minute = 0, second = 0)
		end_month.replace(hour = 0, minute = 0, second = 0)

		# Get start and end of calendar month from Gregorian (True i.e. observed Full Moon)
		gregorian_start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT)
		gregorian_end_month = datetime.strptime(entries[i + 1]["datetime"], DATEFORMAT)


		# Hijri Calendar only exists at and after 622 AD
		if start_month.year < HIRJI_START_YEAR:
			continue;

		# Add month count
		month_count += 1

		
		# -------------------------------- TIMEZONE ------------------------------------
		# Assign UTC to naive datetime objects
		start_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		end_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		gregorian_start_month.replace(tzinfo=pytz.utc).astimezone(MECCA_TIMEZONE)
		gregorian_end_month.replace(tzinfo=pytz.utc)

		# Convert to MECCA time zone
		start_month = start_month.astimezone(MECCA_TIMEZONE)
		end_month = end_month.astimezone(MECCA_TIMEZONE)
		gregorian_start_month = gregorian_start_month.astimezone(MECCA_TIMEZONE)
		gregorian_end_month = gregorian_end_month.astimezone(MECCA_TIMEZONE)

		

		# Length of hirji month
		hijri_month_len = round((end_month - start_month).total_seconds() / (24* 3600)) + 1
		hijri_month_lens[hijri_month_len] += 1

		# Print Hijri Month
		print(f"{HIJRI_MONTHS[month_count]} {hijri_month_len}")

		# Print the Gregorian date
		print(f"\tFull Moon Observed: "+ 
			f"{gregorian_start_month.strftime('%B %d, %Y')} - {gregorian_end_month.strftime('%B %d, %Y')}")

		# Print the Hirji Calendar in Gregorian
		print(f"\tHijri (Gregorian) \t{start_month.strftime('%B %d, %Y')} - {end_month.strftime('%B %d, %Y')}")

		# Print Hijri calendar Natural
		print(f"\tHijri (Natural): \t{HIJRI_MONTHS[month_count]} {1}, {hirji_year} - "
				+ f"{HIJRI_MONTHS[month_count]} {hijri_month_len}, {hirji_year}")
		
		print()


		# -------- END OF YEAR ---------
		if (end_month.month == 1 and start_month.month != 1) or month_count == 13:

			upcoming_year = end_month.year

			# Exit if last year
			if upcoming_year == end_year: 	
				break;

			print(f"Number of months with 29 days: {hijri_month_lens[29]}, Number of months with 30 days: {hijri_month_lens[30]}")

			print(f"\n------------------------------- THE YEAR IS {upcoming_year} ------------------------------\n")
				
			hijri_month_lens = {29: 0, 30: 0}
			hirji_year += 1
			month_count = 0
			muharram_position = get_muharram_position(i, upcoming_year)

			# If Muharram is beginning of year shift all the months down
			if muharram_position == 1:
				month_count = -1

			# For debugging purposes
			print(f"Muharram position:", muharram_position); print()


	print("\n[SUCCESS] Computing Hijri Calendar (Simple)\n")



'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()

