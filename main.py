# Set up and run this Streamlit App
import streamlit as st
# from helper_functions import llm # <--- Not needed anymore. The helper function is now directly called by `customer_query_handler` 🆕
from logics.skillsfuture_query_handler import process_user_message
from utility import check_password

# Do not continue if check_password is not True
if not check_password():
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="SkillsFuture Course Helper"
)

# endregion <--------- Streamlit App Configuration --------->

st.title("SkillsFuture Helper📚🏫")

form = st.form(key="form")
form.subheader("Enquiries")

user_prompt = (
    form.text_area(
        """
        Enter your enquiries here, and we will try our best to help!\n
        Note: Records are accurate as of 10 November 2025
        """, 
        height=200
        )
)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = process_user_message(user_prompt) #<--- This calls the `process_user_message` function that we have created 🆕
    st.write(response)
    print(f"User Input is {user_prompt}")