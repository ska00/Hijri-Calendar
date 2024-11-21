import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

class GeographicalAnalysis:
    def __init__(self, model, preprocessor):
        self.model = model
        self.preprocessor = preprocessor

    def analyze_by_region(self, data, regions):
        results = {}
        for region in regions:
            region_data = data[data['region'] == region]
            X = self.preprocessor.prepare_features(region_data['gregorian_date'])
            y = self.preprocessor.prepare_target(region_data['hijri_date'])
            predictions = self.model.predict(X)
            mse = mean_squared_error(y, predictions)
            results[region] = mse
        return results

    def plot_regional_performance(self, results):
        regions = list(results.keys())
        mse_values = list(results.values())

        plt.figure(figsize=(12, 6))
        plt.bar(regions, mse_values)
        plt.title('Model Performance by Region')
        plt.xlabel('Region')
        plt.ylabel('Mean Squared Error')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()