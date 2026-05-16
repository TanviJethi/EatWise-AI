import streamlit as st

st.markdown("## :orange[My health profile]")
st.markdown(" > Create and manage your health profile to get personalized recommendations.")

name = st.text_input("Name")
age = st.slider("Age", min_value=0, max_value=120)
weight = st.slider("Weight (kg)", min_value=30, max_value=200)
height = st.slider("Height (cm)", min_value=20, max_value=250)
goal = st.selectbox("Health Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
preferences = st.selectbox("Dietary Preferences", ["Vegetarian", "Vegan", "Non-Vegetarian"])
activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
submit_button = st.button("Save Profile")
if submit_button:
    st.markdown(f"### Welcome {name}!")