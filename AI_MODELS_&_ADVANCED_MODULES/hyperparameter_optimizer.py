from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class HyperparameterOptimizer:
    def __init__(self, X, y, cv=5, n_iter=100):
        self.X = X
        self.y = y
        self.cv = cv
        self.n_iter = n_iter

    def grid_search(self):
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=self.cv, n_jobs=-1, verbose=2)
        grid_search.fit(self.X, self.y)
        return grid_search.best_params_, grid_search.best_score_

    def random_search(self):
        param_distributions = {
            'n_estimators': np.arange(100, 1000, 100),
            'max_depth': [None] + list(np.arange(10, 110, 10)),
            'min_samples_split': np.arange(2, 21),
            'min_samples_leaf': np.arange(1, 21)
        }
        rf = RandomForestRegressor(random_state=42)
        random_search = RandomizedSearchCV(rf, param_distributions, n_iter=self.n_iter, cv=self.cv, n_jobs=-1, verbose=2, random_state=42)
        random_search.fit(self.X, self.y)
        return random_search.best_params_, random_search.best_score_