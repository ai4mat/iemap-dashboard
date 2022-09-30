import streamlit as st
import streamlit_book as stb

# Set wide display
st.set_page_config(layout="wide")

# Check if view is admin
if "admin_view" in st.session_state:
    admin_view = st.session_state["admin_view"]
#    authToken = st.session_state["token"]
else:
    admin_view = False

# Check if query param
query_params = st.experimental_get_query_params()
if "view" in query_params:
    if query_params["view"][0] == "admin":
        stb.render_file("public/login.py")
else:
    # Set private and public views
    if admin_view:
        stb.set_book_config(
                menu_title="Authenticated User",
                menu_icon="public",
                options=[
                    "Upload page",    
                    "Logout", 
                    ], 
                paths=[
                    "private/upload.py", 
                    "private/logout.py", 
                    ],
                save_answers=False,
                styles={
                    "nav-link": {"--hover-color": "#aaddcc"},
                    "nav-link-selected": {"background-color": "#00c090"},
                }
                )
    else:
        stb.set_book_config(
                menu_title="Welcome",
                menu_icon="private",
                options=[
                    "Home", 
                    "Register",  
                    "Login", 
                    ], 
                paths=[
                    "public/home.py", 
                    "public/register.py",
                    "public/login.py", 
                    ],
                save_answers=False,
                styles={
                    "nav-link": {"--hover-color": "#e9f6fb"},
                    "nav-link-selected": {"background-color": "#87CEEB"},
                }
                )        

# Add floating button
#stb.floating_button("https://www.enea.it/it", "chat-left-dots-fill", "white", "red")
#stb.floating_button("https://www.enea.it/it", "info-fill", "white", "red")