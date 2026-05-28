# logic/core_pipeline.py

import pandas as pd
from logic.data_loader import load_diet_recommendation_dataset, load_daily_nutrition_dataset
from logic.model import NutritionClusteringModel
from logic.main_nutrition import (
    bmi_calculator,
    bmr_calculator,
    tdee_calculator,
    calorie_macros_calculator,
)
from logic.meal_plan_generator import generate_meal_plan


G_MODEL = None


def initialize_pipeline():
    
    global G_MODEL
    G_MODEL = NutritionClusteringModel(n_clusters=5)
    G_MODEL.load_model()
    print("Nutrition pipeline initialized.")


def get_nutrition_plan(
    age,
    gender,
    height_cm,
    weight_kg,
    activity_level,
    goal,
    diet_type,
    allergies=None,
    diabetes=False,
    hypertension_bp=False,
):
    
    if allergies is None:
        allergies = []

   
    if not isinstance(age, int) or age < 1 or age > 120:
        raise ValueError("Age must be an integer between 1 and 120.")

    if not isinstance(height_cm, (int, float)) or height_cm <= 0:
        raise ValueError("Height must be a positive number.")

    if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
        raise ValueError("Weight must be a positive number.")

    allowed_levels = ["sedentary", "light", "moderate", "very_active"]
    if activity_level not in allowed_levels:
        raise ValueError(f"activity_level must be one of {allowed_levels}.")

    allowed_goals = ["weight_loss", "maintenance", "weight_gain"]
    if goal not in allowed_goals:
        raise ValueError(f"goal must be one of {allowed_goals}.")

    allowed_types = ["veg", "non_veg"]
    if diet_type not in allowed_types:
        raise ValueError(f"diet_type must be one of {allowed_types}.")

    
    plan = generate_meal_plan(
        age=age,
        gender=gender,
        height_cm=height_cm,
        weight_kg=weight_kg,
        activity_level=activity_level,
        goal=goal,
        diet_type=diet_type,
        allergies=allergies,
        diabetes=diabetes,
        hypertension_bp=hypertension_bp,
        model=G_MODEL,
    )
    return plan