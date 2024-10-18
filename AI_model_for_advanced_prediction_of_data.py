import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class AdvancedHijriPredictor:
    def __init__(self):
        self.metonic_cycle = 19 * 365.2425  # 19 years in days
        self.hijri_year_length = 354.36707  # Average Hijri year in days
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.gregorian_start = datetime(622, 7, 16)  # Approximate start of Hijri calendar

    def load_data(self, file_path):
        """Load historical Hijri-Gregorian date correspondences."""
        df = pd.read_csv(file_path)
        df['gregorian_date'] = pd.to_datetime(df['gregorian_date'])
        df['hijri_date'] = pd.to_datetime(df['hijri_date'])
        return df

    def prepare_features(self, dates):
        """Prepare features for the model."""
        days_since_start = (dates - self.gregorian_start).dt.total_seconds() / (24 * 3600)
        metonic_phase = (days_since_start % self.metonic_cycle) / self.metonic_cycle
        year = dates.dt.year
        month = dates.dt.month
        day = dates.dt.day
        return np.column_stack((days_since_start, metonic_phase, year, month, day))

    def train_model(self, data):
        """Train the predictive model."""
        X = self.prepare_features(data['gregorian_date'])
        y = (data['hijri_date'] - self.gregorian_start).dt.total_seconds() / (24 * 3600)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model Mean Squared Error: {mse} days^2")

    def predict_hijri_date(self, gregorian_date):
        """Predict Hijri date for a given Gregorian date."""
        features = self.prepare_features(pd.to_datetime([gregorian_date]))
        days_since_start = self.model.predict(features)[0]
        hijri_date = self.gregorian_start + timedelta(days=days_since_start)
        return hijri_date

    def generate_hijri_calendar(self, start_year, end_year):
        """Generate Hijri calendar for a range of Gregorian years."""
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date)
        hijri_dates = [self.predict_hijri_date(date) for date in date_range]
        return pd.DataFrame({'gregorian_date': date_range, 'hijri_date': hijri_dates})

    def plot_calendar_comparison(self, calendar_df):
        """Plot comparison between Gregorian and Hijri dates."""
        plt.figure(figsize=(12, 6))
        plt.scatter(calendar_df['gregorian_date'], calendar_df['hijri_date'], alpha=0.5)
        plt.xlabel('Gregorian Date')
        plt.ylabel('Hijri Date')
        plt.title('Gregorian vs Hijri Date Comparison')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Example usage
predictor = AdvancedHijriPredictor()

# Load historical data (you need to provide this CSV file)
data = predictor.load_data('hijri_gregorian_correspondence.csv')

# Train the model
predictor.train_model(data)

# Predict a specific date
gregorian_date = datetime(2023, 11, 15)
predicted_hijri = predictor.predict_hijri_date(gregorian_date)
print(f"Predicted Hijri date for {gregorian_date.date()}: {predicted_hijri.date()}")

# Generate and plot calendar for a range of years
calendar_df = predictor.generate_hijri_calendar(2023, 2025)
predictor.plot_calendar_comparison(calendar_df)
