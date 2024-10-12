'''
Author: Salama Algaz
Date: 10/11/2024



Data retrieved from https://www.somacon.com/p570.php
'''


'''	--------- PACKAGES ------------ '''
import csv
import sys
from datetime import datetime


'''	--------- CONSTANTS ------------ '''
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

FILES = { 
		1980: "moon-phases-1980-to-2077-UTC.csv",
		1900: "moon-phases-1900-to-2100-UTC.csv",
		2023: "moon_data_2023-24.csv",
		2027: "moon-phases-2024-to-2027-UTC.csv"
		}

AVG_SYNODIC_MONTH = 29 + 12 / 24 + (44/60 / 24)	# (units: days) 29 days, 12 hours, 44 minutes


'''	-------- FUNCTIONS ------------ '''
def is_fullmoon(row):
	return row["phase"] == "Full Moon"


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
	filename = FILES[2027]
	fullmoon_dates, num_entries = parse_file(filename)


	for i in range(num_entries):

		# Check if last entry and exit, otherwise an error will occur due to accessing out of bounds of list
		if i == num_entries - 1:
			continue;


		current_row = fullmoon_dates[i]
		next_row = fullmoon_dates[i + 1]

		current_date = datetime.strptime(current_row["datetime"], DATEFORMAT)

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


