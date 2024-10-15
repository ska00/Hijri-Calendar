'''
Author: Salama Algaz
Date: 10/11/2024

Timezone: Mecca
This code attempts to predict future full moons. 
Every 5 years and 30 years a day is added. Every 'e' a new month is added.

No pattern can be found either for the muharram month or the day being added.
Best way to know is to check with online calendar to determine whether there was a muharram month
and whether dhul hijjah was 30 days long or not. i do not agree with muharram being at 
the start of the month as that only adds more to an already unpredictable calendar.
The only thing left to do is to try to let the calendar begin a day after the full moon.

Data retrieved from https://www.somacon.com/p570.php and astropixels.com
'''


'''	--------- PACKAGES ------------ '''
import csv
import math
import pytz		# Changing to zoneinfo package will solve compatibility with other platforms
import sys
from datetime import datetime, timedelta

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

HIJRI_MONTHS = {
		1: "Safar I", 2: "Safar II", 3: "Rabi I\t", 
		4: "Rabi II", 5: "Jumada I", 6: "Jumada II",
		7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 
		10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hij."
		}

HIJRI_MONTHS_DAYCOUNT = get_number_of_days_in_month()

# This is the month that occassionally has an extra day, so Dhul Hijjah sometimes has 29 or 30 days
KABS_MONTH = 12

HIRJI_START_YEAR = 622 # AD

# Add the 13th month: Muharram
HIJRI_MONTHS[13] = "Muharram"
HIJRI_MONTHS_DAYCOUNT[13] = 30

MECCA_TIMEZONE = pytz.timezone('Asia/Riyadh')

SOLARYEAR_DAYS = 365.24219	# days


'''	-------- FUNCTIONS ------------ '''
def get_filename(start_year, end_year):
	for file in FILES:
		if file["start_year"] == start_year and file["end_year"] == end_year:
			return file["filename"]

	raise FileNotFoundError

def parse_file(start_year, end_year):
	""" Reads file, recording entries only when it's a full moon """

	filename = get_filename(start_year, end_year)

	entries = []
	with open(filename, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		entries = list(filter(is_fullmoon, reader))

	print("\nFile parsed successfully\n")
	return entries



'''	----------- MAIN -------------- '''

def main():

	'''	--------- VARIABLES ------------ '''
	start_year = 601
	end_year = 2100
	entries = parse_file(start_year, end_year)
	entries_length = len(entries)	

	lunar_days = 0
	lunar_days_off = 0
	lunar_year = 1
	month_count = 0 		# Which month, look to the constant HIJRI_MONTHS
	end_month = -1   		# Placeholder for the date of the end of the month

	kabs_running_small = 0
	kabs_running_large = 0
	muharram_running = 0


	for i in range(entries_length):

		# If loop starting get start of month from the observation of full moon
		if end_month == -1:
			start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT)

		# Exit if last year
		if start_month.year == end_year: 	
			break;

		# Get start and end of calendar month from Gregorian (True i.e. observed Full Moon)
		gregorian_start_month = datetime.strptime(entries[i]["datetime"], DATEFORMAT)
		gregorian_end_month = datetime.strptime(entries[i + 1]["datetime"], DATEFORMAT)


		# Only start after 622 AD
		if gregorian_start_month.year < HIRJI_START_YEAR:
			continue;


		# Adjust month count
		month_count += 1
		# Get end of calendar month
		end_month = start_month + timedelta(days = HIJRI_MONTHS_DAYCOUNT[month_count])

		# -------------------------------- TIMEZONE ------------------------------------
		# Assign UTC to naive timezone
		start_month.replace(tzinfo=pytz.utc)
		end_month.replace(tzinfo=pytz.utc)
		gregorian_start_month.replace(tzinfo=pytz.utc)
		gregorian_end_month.replace(tzinfo=pytz.utc)

		start_month = start_month.astimezone(MECCA_TIMEZONE)
		end_month = end_month.astimezone(MECCA_TIMEZONE)
		gregorian_start_month = gregorian_start_month.astimezone(MECCA_TIMEZONE)
		gregorian_end_month = gregorian_end_month.astimezone(MECCA_TIMEZONE)

		
		# Check difference from actual full moons
		if gregorian_end_month > end_month:
			lunar_days_off = (gregorian_end_month - end_month).days 
		else:
			lunar_days_off = (end_month - gregorian_end_month).days


		if lunar_days_off >= 2:
			print("\nTERMINATING PROGRAM: LUNAR DAYS MORE THAN TWO WHOLE DAYS OFF")
			print("\n[FAILURE] Computing Hijri Calendar\n")
			sys.exit(1)

		# Keep track of lunar days
		lunar_days += HIJRI_MONTHS_DAYCOUNT[month_count]

		print(HIJRI_MONTHS[month_count], HIJRI_MONTHS_DAYCOUNT[month_count])
		# Print the Gregorian date
		print(f"\tFull Moon Observed \t"+ 
			f"{gregorian_start_month.strftime('%B %d, %Y')} - {gregorian_end_month.strftime('%B %d, %Y')}")

		# Print the Lunar Calendar in Gregorian
		print(f"\tHijri (Gregorian) \t{start_month.strftime('%B %d, %Y')} - {end_month.strftime('%B %d, %Y')}")

		# Print Hijri calendar
		print(f"\tHijri (Natural): \t{HIJRI_MONTHS[month_count]} {1}, {lunar_year} - "
				+ f"{HIJRI_MONTHS[month_count]} {HIJRI_MONTHS_DAYCOUNT[month_count]}, {lunar_year}")
		print(f"\t\t\t\t\t\t\tDays off: {lunar_days_off}")
		print()


		# -------- END OF YEAR ---------
		if end_month.month == 1 and start_month.month != 1:

			if abs(SOLARYEAR_DAYS - lunar_days) > 30:
				print("\nTERMINATING PROGRAM: CALENDAR YEAR IS OFF FROM SOLAR YEAR BY MORE THAN 30 DAYS")
				print("\n[FAILURE] Computing Hijri Calendar\n")
				sys.exit(2)



			print(f"\n---------------------------- THE YEAR IS {end_month.year} ---------------------------\n")
			lunar_days = 0
			month_count = 0
			lunar_year += 1


			muharram_running += 1
			kabs_running_small += 1
			

			print(f"kabs_running_small : {kabs_running_small}, kabs_running_large: {kabs_running_large}")

			# if kabs_running_small == 4 and kabs_running_large == 29:
			# 	print("TERMINATE. CANT ADD TWO DAYS")
			# 	sys.exit()

			if kabs_running_small >= 5:
				kabs_running_large += 4 / 30
				kabs_running_small = -1 / 30
				HIJRI_MONTHS_DAYCOUNT[KABS_MONTH] = 30
				# kabs_running_small = -1 + kabs_running_large
				# if kabs_running_large >= 0.9:
				# 	kabs_running_large = 0
			# elif kabs_running_large == 29:
			# 	HIJRI_MONTHS_DAYCOUNT[KABS_MONTH] = 30
			# 	kabs_running_large = 0
			else:
				HIJRI_MONTHS_DAYCOUNT[KABS_MONTH] = 29




		# Go the next month
		start_month = end_month

	print("\n[SUCCESS] Computing Hijri Calendar\n")



'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()

