import streamlit as st
import requests, json
from io import StringIO, BytesIO
from components.endpoints import urls
from requests_toolbelt import MultipartEncoder


st.title("Upload page")

st.header("1- Upload metadata files")
uploaded_md_file = st.file_uploader("Upload your metadata json file", type="json")
if uploaded_md_file is not None:
    data = json.load(uploaded_md_file)
    st.write(data)
if st.button("Load Metadata"):
    headers = {
        "Authorization": "Bearer " + st.session_state["token"],
        "Content-Type": "application/json",
    }
    proj_metadata_response = requests.post(
        urls.post_metadata, headers=headers, data=json.dumps(data)
    )
    if proj_metadata_response.status_code == 200:
        st.success("Metadata uploaded successfully!")
        st.session_state["proj_id"] = proj_metadata_response.json()["inserted_id"]
    elif proj_metadata_response.status_code == 422:
        st.error("Metadata not uploaded. Validation error.")
    else:
        st.error("Metadata upload failed!")


st.write("\n")

st.header("2- Upload data file")
uploaded_file = st.file_uploader("Upload your data file")
if uploaded_file is not None:
    st.text(
        "File name: {}\nType: {}\nSize: {}".format(
            uploaded_file.name, uploaded_file.type, uploaded_file.size
        )
    )
if st.button("Load Data") and uploaded_file != None:

    f = BytesIO(uploaded_file.getvalue())
    f.seek(0)
    m = MultipartEncoder(fields={"file": (uploaded_file.name, f, uploaded_file.type)})
    headers = {
        "Authorization": "Bearer " + st.session_state["token"],
        "Content-Type": m.content_type,
    }
    proj_data_response = requests.post(
        urls.post_file
        + st.session_state["proj_id"]
        + "&file_name="
        + uploaded_file.name,
        headers=headers,
        data=m,
    )
    if proj_data_response.status_code == 200:
        st.success("Data uploaded successfully!")
        st.text(proj_data_response.text)
    elif proj_data_response.status_code == 422:
        st.error("Metadata not uploaded. Validation error.")
        st.text(proj_data_response.json())
    else:
        st.error("Metadata upload failed!")
