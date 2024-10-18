import math
from datetime import date, timedelta

class MetonicCycle:
    CYCLE_YEARS = 19
    CYCLE_LUNAR_MONTHS = 235

    def __init__(self, solar_year_length=365.2425, lunar_month_length=29.53059):
        self.solar_year_length = solar_year_length
        self.lunar_month_length = lunar_month_length
        self.cycle_length_days = self.CYCLE_YEARS * self.solar_year_length
        self.cycle_error = (self.CYCLE_LUNAR_MONTHS * self.lunar_month_length) - self.cycle_length_days

    def get_cycle_count(self, years):
        return years // self.CYCLE_YEARS

    def get_remaining_years(self, years):
        return years % self.CYCLE_YEARS

    def calculate_drift(self, years):
        cycles = self.get_cycle_count(years)
        remaining_years = self.get_remaining_years(years)
        return (cycles * self.cycle_error) + (remaining_years * (self.solar_year_length - self.lunar_month_length * 12))

class IslamicCalendar:
    def __init__(self, year_length=354.36707):
        self.year_length = year_length
        self.metonic_cycle = MetonicCycle()

    def gregorian_to_islamic(self, gregorian_date, known_islamic_date, known_gregorian_date):
        years_diff = gregorian_date.year - known_gregorian_date.year
        days_diff = (gregorian_date - known_gregorian_date).days

        total_drift = self.metonic_cycle.calculate_drift(years_diff)
        total_days = days_diff + total_drift

        islamic_years_passed = math.floor(total_days / self.year_length)
        remaining_days = total_days % self.year_length
        islamic_months_passed = math.floor(remaining_days / self.metonic_cycle.lunar_month_length)

        new_islamic_year = known_islamic_date[0] + islamic_years_passed
        new_islamic_month = (known_islamic_date[1] + islamic_months_passed - 1) % 12 + 1
        new_islamic_day = known_islamic_date[2]  # Approximation

        return (new_islamic_year, new_islamic_month, new_islamic_day)

    def islamic_to_gregorian(self, islamic_date, known_islamic_date, known_gregorian_date):
        years_diff = islamic_date[0] - known_islamic_date[0]
        months_diff = islamic_date[1] - known_islamic_date[1]
        days_diff = islamic_date[2] - known_islamic_date[2]

        total_days = (years_diff * self.year_length) + (months_diff * self.metonic_cycle.lunar_month_length) + days_diff
        
        # Adjust for Metonic cycle drift
        metonic_cycles = self.metonic_cycle.get_cycle_count(years_diff)
        total_days -= metonic_cycles * self.metonic_cycle.cycle_error

        return known_gregorian_date + timedelta(days=round(total_days))

class CalendarConverter:
    def __init__(self):
        self.islamic_calendar = IslamicCalendar()

    def predict_islamic_date(self, gregorian_date, known_islamic_date, known_gregorian_date):
        return self.islamic_calendar.gregorian_to_islamic(gregorian_date, known_islamic_date, known_gregorian_date)

    def predict_gregorian_date(self, islamic_date, known_islamic_date, known_gregorian_date):
        return self.islamic_calendar.islamic_to_gregorian(islamic_date, known_islamic_date, known_gregorian_date)

# Example usage
converter = CalendarConverter()

# Known correspondence
known_gregorian = date(2023, 11, 15)
known_islamic = (1445, 5, 1)  # 1 Jumada al-awwal 1445 AH

# Predict Islamic date for a future Gregorian date
future_gregorian = date(2050, 11, 15)
predicted_islamic = converter.predict_islamic_date(future_gregorian, known_islamic, known_gregorian)
print(f"Predicted Islamic date for {future_gregorian}: Year {predicted_islamic[0]}, Month {predicted_islamic[1]}, Day {predicted_islamic[2]}")

# Predict Gregorian date for a future Islamic date
future_islamic = (1500, 1, 1)  # 1 Muharram 1500 AH
predicted_gregorian = converter.predict_gregorian_date(future_islamic, known_islamic, known_gregorian)
print(f"Predicted Gregorian date for Islamic Year {future_islamic[0]}, Month {future_islamic[1]}, Day {future_islamic[2]}: {predicted_gregorian}")
