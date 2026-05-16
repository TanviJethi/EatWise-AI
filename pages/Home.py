import streamlit as st
from st_circular_progress import CircularProgress

st.markdown(f" ## :red[Hey, Complete your daily nutrition!! ]")
st.write(" > Track your daily nutrient intake and ensure you're meeting your nutritional needs.")

target_calories = 1120
consumed_calories = 656
remaining_calories = target_calories - consumed_calories

percentage = min(int((consumed_calories / target_calories) * 100), 100)

my_meter = CircularProgress(
    label="% Calories Consumed",
    value=percentage,
    key="calorie_tracker_meter",
    color="blue",
    track_color="lightgray",
    size="Large",
)

st.subheader(":blue[Food Log Focus:]")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f" Remaining Calories: {remaining_calories} kcal")
with col2:
    my_meter.st_circular_progress()
with col3:
    st.write(f"Target: {target_calories} kcal")