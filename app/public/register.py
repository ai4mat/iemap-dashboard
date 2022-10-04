import requests
import streamlit as st
from components.endpoints import urls


st.markdown("# Registration page")

# Create an empty container
placeholder = st.empty()


# Insert a form in the container
with placeholder.form("register"):
    st.markdown("#### Enter your informations")
    email = st.text_input("Email")
    affiliation = st.text_input("Affiliation")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Register")
    form_data = { "email": email, "affiliation": affiliation, "password": password }
    
    try:
        response = requests.post(urls.register, json=form_data)
        if submit and response.status_code == 201:
#            placeholder.form[0]
            st.success("Your are successfully registered! You can now login.")
        elif submit and response.status_code == 400:
            st.error("Sorry, something went wrong. Registration failed!")
        else:
            pass
    except Exception as e:
            st.exception(e)
            mkd = """Please set the user and password."""
            st.error(mkd)

    