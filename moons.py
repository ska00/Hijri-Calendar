'''
Author: Salama Algaz
Date: 10/11/2024



Data retrieved from https://www.somacon.com/p570.php
'''


'''	--------- PACKAGES ------------ '''
import csv
import sys
from datetime import datetime, timedelta

'''	--------- UTILITIES ------------ '''
def month_days():
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
		1700: "moon-phases-1700-to-2100-UTC.csv",
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
			7: "Rajab\t", 8: "Sha'ban", 9: "Ramadan", 10: "Shawwal", 11: "Dhul Hijjah", 12: "Dhul Qadah", 13: "Muharram"}

MONTHS_DAYSCOUNT = month_days()

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



'''	----------- MAIN -------------- '''
def main():

	'''	--------- VARIABLES ------------ '''
	days_off = 0
	day_offset = 0
	days_count = 0
	difference_lunar = 0
	lunar_year = 2024
	lunar_days = 0
	filename = FILES[2055]
	fullmoon_dates, num_entries = parse_file(filename)
	fullmoon_count = 0
	final_year = datetime.strptime(fullmoon_dates[-1]["datetime"], DATEFORMAT).year
	est_next_date = -1

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

		
		# Keep count of how many full moons
		fullmoon_count += 1

		



		if fullmoon_count == 13 and MONTHS_DAYSCOUNT[2] == 30:
			days_count = 385
		elif fullmoon_count == 13 and MONTHS_DAYSCOUNT[2] == 29:
			days_count = 384
		else:
			days_count += MONTHS_DAYSCOUNT[now_date.month]

		




		m = now_date + timedelta(days=MONTHS_DAYSCOUNT[fullmoon_count])
		# days_off += m - now_date
		est_next_date = m

		now_date_gregorian = datetime.strptime(fullmoon_dates[i]["datetime"], DATEFORMAT)

		l = next_date - now_date_gregorian
		lunar_days += l.total_seconds() / (24 * 3600)

		time_difference = next_date - now_date_gregorian
		days_difference = time_difference.total_seconds() / (24 * 3600)	# Between two fullmoons
		# days_off += days_difference - MONTHS_DAYSCOUNT[now_date.month]


		print(f"{MONTHS[fullmoon_count]} \t {MONTHS_DAYSCOUNT[fullmoon_count]} \t" + 
			f"{fullmoon_dates[i]["friendlydate"]} - {next_row["friendlydate"]}") #\t{round(days_difference, 3)}

		
		print(f"\t\t\t\t{now_date.strftime("%B %d, %Y")} - {m.strftime("%B %d, %Y")}")





		day_offset = 0

		if next_date.month == 1 and now_date_gregorian.month != next_date.month:
			
			difference_lunar += SOLARYEAR - days_count
			lunar_year += 1

			days_off += lunar_days - days_count
			
			print("\ndays_off", days_off)
			print("Number of fullmoons:", fullmoon_count)
			print(f"Solar year: {SOLARYEAR}")
			print(f"Lunar year: {days_count}")
			print("Difference:", difference_lunar)
			print("The year is", lunar_year); print()

			
			# For next year
			if days_off >= 0.9:
				MONTHS_DAYSCOUNT[2] = 30
				MONTHS_DAYSCOUNT[3] = 30
			elif days_off <= -0.9:
				MONTHS_DAYSCOUNT[3] = 29
				MONTHS_DAYSCOUNT[2] = 29
			else:
				MONTHS_DAYSCOUNT[2] = 29
				MONTHS_DAYSCOUNT[3] = 30
			


			fullmoon_count = 0
			days_count = 0
			lunar_days = 0



'''	----------- MAIN -------------- '''
def main_backup():

	'''	--------- VARIABLES ------------ '''
	days_off = 0
	day_offset = 0
	days_count = 0
	difference_lunar = 0
	lunar_year = 2024
	filename = FILES[2027]
	fullmoon_dates, num_entries = parse_file(filename)
	fullmoon_count = 0
	final_year = datetime.strptime(fullmoon_dates[-1]["datetime"], DATEFORMAT).year

	for i in range(num_entries):

		now_row = fullmoon_dates[i]
		next_row = fullmoon_dates[i + 1]

		now_date = datetime.strptime(now_row["datetime"], DATEFORMAT)
		next_date = datetime.strptime(next_row["datetime"], DATEFORMAT)

		# Exit if last year
		if now_date.year == final_year:
			break;

		time_difference = next_date - now_date
		days_difference = time_difference.total_seconds() / (24 * 3600)	# Between two fullmoons

		# Keep count of how many full moons
		fullmoon_count += 1

		days_count += MONTHS_DAYSCOUNT[now_date.month]

		days_off += days_difference - MONTHS_DAYSCOUNT[now_date.month]


		print(f"{MONTHS[fullmoon_count]} \t {MONTHS_DAYSCOUNT[fullmoon_count] + day_offset} \t" + 
			f"{now_row["friendlydate"]} - {next_row["friendlydate"]}") #\t{round(days_difference, 3)}

		m = now_date + timedelta(days=MONTHS_DAYSCOUNT[fullmoon_count])
		print(f"\t\t\t{now_row["friendlydate"]} - {m.strftime("%B %d, %Y")}")

		day_offset = 0

		if next_date.month == 1 and now_date.month != next_date.month:
			
			difference_lunar += SOLARYEAR - days_count
			lunar_year += 1
			
			print("\ndays_off", days_off)
			print(f"Solar year: {SOLARYEAR}")
			print(f"Lunar year: {days_count}")
			print("Difference:", difference_lunar)
			print("The year is", lunar_year); print()

			# For next year
			if days_off > 1:
				MONTHS_DAYSCOUNT[2] = 30
			else:
				MONTHS_DAYSCOUNT[2] = 29

			fullmoon_count = 0
			days_count = 0




'''	------- EXECUTE MAIN ---------- '''
if __name__ == "__main__":
	main()
	sys.exit()


days = 0
num_fullmoons = 0







months_fullmoon = {}
months = []

leftover_days = 0
lowest = 10;
highest = 0








for i in range(length_of_fullmoons):

	row = fullmoons[i]

	date = row["datetime"]

	current_fullmoon = datetime.strptime(row["datetime"], DATEFORMAT)

	if i == 0:
		#print(f"{current_fullmoon}")
		num_fullmoons = 1
		continue;

	previous_row = fullmoons[i - 1]

	current_year = current_fullmoon.year

	previous_fullmoon = datetime.strptime(previous_row["datetime"], DATEFORMAT)

	previous_year = previous_fullmoon.year

	delta = current_fullmoon - previous_fullmoon

	total_days = delta.total_seconds() / (24 * 3600)

	if current_fullmoon.month == previous_fullmoon.month:
		if not current_fullmoon.month in months_fullmoon:
			months_fullmoon[current_fullmoon.month] = 1
		else:
			months_fullmoon[current_fullmoon.month] += 1

		months.append(f"Month: {current_fullmoon.month}, Year: {current_year}")


	
	if current_year != previous_year:
		print()
		print("Total days:", days)
		print(f"Number of full moons in {current_year}: {num_fullmoons}")
		print("Mean Synodic Month:", mean_synodic_month)
		print()

		# if leftover_days < lowest: lowest = leftover_days
		# if leftover_days > highest: highest = leftover_days

		leftover_days += days - mean_synodic_month * 12

		days = 0
		num_fullmoons = 0
		# leftover_days = 0

	# Check here if 13 fullmoons happen
	num_fullmoons += 1
	# Get the remainder
	leftover_days += total_days - mean_synodic_month


	

	if current_fullmoon.month % 2 == 0:
		days += 29
		print(f"{previous_fullmoon} - {current_fullmoon} , {29} days")
		# print("Leftover days:", leftover_days)
		print()
	else:
		days += 30
		print(f"{previous_fullmoon} - {current_fullmoon} , {30} days")
		# print("Leftover days:", leftover_days)
		print()

	# leftover_days += total_days - mean_synodic_month

	
	# if total_days > mean_synodic_month:
	# 	days += 30
	# 	print(f"{previous_fullmoon} - {current_fullmoon} , 30 days")
	# else:
	# 	days += 29
	# 	print(f"{previous_fullmoon} - {current_fullmoon}  , 29 days")


print()
print("Total days:", days)
print(f"Number of full moons in {current_year}: {num_fullmoons}")
print("leftover_days: ", leftover_days)
# print("Highest LEftover", highest)
# print("lowest leftover:", lowest)
print()


# for month in months:
# 	print(month)

# print(months_fullmoon)


#filename = "moon_data_2023-24.csv"

#months_fullmoon = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0,
#					"May": 0, "Jun": 0, "Jul": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}


