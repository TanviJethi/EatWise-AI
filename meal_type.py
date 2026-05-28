

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pandas as pd


class MealTypeModel:
    def __init__(self):
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ("clf", RandomForestClassifier(n_estimators=50, random_state=42)),
        ])

    def fit(self, foods_df, labels_df):
        """
        foods_df: your food dataset (with Food_Item)
        labels_df: food_labels.csv (columns: Food_Item, is_main)
        """
        merged = foods_df.merge(labels_df, on="Food_Item", how="inner")
        
        X_text = merged["Food_Item"]
        num_cols = ["Calories (kcal)", "Protein (g)", "Carbohydrates (g)", "Fat (g)"]
        X_num = merged[num_cols].fillna(0)
        # Combine text + numbers
        X = pd.concat([X_text.to_frame(name="Food_Item"), X_num], axis=1)
        y = merged["is_main"]
        print("X shape:", X.shape)
        print("y shape:", y.shape)

        self.pipeline.fit(X, y)

    def predict_is_main(self, foods_df):
        """
        foods_df: your full food dataset (all 645 rows)
        returns: 1D array of is_main (0 or 1)
        """
        X_text = foods_df["Food_Item"]
        num_cols = ["Calories (kcal)", "Protein (g)", "Carbohydrates (g)", "Fat (g)"]
        X_num = foods_df[num_cols].fillna(0)
        X = pd.concat([X_text.to_frame(name="Food_Item"), X_num], axis=1)

        return self.pipeline.predict(X)
    



