from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

class TimeSeriesModel:
    def __init__(self, data):
        self.data = data
        self.model = None

    def prepare_time_series(self):
        # Convert data to time series format
        ts = pd.Series(self.data['hijri_date'].values, index=self.data['gregorian_date'])
        ts = ts.asfreq('D')  # Ensure daily frequency
        return ts

    def fit_arima(self, order=(1,1,1)):
        ts = self.prepare_time_series()
        self.model = ARIMA(ts, order=order)
        self.model_fit = self.model.fit()

    def predict(self, start_date, end_date):
        if self.model_fit is None:
            raise ValueError("Model not fitted. Call fit_arima() first.")
        forecast = self.model_fit.predict(start=start_date, end=end_date)
        return forecast

    def evaluate(self, test_data):
        predictions = self.predict(test_data.index[0], test_data.index[-1])
        mse = mean_squared_error(test_data, predictions)
        return mse