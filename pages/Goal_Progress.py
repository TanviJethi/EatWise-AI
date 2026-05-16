import streamlit as st

st.markdown("## :green[Goal Progress]")
st.write("> Track your progress towards your health goals and stay motivated on your journey.")
# Add progress tracking components
st.markdown("### :green[My Progress]")
goal = st.selectbox("Select Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
progress = st.slider("Progress towards goal (%)", min_value=0, max_value=100)
st.info(f"Your progress towards your goal of {goal} is {progress}%. Keep up the good work!")
