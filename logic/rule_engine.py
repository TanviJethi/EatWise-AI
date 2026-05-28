# logic/rule_engine.py

import pandas as pd


# -----------------------------------
# Helper: remove duplicate foods
# -----------------------------------

def remove_duplicates(food_df):

    return food_df.drop_duplicates(
        subset=["Food_Item"]
    )


# -----------------------------------
# Helper: remove tiny ingredient foods
# -----------------------------------

def remove_tiny_foods(food_df, min_calories=100):

    return food_df[
        food_df["Calories (kcal)"] >= min_calories
    ]


# -----------------------------------
# Diabetes filter
# -----------------------------------

def apply_diabetes_rules(food_df):

    avoid_keywords = [
        "fries",
        "cake",
        "croissant",
        "donut",
        "candy",
        "soda",
        "sugar"
    ]

    pattern = "|".join(avoid_keywords)

    filtered = food_df[
        ~food_df["Food_Item"]
        .str.lower()
        .str.contains(pattern, na=False)
    ]

    return filtered


# -----------------------------------
# Hypertension filter
# -----------------------------------

def apply_hypertension_rules(food_df):

    # Lower sodium foods
    return food_df[
        food_df["Sodium (mg)"] <= 500
    ]


# -----------------------------------
# Simple nutrition scoring
# -----------------------------------

def apply_nutrition_scoring(food_df):

    food_df = food_df.copy()

    food_df["score"] = (

        food_df["Protein (g)"] * 2

        - food_df["Sugars (g)"] * 1.5

        - food_df["Sodium (mg)"] * 0.01
    )

    food_df = food_df.sort_values(
        by="score",
        ascending=False
    )

    return food_df


# -----------------------------------
# Main rule engine
# -----------------------------------

def apply_rule_engine(
    food_df,
    diabetes=False,
    hypertension_bp=False
):

    # Remove duplicate foods
    food_df = remove_duplicates(food_df)

    # Remove tiny foods
    food_df = remove_tiny_foods(food_df)

    # Disease-based filtering
    if diabetes:
        food_df = apply_diabetes_rules(food_df)

    if hypertension_bp:
        food_df = apply_hypertension_rules(food_df)

    # Apply scoring
    food_df = apply_nutrition_scoring(food_df)

    return food_df