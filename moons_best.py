'''
Author: Salama Algaz
Date: 10/11/2024


If Next year is going to be off we need to remove a day off in that year rather than waiting
for next year to implement it. Code needs to be rewritten so the code is more efficient. 
For example, backtracking rather than getting a future estimate is faster.
Also, using 'e' as an estimate of when to put muharram rather than on physical observations, and 5.167
(this number is based on observations made from full moon data) years to add a day. 
Further data analysis can be made on the pattern to be observed of when the days are added.
Instead of depending on a crude average, the years can be clustered and rules can be derived, that is
if a pattern could be found.

Data retrieved from https://www.somacon.com/p570.php and astropixels.com
'''


'''	--------- PACKAGES ------------ '''
import csv
import math
import sys
from datetime import datetime, timedelta

'''	--------- UTILITIES ------------ '''
def get_month_daycounts():
	d = {}
	for i in range(1, 12 + 1):
		d[i] = 30 if i % 2 == 1 else 29
	return d

def is_fullmoon(row):
	return row["phase"] == "Full Moon"


'''	--------- CONSTANTS ------------ '''

AVG_SYNODIC_MONTH = 29 + 12 / 24 + (44/60 / 24)	# (units: days) 29 days, 12 hours, 44 minutes. 29.530594 days

DATEFORMAT = "%Y-%m-%d %H:%M:%S"

FILES = { 
		601: "moon-phases-601-to-2001-UT.csv",
		# 1700: "moon-phases-1700-to-2100-UTC.csv",
		1980: "moon-phases-1980-to-2077-UTC.csv",
		1900: "moon-phases-1900-to-2100-UTC.csv",
		1902: "moon-phases-1902-to-1998-UTC.csv",
		2023: "moon-phases-2023-to-2024-UTC.csv",
		2027: "moon-phases-2024-to-2027-UTC.csv",
		2040: "moon-phases-2024-to-2040-UTC.csv",
		2044: "moon-phases-2024-to-2044-UTC.csv",
		2055: "moon-phases-2024-to-2055-UTC.csv",
		}

MONTHS = {1: "Safar I", 2: "Safar II", 3: "Rabi I\t", 4: "Rabi II", 5: "Jumada I", 6: "Jumada II",
			7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 10: "Shawwal", 11: "Dhul Qadah", 12: "Dhul Hijjah", 13: "Muharram"}

MONTHS_DAYSCOUNT = get_month_daycounts()

CHANGING_MONTH = 12

HIRJI_STARTING_YEAR = 622

# Muharram
MONTHS_DAYSCOUNT[13] = 30

SOLARYEAR = 365.24219


'''	-------- FUNCTIONS ------------ '''
def parse_file(file):
	""" Returns list of data entries in which there was a full moon """
	fullmoon_dates = []
	with open(file, "r") as csvfile:
		reader = csv.DictReader(csvfile)
		fullmoon_dates = list(filter(is_fullmoon, reader))

	return fullmoon_dates, len(fullmoon_dates)

def year_contains_muharram(year, fullmoon_dates):
	def is_year(entry):
		entry_year = datetime.strptime(entry["datetime"], DATEFORMAT).year
		return entry_year == year
	# Count how many full moons and return true if 13
	dates_in_year = list(filter(is_year, fullmoon_dates))
	return len(dates_in_year) == 13




'''	----------- MAIN -------------- '''
def main():

	'''	--------- VARIABLES ------------ '''
	days_added = 0
	months_added = 0
	days_off = 0
	day_offset = 0
	days_count = 0
	difference_lunar = 0
	lunar_year = 0
	lunar_days = 0
	filename = FILES[601]
	fullmoon_dates, num_entries = parse_file(filename)
	fullmoon_count = 0
	final_year = datetime.strptime(fullmoon_dates[-1]["datetime"], DATEFORMAT).year
	est_next_date = -1
	e = math.e
	running_years = 0
	running_days = 0
	every_other_muharram = False
	days_added_dict = {}	# NULL

	days_added_list = []
	order = 1

	for i in range(num_entries):

		now_date = est_next_date

		if est_next_date == -1:
			now_row = fullmoon_dates[i]
			now_date = datetime.strptime(now_row["datetime"], DATEFORMAT)
		
		next_row = fullmoon_dates[i + 1]
		next_date = datetime.strptime(next_row["datetime"], DATEFORMAT)

		# Exit if last year
		if now_date.year == final_year:
			break;

		if now_date.year < HIRJI_STARTING_YEAR:
			continue;

		
		# Keep count of how many full moons
		fullmoon_count += 1


		if fullmoon_count == 13 and MONTHS_DAYSCOUNT[CHANGING_MONTH] == 30:
			days_count = 385
		elif fullmoon_count == 13 and MONTHS_DAYSCOUNT[CHANGING_MONTH] == 29:
			days_count = 384
		else:
			days_count += MONTHS_DAYSCOUNT[now_date.month]



		m = now_date + timedelta(days=MONTHS_DAYSCOUNT[fullmoon_count])
		# days_off += m - now_date
		est_next_date = m

		now_date_gregorian = datetime.strptime(fullmoon_dates[i]["datetime"], DATEFORMAT)

		l = next_date - now_date_gregorian
		lunar_days += l.total_seconds() / (24 * 3600)

		if (now_date_gregorian - now_date).days >= 4 or (now_date - now_date_gregorian).days >= 4:
			print("Greater than 3 days difference!")
			break


		time_difference = next_date - now_date_gregorian
		days_difference = time_difference.total_seconds() / (24 * 3600)	# Between two fullmoons
		# days_off += days_difference - MONTHS_DAYSCOUNT[now_date.month]


		print(f"{MONTHS[fullmoon_count]} \t {MONTHS_DAYSCOUNT[fullmoon_count]} \t"+ 
			f"{fullmoon_dates[i]['friendlydate']} - {next_row['friendlydate']}") #\t{round(days_difference, 3)}

		
		print(f"\t\t\t\t{now_date.strftime('%B %d, %Y')} - {m.strftime('%B %d, %Y')}")





		day_offset = 0

		if next_date.month == 1 and now_date_gregorian.month != next_date.month:
			
			difference_lunar += SOLARYEAR - days_count

			if abs(difference_lunar) > 30:
				print("Deviated from solar!")
			lunar_year += 1

			days_off += lunar_days - days_count

			running_days += days_count

			running_years_sol = float(running_days) / SOLARYEAR

			running_years += 1
			# Count years in solar days!
			# running_years = running_years_sol
			
			print("\ndays_off", days_off)
			print("Number of fullmoons:", fullmoon_count)
			print(f"Solar year: {SOLARYEAR}")
			print(f"Lunar year: {days_count}")
			print("Difference:", difference_lunar)
			print("The year is", lunar_year); print()

			print(days_added_dict); print()

			print("running_years", running_years)
			print("e", e)
			# print(year_contains_muharram(lunar_year, fullmoon_dates))
			print()

			# is_muharram_next_year = year_contains_muharram(lunar_year, fullmoon_dates)

			

			# if is_muharram_next_year and not every_other_muharram:
			# 	every_other_muharram = True
			# 	e += math.e
			# # Need to anticipate
			# if float(running_days + SOLARYEAR) / SOLARYEAR + 1 > e :
			# 	if is_muharram_next_year and every_other_muharram or not every_other_muharram:
			# 		days_added += 1 
			# 		MONTHS_DAYSCOUNT[CHANGING_MONTH] = 30
			# 		e = math.e + (float(running_days + SOLARYEAR) / SOLARYEAR - e)
			# 		running_years = 0
			# 		running_days = 0
			# 		every_other_muharram = False
			# else:
			# 	MONTHS_DAYSCOUNT[CHANGING_MONTH] = 29
			# if is_muharram_next_year:
			# 	running_years -= 1
			# if running_years + 1 > e :
			# 	# if not is_muharram_next_year:
			# 	days_added += 1
			# 	e = math.e + (running_years +1 - e)
			# 	running_years = 0
			# 	running_days = 0
			# 	MONTHS_DAYSCOUNT[CHANGING_MONTH] = 30
			# else:
			# 	MONTHS_DAYSCOUNT[CHANGING_MONTH] = 29

			# For next year
			if days_off >= 0.9:
				days_added += 1
				days_added_list.append({"Order": order, "Year": lunar_year, "Interval (years)": running_years, "Muharram": fullmoon_count == 13})
				order += 1
				try:
					days_added_dict[running_years] += 1	
				except KeyError:
					days_added_dict[running_years] = 1
				running_years = 0
				MONTHS_DAYSCOUNT[CHANGING_MONTH] = 30
				MONTHS_DAYSCOUNT[3] = 30
			# elif days_off <= -0.9:
			# 	sys.exit()
			# 	days_added -= 1
			# 	MONTHS_DAYSCOUNT[3] = 29
			# 	MONTHS_DAYSCOUNT[CHANGING_MONTH] = 29
			else:
				MONTHS_DAYSCOUNT[CHANGING_MONTH] = 29
				MONTHS_DAYSCOUNT[3] = 30

			if fullmoon_count == 13:
				months_added += 1

			
			fullmoon_count = 0
			days_count = 0
			lunar_days = 0

	print("number of days addded:", days_added)
	print("Number of months added:", months_added)

	# Write to csv file
	with open("Days_added_601.csv", mode='w', newline='', encoding='utf-8') as file:
        # Create a DictWriter object
		writer = csv.DictWriter(file, fieldnames = days_added_list[0].keys())

		writer.writeheader()

        # Write the data
		writer.writerows(days_added_list)

	print(f"Data written successfully\n")





'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()
