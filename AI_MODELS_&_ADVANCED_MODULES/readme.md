# Hijri Date Prediction System - Project Structure Overview

## 1. Core Components

### data_loader.py
- **Purpose**: Handles loading and initial processing of the dataset.
- **Key Class**: `DataLoader`
- **Functionality**: Reads CSV file, converts date strings to datetime objects.

### preprocessor.py
- **Purpose**: Prepares data for model input.
- **Key Class**: `Preprocessor`
- **Functionality**: Creates features like Metonic cycle phase, lunar phase, and other relevant astronomical and calendar-based features.

### hijri_model.py
- **Purpose**: Implements the main machine learning model for Hijri date prediction.
- **Key Class**: `HijriModel`
- **Functionality**: Trains Random Forest model, includes methods for prediction, cross-validation, and visualization.

### astronomical_calculator.py
- **Purpose**: Provides traditional astronomical calculations for Hijri dates.
- **Key Class**: `AstronomicalCalculator`
- **Functionality**: Converts between Gregorian and Hijri dates using astronomical methods.

### hybrid_model.py
- **Purpose**: Combines ML predictions with astronomical calculations.
- **Key Class**: `HybridModel`
- **Functionality**: Weighted combination of ML and astronomical predictions.

## 2. Advanced Features

### hyperparameter_optimizer.py
- **Purpose**: Optimizes model hyperparameters.
- **Key Class**: `HyperparameterOptimizer`
- **Functionality**: Implements Grid Search and Random Search for hyperparameter tuning.

### time_series_model.py
- **Purpose**: Implements time series analysis for Hijri date prediction.
- **Key Class**: `TimeSeriesModel`
- **Functionality**: ARIMA model implementation for time series forecasting.

### geographical_analysis.py
- **Purpose**: Analyzes model performance across different geographical regions.
- **Key Class**: `GeographicalAnalysis`
- **Functionality**: Evaluates and visualizes model performance by region.

## 3. Testing and Validation

### test_hijri_model.py
- **Purpose**: Contains unit tests for various components of the system.
- **Key Class**: `TestHijriModel`
- **Functionality**: Tests individual components and overall system accuracy.

## 4. Main Execution Scripts

### main.py
- **Purpose**: Main script for running the basic Hijri date prediction system.
- **Functionality**: Orchestrates data loading, preprocessing, model training, and basic predictions.

### main_advanced.py
- **Purpose**: Script for running advanced analyses and optimizations.
- **Functionality**: Incorporates hyperparameter optimization, time series analysis, and geographical analysis.

## Project Workflow

1. **Data Ingestion**: 
   - `data_loader.py` reads the raw data.

2. **Data Preparation**: 
   - `preprocessor.py` transforms raw data into features suitable for ML models.

3. **Model Training and Prediction**:
   - `hijri_model.py` trains the main ML model.
   - `astronomical_calculator.py` provides traditional calculations.
   - `hybrid_model.py` combines both approaches.

4. **Advanced Analysis**:
   - `hyperparameter_optimizer.py` fine-tunes the ML model.
   - `time_series_model.py` adds time series forecasting capabilities.
   - `geographical_analysis.py` examines regional performance variations.

5. **Testing and Validation**:
   - `test_hijri_model.py` ensures reliability and accuracy of components.

6. **Execution**:
   - `main.py` for basic execution.
   - `main_advanced.py` for running advanced analyses.

## Data Flow

1. Raw data → `DataLoader` → Loaded dataset
2. Loaded dataset → `Preprocessor` → Feature set
3. Feature set → `HijriModel` / `TimeSeriesModel` → Trained models
4. Trained models + `AstronomicalCalculator` → `HybridModel` → Final predictions
5. Various models → `GeographicalAnalysis` → Regional performance insights

## Extensibility

- The modular structure allows for easy addition of new features or models.
- Each component can be independently improved or replaced without affecting others.

## Key Interactions

- `HijriModel` and `AstronomicalCalculator` feed into `HybridModel`.
- `HyperparameterOptimizer` directly impacts `HijriModel` performance.
- `GeographicalAnalysis` works with outputs from various models to provide regional insights.

This structure provides a comprehensive framework for Hijri date prediction, combining traditional methods with advanced machine learning techniques, while allowing for detailed analysis and continuous improvement.