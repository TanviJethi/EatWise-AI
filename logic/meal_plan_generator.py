

import pandas as pd
import numpy as np
from logic.rule_engine import apply_rule_engine
from logic.main_nutrition import (
    bmi_calculator,
    bmr_calculator,
    tdee_calculator,
    calorie_macros_calculator,
)
from logic.model import NutritionClusteringModel
from logic.data_loader import load_daily_nutrition_dataset


def classify_food_type(food_name):

    food_name = str(food_name).lower()

    non_veg_keywords = [
        "chicken",
        "beef",
        "fish",
        "egg",
        "mutton",
        "pork",
        "turkey",
        "bacon",
        "ham",
        "shrimp",
        "meat"
    ]

    for word in non_veg_keywords:
        if word in food_name:
            return "non_veg"

    return "veg"


def generate_meal_plan(
    age,
    gender,
    height_cm,
    weight_kg,
    activity_level,
    goal,
    diet_type,  # "veg", "non_veg"
    allergies=None,
    diabetes=False,
    hypertension_bp=False,
    model=None,
):
    """
    Generate a full nutrition plan for a user.

    Returns:
        {
            "bmi": float,
            "bmr": float,
            "tdee": float,
            "macros": dict,
            "cluster": int,
            "meals": {
                "breakfast": [ { ... }, ... ],
                "lunch": [ { ... }, ... ],
                "dinner": [ { ... }, ... ],
            }
        }
    """
    if allergies is None:
        allergies = []

   
    bmi = bmi_calculator(weight_kg, height_cm)
    bmr = bmr_calculator(age, gender, weight_kg, height_cm)
    tdee = tdee_calculator(bmr, activity_level)
    macros = calorie_macros_calculator(tdee, goal)

   
    user_features = np.array(
        [
            [
                age,
                weight_kg,
                height_cm,
                bmi,
                tdee,  
                0.0,  
                0.0,  
                0.0,  
                3.0,  
                1.0,  
                0.5,  
            ]
        ]
    )
    print("User_features shape:", user_features.shape)

    
    if model is None:
        raise ValueError("model must be provided (e.g., from core_pipeline.G_MODEL)")

    cluster = model.predict_cluster(user_features)

    
    food_df = load_daily_nutrition_dataset()
    print("Number of foods:", len(food_df))

    
    filtered_df = _apply_food_filters(
        food_df,
        diet_type=diet_type,
        allergies=allergies,
        diabetes=diabetes,
        hypertension_bp=hypertension_bp,
    )

    filtered_df = apply_rule_engine(
    filtered_df,
    diabetes=diabetes,
    hypertension_bp=hypertension_bp
)


    print("Filtered foods:", len(filtered_df))

    if filtered_df.empty:
       
        df = food_df.copy()
        df["food_type"] = df["Food_Item"].apply(classify_food_type)

        
        if diet_type == "veg":
            df = df[df["food_type"] == "veg"]

        elif diet_type == "non_veg":
            df = df[df["food_type"] == "non_veg"]

        
        if allergies:
            for allergen in allergies:
                pattern = allergen.lower()
                danger_mask = (
                    df["Food_Item"].str.contains(pattern, case=False, na=False) |
                    df["Category"].str.contains(pattern, case=False, na=False)
                )
                df = df[~danger_mask]

        
        if diabetes:
            df = df[df["Sugars (g)"] <= 10.0]

        
        if hypertension_bp:
            df = df[df["Sodium (mg)"] <= 400]

        filtered_df = df

        if filtered_df.empty:
            raise ValueError("No foods passed filters even after relaxing constraints.")

   
    meals = _pick_meals_greedy(
        food_df=filtered_df,
        tdee=tdee,
        target_protein=macros["protein_gm"],
        target_carbs=macros["carbs_gm"],
        target_fats=macros["fats_gm"],
        num_options_per_meal=3,
    )

    return {
        "bmi": float(bmi),
        "bmr": float(bmr),
        "tdee": float(tdee),
        "macros": macros,
        "cluster": int(cluster),
        "meals": meals,
    }


def _apply_food_filters(
    food_df,
    diet_type,
    allergies,
    diabetes,
    hypertension_bp,
):
    """
    Filter by diet_type, allergies, diabetes, hypertension.
    """
    df = food_df.copy()

   
    if diet_type == "veg":
        df = df[df["Category"].str.contains("veg|vegetarian", case=False, na=False)]
    elif diet_type == "non_veg":
        df = df[df["Category"].str.contains("non.*veg", case=False, na=False)]

    
    if allergies:
        for allergen in allergies:
            pattern = allergen.lower()
            mask = (
                df["Food_Item"].str.contains(pattern, case=False, na=False) |
                df["Category"].str.contains(pattern, case=False, na=False)
            )
            df = df[~mask]

   
    if diabetes:
        df = df[
        (df["Sugars (g)"] <= 15.0) &
        (df["Carbohydrates (g)"] <= 60.0) & (df["Calories (kcal)"]<=400)
    ]

    
    if hypertension_bp:
        df = df[df["Sodium (mg)"] <= 500]

    return df


def _pick_meals_greedy(
    food_df,
    tdee,
    target_protein,
    target_carbs,
    target_fats,
    calories_per_meal_tolerance=0.4,
    num_options_per_meal=3,
):
    """
    Pick multiple meaningful options per meal.
    """
    calories_per_meal = tdee / 3

    
    MIN_BF_CAL = 150
    MIN_LN_CAL = 250
    MIN_DN_CAL = 350

    min_cal_map = {
        "breakfast": MIN_BF_CAL,
        "lunch": MIN_LN_CAL,
        "dinner": MIN_DN_CAL,
    }

    low_ratio = 1 - calories_per_meal_tolerance
    high_ratio = 1 + calories_per_meal_tolerance

    meals = {}
    meal_types = ["breakfast", "lunch", "dinner"]
    used_foods = set()
    for meal in meal_types:
        min_cal = min_cal_map[meal]
        low_cal = max(min_cal, calories_per_meal * low_ratio)
        high_cal = calories_per_meal * high_ratio

       
        candidates = food_df[
            (food_df["Meal_Type"].str.contains(meal, case=False, na=False)) |
            (food_df["Meal_Type"].str.contains("any", case=False, na=False))
        ].copy()

        
        if meal in ["lunch", "dinner"]:
            candidates = candidates[candidates["is_main"] == 1]

       
        candidates = candidates[candidates["Calories (kcal)"] >= min_cal]

       
        candidates = candidates[candidates["Calories (kcal)"].between(low_cal, high_cal)]

        
        if candidates.empty:
            candidates = food_df[
            food_df["Calories (kcal)"] >= 100]
            base = food_df[
                (food_df["Meal_Type"].str.contains(meal, case=False, na=False)) |
                (food_df["Meal_Type"].str.contains("any", case=False, na=False))
            ]
            base = base[base["Calories (kcal)"] >= min_cal]
            if not base.empty:
                candidates = base
            else:
                candidates = food_df[food_df["Calories (kcal)"] >= min_cal]

       
        if candidates.empty:
            candidates = food_df.sample(n=num_options_per_meal, replace=True)

       
        n = min(num_options_per_meal, len(candidates))
        if n > 0:
            sampled = candidates.sample(n=n, replace=False)
        else:
            sampled = candidates.iloc[:num_options_per_meal]

        options = []

        for _, row in sampled.iterrows():

            food_name = row["Food_Item"]

            # skip duplicates
            if food_name in used_foods:
                continue

            used_foods.add(food_name)

            options.append({
                "food_name": food_name,
                "calories": float(row["Calories (kcal)"]),
                "protein_gm": float(row["Protein (g)"]),
                "carbs_gm": float(row["Carbohydrates (g)"]),
                "fats_gm": float(row["Fat (g)"]),
                "sodium_mg": float(row.get("Sodium (mg)", 0)),
                "sugars_g": float(row.get("Sugars (g)", 0)),
            })

        # =========================================
        # FALLBACK IF EVERYTHING GOT SKIPPED
        # =========================================

        if len(options) == 0:

            fallback = food_df.sample(n=1).iloc[0]

            options.append({
                "food_name": fallback["Food_Item"],
                "calories": float(fallback["Calories (kcal)"]),
                "protein_gm": float(fallback["Protein (g)"]),
                "carbs_gm": float(fallback["Carbohydrates (g)"]),
                "fats_gm": float(fallback["Fat (g)"]),
                "sodium_mg": float(fallback.get("Sodium (mg)", 0)),
                "sugars_g": float(fallback.get("Sugars (g)", 0)),
            })

        meals[meal] = options

    return meals