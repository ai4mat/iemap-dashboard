import streamlit as st
def login(email, pswd):
    import time
    from components.endpoints import urls
    import requests

    try:
        jwt_response = requests.post(
            urls.login, data={"username": email, "password": pswd}
        )
        if jwt_response.status_code == 200:
            token = jwt_response.json()["access_token"]
            st.session_state["correct_password"] = True
            st.session_state["token"] = token
        else:
            st.session_state["correct_password"] = False
    except Exception as e:
        st.exception(e)
        mkd = """Please set the user and password."""
        st.error(mkd)
    if st.session_state["correct_password"]:
        st.session_state["admin_view"] = True
        time.sleep(0.25)
        query_dict = {}
        st.experimental_set_query_params(**query_dict)
    else:
        st.warning("Wrong username or password")


st.title("Login")
c1, c2, c3 = st.columns([2, 2, 1])
email = c1.text_input("Username:", "")
pswd = c2.text_input("Password:", "", type="password")
c3.markdown("")
c3.markdown("")
c3.button("Login", on_click=login, args=(email, pswd))
