import email
import streamlit as st
from components.endpoints import urls
import requests

# Auxiliary functions for autentication
def on_click():
    import time
    if st.session_state["correct_password"]:
        st.session_state["admin_view"] = True
#        st.session_state['token'] = token
        time.sleep(.25)
        query_dict = {}
        st.experimental_set_query_params(**query_dict)        
    else:
        st.warning("Wrong username or password")

placeholder = st.empty()


# Insert a form in the container
with placeholder.form("register"):
    st.markdown("#### Enter your informations")
    email = st.text_input("Email")
    pswd = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login", on_click=on_click)

# st.title("Login")
# c1, c2, c3 = st.columns([2,2,1])
# email = c1.text_input("Username:", "")
# pswd = c2.text_input("Password:", "", type="password")

try:
    jwt_response = requests.post(urls.login, data={"username": email, "password": pswd})

    if jwt_response.status_code == 200:
        token = jwt_response.json()['access_token']
        st.session_state["correct_password"] = True
        st.session_state["token"] = token
    else:
        st.session_state["correct_password"] = False
    # c3.markdown("")
    # c3.markdown("")
    # c3.button("Login", on_click=on_click)
except Exception as e:
    st.exception(e)
    mkd = """Please set the user and password."""
    st.error(mkd)

