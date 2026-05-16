import streamlit as st

home_page = st.Page("pages/Home.py", title="Home", icon="🏠", default=True)
health_profile = st.Page("pages/Health_Profile.py", title="Health Profile", icon="👤")
meal_plan = st.Page("pages/Meal_Plan.py", title="Meal Plan", icon="🍽️")
food_scanner = st.Page("pages/Food_Scanner.py", title="Food Scanner", icon="📷")
goal_progress = st.Page("pages/Goal_Progress.py", title="Goal Progress", icon="📈")
ask_vani = st.Page("pages/Ask_Vani.py", title="Ask Vani", icon="💬")
about_page = st.Page("pages/About.py", title="About", icon="ℹ️")

pg = st.navigation([
    home_page,
    health_profile, 
    meal_plan, 
    food_scanner, 
    goal_progress, 
    ask_vani, 
    about_page
])

st.markdown("# 🥗 :rainbow[EatWise AI]")
st.markdown("###### Your Personal Nutrition Companion")

pg.run()