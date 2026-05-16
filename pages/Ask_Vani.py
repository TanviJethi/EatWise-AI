import streamlit as st

st.markdown("## :violet[Ask Vani]")

st.write("Have questions about physical activity, sleep, or hydration? Ask Vani for evidence-based recommendations tailored to your age and lifestyle!")
question = st.selectbox("Ask Vani :", ["How much physical activity is recommended?", "How much sleep is recommended?", "What is the recommended daily water intake?"])
if question == "How much physical activity is recommended?":
    age = st.selectbox("Select your age group:", ["Infants under 1 year", "Children 1-2 years","Children 3-4 years","Children (5-17 years) & Teens", "Adults (18-64 years)", "Older Adults (65+ years)"])
    if age == "Infants under 1 year":
        st.info("At least 30 minutes of tummy time spread throughout the day.")
    elif age == "Children 1-2 years":
        st.info("At least 180 minutes of various physical activities at any intensity.")
    elif age == "Children 3-4 years":
        st.info("At least 180 minutes of physical activity, with at least 60 minutes being moderate-to-vigorous intensity")
    elif age == "Children (5-17 years) & Teens":
        st.info("An average of at least 60 minutes per day of moderate-to-vigorous intensity activity across the week")
    elif age == "Adults (18-64 years)":
        st.info("150–300 minutes of moderate-intensity OR 75–150 minutes of vigorous-intensity aerobic activity per week.")
    elif age == "Older Adults (65+ years)":
        st.info("Same aerobic targets as younger adults (150–300 mins moderate or 75–150 mins vigorous weekly)..")
elif question == "How much sleep is recommended?":
    age = st.selectbox("Select your age group:", ["Newborns (0-3 months)", "Infants (4-12 months)","Toddlers (1-2 years)","Preschoolers (3-5 years)", "Children (6-12 years)", "Teens (13-18 years)", "Adults (18-64 years)", "Older Adults (65+ years)"])
    if age == "Newborns (0-3 months)":
        st.info("14-17 hours per day")
    elif age == "Infants (4-12 months)":
        st.info("12-16 hours per day")
    elif age == "Toddlers (1-2 years)":
        st.info("11-14 hours per day")
    elif age == "Preschoolers (3-5 years)":
        st.info("10-13 hours per day")
    elif age == "Children (6-12 years)":
        st.info("9-12 hours per night")
    elif age == "Teens (13-18 years)":
        st.info("8-10 hours per night")
    elif age == "Adults (18-64 years)":
        st.info("7 or more hours per night")
    elif age == "Older Adults (65+ years)":
        st.info("7 or more hours per night")
elif question == "What is the recommended daily water intake?":
    condition = st.selectbox("Select your Physiological State:", ["Average Conditions", "Active Individuals or Hot Climates", "Lactating/ Breastfeeding Mothers"])
    if condition == "Average Conditions":
        st.info(" 2.0 to 2.5 liters per day (about 8 glasses) is recommended for an average adult")
    elif condition == "Active Individuals or Hot Climates":
        st.info("Up to 4.5 to 6.0 Litres per day (depending on sweat rate and exposure intensity)")
    elif condition == "Lactating/ Breastfeeding Mothers":
        st.info("4.5 to 5.5 Litres of total fluid per day (which inherently includes a baseline minimum of 2.6 to 3.4 Litres of plain drinking fluid)")
