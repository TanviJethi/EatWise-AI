

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from logic.data_loader import load_diet_recommendation_dataset
import joblib

class NutritionClusteringModel:
    def __init__(self, n_clusters=5, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
        )
        self.feature_columns = None  


    def save_model(self, path="nutrition_model.pkl"):
        joblib.dump({
            "kmeans": self.kmeans,
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
        }, path)

        print(f"Model saved to {path}")


    def load_model(self, path="nutrition_model.pkl"):
        data = joblib.load(path)

        self.kmeans = data["kmeans"]
        self.scaler = data["scaler"]
        self.feature_columns = data["feature_columns"]

        print(f"Model loaded from {path}")

    def fit(self):
        """
        Fit the clustering model on the user dataset.
        """
        df = load_diet_recommendation_dataset()

        print("ORIGINAL COLUMNS")
        print(df.columns.tolist())
        print("Shape: ", df.shape)

        
        numeric_df = df.select_dtypes(include="number")
        self.feature_columns = numeric_df.columns.tolist()

        if not self.feature_columns:
            raise ValueError("No numeric columns in diet_recommendation_dataset!")

        print("Numeric columns:", self.feature_columns)
        print("Shape before dropna:", numeric_df.shape)

        # 2. Drop NA rows
        numeric_df = numeric_df.dropna()
        print("Shape after dropna:", numeric_df.shape)

        X = numeric_df.values

        # 3. Scale and fit
        X_scaled = self.scaler.fit_transform(X)
        self.kmeans.fit(X_scaled)

        print(
            f"KMeans fitted with {self.n_clusters} clusters on "
            f"{X_scaled.shape[0]} users."
        )

    def predict_cluster(self, user_features):
        
        n_features = user_features.shape[1]
        expected = self.scaler.n_features_in_

        if n_features != expected:
            raise ValueError(
                f"user_features has {n_features} features "
                f"(expected {expected} for columns {self.feature_columns})"
            )

        X_scaled = self.scaler.transform(user_features)
        cluster = self.kmeans.predict(X_scaled)[0]
        return int(cluster)


if __name__ == "__main__":
    model = NutritionClusteringModel(n_clusters=5)
    model.fit()
    print("Model fitted successfully!")