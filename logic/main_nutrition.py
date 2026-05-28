def bmi_calculator(weight_kg, height_cm):
    height_m=height_cm/100
    return weight_kg/(height_m ** 2)


def bmr_calculator(age, gender, weight_kg, height_cm):
    height_m=height_cm/100
    if gender.lower()=="male":
        return 10 * weight_kg + 6.25 * height_m * 100 - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_m * 100 - 5 * age - 161
    

def tdee_calculator(bmr, activity_level):
    multipliers={
        "sedentary":1.2,
        "lightly_active":1.375,
        "moderately_active":1.55,
        "very_active":1.725,
        "extra_active":1.9,
    }
    return bmr * multipliers.get(activity_level.lower(), 1.2)


def calorie_macros_calculator(tdee, goal):
    if goal.lower()=="weight_loss":
        protein=0.30
        carbs=0.40
        fats=0.30
    elif goal.lower()=="weight_gain":
        protein=0.25
        carbs=0.55
        fats=0.20
    else:
        protein=0.25
        carbs=0.50
        fats=0.25
    return {
        "calories": tdee,
        "protein_gm": protein * tdee / 4,
        "carbs_gm": carbs * tdee / 4,
        "fats_gm": fats * tdee / 9, 
    }