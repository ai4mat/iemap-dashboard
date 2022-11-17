import streamlit as st


st.write("# Welcome to IEMAP ⚛️")


video_file = open('files/register.m4v', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)


st.markdown(
    """
    This is a small *PoC* of **IEMAP Platform**. It includes just the _register_, _login_ and _upload_ features. It also includes a _query_ feature, but it is not fully implemented yet.
    
    ### Register page

    To register a new user, you need to fill the form with your email and password. The password must have at least 8 characters, one uppercase letter, one lowercase letter and one number.
    Once the user is registerd, it will receive an ativation email. The user must click on the link to activate the account.
    
    Once the activation is done, the user can login with the email and password.
    
    ### Login page
    You can login with the email and password. If the login is successful, you will be redirected to the upload data page.
    
    ## Authenticated users only!
    ### Upload data page
    In this page you can upload the metadata json file and project related files. 
    
    ### Query data page
    Just a simple query to the database to get all the data.
    
"""
)