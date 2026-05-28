
import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_daily_nutrition_dataset():
    """This is the FOOD dataset (daily_food_nutrition_dataset.csv)"""
    path = os.path.join(DATA_DIR, "daily_food_nutrition_dataset.csv")
    df = pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")
    print("1. food_df shape:", df.shape)

   
    min_cal = 200
    min_protein = 10
    df["is_main"] = (
        (df["Calories (kcal)"] >= min_cal) &
        (df["Protein (g)"] >= min_protein)
    ).astype(int)

    print("2. labels_df skipped (no model); added is_main based on rules")
    print("3. df with is_main shape:", df.shape)
    print("is_main counts:\n", df["is_main"].value_counts(dropna=False))

    return df


def load_diet_recommendation_dataset():
    path = os.path.join(DATA_DIR, "diet_recommendations_dataset.csv")
    df = pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")
    print("shape: ", df.shape)
    return df


if __name__ == "__main__":
    print("=== Testing data_loader directly ===\n")

    print("1. Testing load_daily_nutrition_dataset()...")
    food_df = load_daily_nutrition_dataset()

    print("\n2. Testing load_diet_recommendation_dataset()...")
    user_df = load_diet_recommendation_dataset()