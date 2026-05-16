import streamlit as st
from streamlit_card import card

st.markdown("## :yellow[Meal Plan]")
st.write("> Get your personalized meal plan based on your health profile and goals. Simply input your dietary preferences and specific health goals, and we'll generate a meal plan that includes nutritious recipes to help you achieve your objectives. Start your journey to better health with our customized meal plans today! ")
tab1 , tab2, tab3 = st.tabs(["Breakfast", "Lunch", "Dinner"])
with tab1:
            res = card(
            title="Breakfast",
            text="Required Kcal"
            ) 
            with st.expander("Meal Options", expanded=False):
                st.write("""
                - wwwww
                - vvvvvv
                - xxxxxx
                """)
with tab2:
            res = card(
            title="Lunch",
            text="Required Kcal"
            )
            with st.expander("Meal Options", expanded=False):
                st.write("""
                - wwwww
                - vvvvvv
                - xxxxxx
                """)
with tab3:
            res = card(
            title="Dinner",
            text="Required Kcal"
            )
            with st.expander("Meal Options", expanded=False):
                st.write("""
                - wwwww
                - vvvvvv
                - xxxxxx
                """)