from data_loader import DataLoader
from preprocessor import Preprocessor
from hijri_model import HijriModel
from predictor import HijriPredictor

def main():
    # Load data
    loader = DataLoader('path_to_your_data.csv')
    data = loader.load_data()

    # Preprocess data
    preprocessor = Preprocessor()
    X = preprocessor.prepare_features(data['gregorian_date'])
    y = preprocessor.prepare_target(data['hijri_date'])

    # Define feature names
    feature_names = [
        'Days Since Start', 'Metonic Phase', 'Lunar Phase', 'Year', 'Month', 'Day',
        'Day of Year', 'Is Leap Year', 'Season', 'Moon Elongation', 'Is Potential Month Start'
    ]

    # Train model
    model = HijriModel()
    model.train(X, y)

    # Perform cross-validation
    model.cross_validate(X, y)

    # Visualize feature importance
    model.plot_feature_importance(feature_names)

    # Visualize predictions
    model.visualize_predictions(X, y, data['gregorian_date'], data['hijri_date'], preprocessor)

    # Create predictor
    predictor = HijriPredictor(model, preprocessor)

    # Example prediction
    gregorian_date = datetime(2023, 11, 15)
    predicted_hijri = predictor.predict_hijri_date(gregorian_date)
    print(f"Predicted Hijri date for {gregorian_date.date()}: {predicted_hijri.date()}")

if __name__ == "__main__":
    main()