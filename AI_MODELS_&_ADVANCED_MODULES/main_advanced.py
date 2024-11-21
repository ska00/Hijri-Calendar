from data_loader import DataLoader
from preprocessor import Preprocessor
from hijri_model import HijriModel
from hyperparameter_optimizer import HyperparameterOptimizer
from time_series_model import TimeSeriesModel
from geographical_analysis import GeographicalAnalysis

def main():
    # Load and preprocess data
    loader = DataLoader('path_to_your_data.csv')
    data = loader.load_data()
    preprocessor = Preprocessor()
    X = preprocessor.prepare_features(data['gregorian_date'])
    y = preprocessor.prepare_target(data['hijri_date'])

    # Hyperparameter optimization
    optimizer = HyperparameterOptimizer(X, y)
    best_params, best_score = optimizer.random_search()
    print(f"Best hyperparameters: {best_params}")
    print(f"Best score: {best_score}")

    # Train optimized model
    optimized_model = HijriModel(**best_params)
    optimized_model.train(X, y)

    # Time series analysis
    ts_model = TimeSeriesModel(data)
    ts_model.fit_arima()
    ts_mse = ts_model.evaluate(data['hijri_date'][-365:])  # Evaluate on last year of data
    print(f"Time Series Model MSE: {ts_mse}")

    # Geographical analysis
    geo_analyzer = GeographicalAnalysis(optimized_model, preprocessor)
    regions = data['region'].unique()  # Assuming 'region' column exists
    regional_results = geo_analyzer.analyze_by_region(data, regions)
    geo_analyzer.plot_regional_performance(regional_results)

if __name__ == "__main__":
    main()