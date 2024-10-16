'''
Author: Salama Algaz
Date: 10/11/2024

I'm implementing a metonic cycle that's predictable here. This way given any year we know
if a leap month was added or not. This is a proof of concept

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
def get_number_of_days_in_month():
	d = {}
	for month_number in range(1, 12 + 1):
		d[month_number] = 30 if month_number % 2 == 1 else 29
	return d

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

# This is the month that occassionally has an extra day, so Dhul Hijjah sometimes has 29 or 30 days
KABS_MONTH = 12

HIJRI_MONTHS = {
		1: "Safar I", 2: "Safar II", 3: "Rabi I\t", 
		4: "Rabi II", 5: "Jumada I", 6: "Jumada II",
		7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 
		10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hij."
		}

HIJRI_MONTHS_DAYCOUNT = get_number_of_days_in_month()

HIRJI_START_YEAR = 622 # AD

# Add the 13th month: Muharram
HIJRI_MONTHS[13] = "Muharram"  		# Muharram is placed at end of year
HIJRI_MONTHS_DAYCOUNT[13] = 30
HIJRI_MONTHS[0] = "Muharram"  		# Muharram is placed at start of year
HIJRI_MONTHS_DAYCOUNT[0] = 30

MUHARRAM_YEARS = [3, 6, 8, 11, 14, 17, 19] #[1, 4, 6, 9, 12, 15, 17]
KABS_MONTHS = [8, 12]

MECCA_TIMEZONE = pytz.timezone('Asia/Riyadh')

"""
***************** PLEASE READ ************:
This limit is somewhat arbitrary. Change this as you see fit. I recommend a value from 0 to 0.5.

If the hirji calendar day is behind the full moon (gregorian) date by 0.1 days, the code will add an 
extra day in dhul hijjah. You'll notice, though, that I do not add an extra day even if the value 
falls under the limit if the year includes the Muharram month. This is because Muharram typically 
readjusts the hijri calendar to the Gregorian calendar in which adding the day actually overshoots 
the Hijri calendar.
"""
LIMIT_LUNAR_DAYS_OFF = 0.1 

SOLARYEAR_DAYS = 365.24219	# days


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

	'''	--------- VARIABLES ------------ '''
	start_year = 601
	end_year = 2100
	# entries = parse_file(start_year, end_year)
	entries = parse_file_with_eclipses(start_year, end_year)
	entries_length = len(entries)

	end_month = -1   		# Placeholder for the date of the end of the month
	hirji_year = 1  		# Hirji year
	lunar_days = 0   		# Number of days in the Hirji Calendar
	month_count = 0 		# Which month we're in, look at 'HIJRI_MONTHS'
	is_muharram = False


	for i in range(entries_length):

		# If loop just started set start of month to Gregorian full moon date.
		if end_month == -1:
			start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT) + timedelta(days = 1)


		# Get start and end of calendar month from Gregorian (True i.e. observed Full Moon)
		gregorian_start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT)
		gregorian_end_month = datetime.strptime(entries[i + 1]["datetime"], DATEFORMAT)


		# Hijri Calendar only exists at and after 622 AD
		if gregorian_start_month.year < HIRJI_START_YEAR:
			continue;

		# Add month count
		month_count += 1
		# Get end of calendar month
		end_month = start_month + timedelta(days = HIJRI_MONTHS_DAYCOUNT[month_count])

		
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


		days_off = (gregorian_end_month.replace(hour = 0, minute = 0, second = 0) -
					end_month.replace(hour = 0, minute = 0, second = 0)).days
			

		# Adjust length of the month accordingly if it's KABS month
		if days_off >= 1 and not is_muharram and month_count == KABS_MONTH:
			end_month += timedelta(days = 1)			# Add a day to the end of the month
			HIJRI_MONTHS_DAYCOUNT[month_count] = 30
		elif month_count in KABS_MONTHS:
			HIJRI_MONTHS_DAYCOUNT[month_count] = 29


		if days_off > 3 or days_off < -3:
			print("\nTERMINATING PROGRAM: LUNAR DAYS MORE THAN THREE WHOLE DAYS OFF")
			print(f"\nLUNAR DAYS OFF: {lunar_days_off}")
			print("\n[FAILURE] Computing Hijri Calendar\n")
			sys.exit(1)


		# Keep track of lunar days
		lunar_days += HIJRI_MONTHS_DAYCOUNT[month_count]

		# Print Hijri Month
		print(f"{HIJRI_MONTHS[month_count]} {HIJRI_MONTHS_DAYCOUNT[month_count]} \t\t\t\t\t\t\t\t\t\t\t\t\t\t{entries[i]['eclipse']}")

		# Print the Gregorian date
		print(f"\tFull Moon Observed: "+ 
			f"{gregorian_start_month.strftime('%B %d, %Y')} - {(gregorian_end_month - timedelta(days=1)).strftime('%B %d, %Y')}")

		# Print the Hirji Calendar in Gregorian
		print(f"\tHijri (Gregorian) \t{start_month.strftime('%B %d, %Y')} - {(end_month - timedelta(days=1)).strftime('%B %d, %Y')}")

		# Print Hijri calendar Natural
		print(f"\tHijri (Natural): \t{HIJRI_MONTHS[month_count]} {1}, {hirji_year} - "
				+ f"{HIJRI_MONTHS[month_count]} {HIJRI_MONTHS_DAYCOUNT[month_count]}, {hirji_year}")
		
		print("\t\t\t\t\t\tDays off:", days_off)
		print()


		# -------- END OF YEAR ---------
		if (month_count == 12 and not is_muharram) or month_count == 13:

			# Check deviation of Hijri year (in days) from solar year
			if abs(SOLARYEAR_DAYS - lunar_days) > 30:
				print("\nTERMINATING PROGRAM: HIRJI YEAR IS OFF FROM SOLAR YEAR BY MORE THAN 30 DAYS")
				print("\nDIFFERENCE:", abs(SOLARYEAR_DAYS - lunar_days))
				print("\n[FAILURE] Computing Hijri Calendar\n")

				sys.exit(2)

			upcoming_year = end_month.year

			# Exit if last year
			if upcoming_year == end_year: 	
				break;

			print(f"\n------------------------------- THE YEAR IS {hirji_year + 1} ------------------------------\n")
				

			hirji_year += 1
			lunar_days  = 0
			month_count = 0

			is_muharram = hirji_year % 19 in MUHARRAM_YEARS

			# For debugging purposes
			print(f"Is Leap Year:", is_muharram); print()

		# Go the next month
		start_month = end_month


	print("\n[SUCCESS] Computing Hijri Calendar\n")



'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()