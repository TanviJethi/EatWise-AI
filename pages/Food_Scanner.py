import streamlit as st
from streamlit_card import card

st.markdown("## :blue[Food Scanner]")
st.write("Scan food items to get nutritional information and a health rating. Simply upload an image of your food item, and our AI-powered scanner will analyze it to provide you with insights into its nutritional content and overall healthiness. Start scanning your food today and take a step towards a healthier lifestyle!")
image = st.file_uploader("Upload an image of your food item", type=["jpg", "jpeg", "png"])
if st.button("Scan"):
    if image is not None:    
        col_image, col_rating = st.columns(2)
        with col_image:
            st.image(image, caption="Uploaded Food Item", width=300)
        with col_rating:
            st.success("FOOD RATING")
        st.markdown("### :blue[Nutritional Info]")
        col1, col2 = st.columns(2)  
        with col1:
            res = card(
                title="Carbs",
                text="x g",
            )
            res = card(
                title="Protein",
                text="x g",
            )
        with col2:
            res = card(
                title="Fat",
                text="x g",
            )
            res = card(
                title="Sugar",
                text="x g",
            )
    elif image is None:
        st.info("Please upload an image and click 'Scan' to see the results.")