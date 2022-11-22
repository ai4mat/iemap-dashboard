import streamlit as st
from components.endpoints import urls
import requests

url = urls.query+str(st.session_state["project_id"])
response = requests.get(
    url,
    headers={"Authorization": f"Bearer "+st.session_state["token"]}
)

st.title("Project: " + str(response["project_name"]))
st.json(response.json())
