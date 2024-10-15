

def main_old():

	'''	--------- VARIABLES ------------ '''
	days_added = 0
	months_added = 0
	days_off = 0
	day_offset = 0
	days_count = 0
	difference_lunar = 0
	lunar_year = 0
	lunar_days = 0
	est_next_date = 0

	entries = parse_file(2023, 2024)
	entries_length = len(entries)
	fullmoon_count = 0
	final_year = datetime.strptime(entries[-1]["datetime"], DATEFORMAT).year
	e = math.e
	running_years = 0
	running_days = 0
	every_other_muharram = False
	days_added_dict = {}	# NULL

	days_added_list = []
	order = 1

	for i in range(entries_length):

		now_date = est_next_date

		if est_next_date == -1:
			now_row = entries[i]
			now_date = datetime.strptime(now_row["datetime"], DATEFORMAT)
		
		next_row = entries[i + 1]
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

		now_date_gregorian = datetime.strptime(entries[i]["datetime"], DATEFORMAT)

		l = next_date - now_date_gregorian
		lunar_days += l.total_seconds() / (24 * 3600)

		if (now_date_gregorian - now_date).days >= 4 or (now_date - now_date_gregorian).days >= 4:
			print("Greater than 3 days difference!")
			break


		time_difference = next_date - now_date_gregorian
		days_difference = time_difference.total_seconds() / (24 * 3600)	# Between two fullmoons
		# days_off += days_difference - MONTHS_DAYSCOUNT[now_date.month]


		print(f"{MONTHS[fullmoon_count]} \t {MONTHS_DAYSCOUNT[fullmoon_count]} \t"+ 
			f"{entries[i]['friendlydate']} - {next_row['friendlydate']}") #\t{round(days_difference, 3)}

		
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
			# print(year_contains_muharram(lunar_year, entries))
			print()

			# is_muharram_next_year = year_contains_muharram(lunar_year, entries)
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



# def year_contains_muharram(year, entries):
# 	def is_year(entry):
# 		entry_year = datetime.strptime(entry["datetime"], DATEFORMAT).year
# 		return entry_year == year
# 	# Count how many full moons and return true if 13
# 	dates_in_year = list(filter(is_year, entries))
# 	return len(dates_in_year) == 13
