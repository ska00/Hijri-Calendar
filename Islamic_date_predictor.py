import datetime
import math

class IslamicDatePredictor:
    def __init__(self):
        self.gregorian_year_length = 365.2425  # Average Gregorian year length
        self.islamic_year_length = 354.36707   # Average Islamic year length
        self.metonic_cycle_years = 19          # Years in a Metonic cycle
        self.metonic_cycle_months = 235        # Lunar months in a Metonic cycle

    def predict_islamic_date(self, gregorian_date, islamic_date, future_gregorian_year):
        """
        Predict the Islamic date for a given future Gregorian year based on a known correspondence.
        
        :param gregorian_date: Known Gregorian date (datetime.date)
        :param islamic_date: Corresponding Islamic date (tuple of year, month, day)
        :param future_gregorian_year: The Gregorian year to predict for
        :return: Predicted Islamic date (tuple of year, month, day)
        """
        years_diff = future_gregorian_year - gregorian_date.year
        
        # Calculate the number of complete Metonic cycles
        metonic_cycles = years_diff // self.metonic_cycle_years
        remaining_years = years_diff % self.metonic_cycle_years

        # Calculate the drift within the Metonic cycle
        cycle_drift = (self.metonic_cycle_months * 29.53059) - (self.metonic_cycle_years * self.gregorian_year_length)
        
        # Calculate total drift
        total_drift = (metonic_cycles * cycle_drift) + (remaining_years * (self.gregorian_year_length - self.islamic_year_length))

        # Convert drift to Islamic years and months
        islamic_years_passed = math.floor(total_drift / self.islamic_year_length)
        remaining_days = total_drift % self.islamic_year_length
        islamic_months_passed = math.floor(remaining_days / 29.53059)

        # Calculate new Islamic date
        new_islamic_year = islamic_date[0] + islamic_years_passed
        new_islamic_month = (islamic_date[1] + islamic_months_passed - 1) % 12 + 1
        
        # Approximate the day (this is less accurate due to variable month lengths)
        new_islamic_day = islamic_date[2]  # Assuming same day for simplicity

        return (new_islamic_year, new_islamic_month, new_islamic_day)

    def get_equation_explanation(self):
        """
        Provide an explanation of the equation used in the prediction.
        """
        explanation = """
        The prediction is based on the following equation:

        D = (N * Cm) + (R * (Gy - Iy))

        Where:
        D  = Total drift in days
        N  = Number of complete Metonic cycles
        Cm = Cycle drift (difference between Metonic cycle and exact solar years)
        R  = Remaining years after complete Metonic cycles
        Gy = Gregorian year length
        Iy = Islamic year length

        The total drift is then converted to Islamic years and months:

        Islamic Years Passed = floor(D / Iy)
        Remaining Days = D % Iy
        Islamic Months Passed = floor(Remaining Days / 29.53059)

        These calculations provide an approximation, as they don't account for
        the exact lengths of Islamic months which can vary based on lunar sightings.
        """
        return explanation

# Example usage
predictor = IslamicDatePredictor()

# Known correspondence
known_gregorian = datetime.date(2023, 11, 15)
known_islamic = (1445, 5, 1)  # 1 Jumada al-awwal 1445 AH

# Predict for a future year
future_year = 2050

predicted_islamic = predictor.predict_islamic_date(known_gregorian, known_islamic, future_year)

print(f"Predicted Islamic date for Gregorian year {future_year}:")
print(f"{predicted_islamic[0]} AH, Month {predicted_islamic[1]}, Day {predicted_islamic[2]}")

print("\nEquation Explanation:")
print(predictor.get_equation_explanation())
