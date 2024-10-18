from datetime import datetime, timedelta

class HijriPredictor:
    def __init__(self, model, preprocessor):
        self.model = model
        self.preprocessor = preprocessor

    def predict_hijri_date(self, gregorian_date):
        features = self.preprocessor.prepare_features(pd.to_datetime([gregorian_date]))
        days_since_start = self.model.predict(features)[0]
        hijri_date = self.preprocessor.gregorian_start + timedelta(days=days_since_start)
        return hijri_date