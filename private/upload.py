import streamlit as st
import requests, json
from io import BytesIO
from components.endpoints import urls
from requests_toolbelt import MultipartEncoder


st.title("Upload page")

st.header("1- Upload metadata file")
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

st.header("2- Upload data files")
uploaded_files = st.file_uploader("Upload your project data files", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    st.text(
        "File name: {}\nType: {}\nSize: {}".format(
            uploaded_file.name, uploaded_file.type, uploaded_file.size
        )
    )
if st.button("Load Data") and uploaded_files != None:
    for uploaded_file in uploaded_files:
        # f = BytesIO(uploaded_file.getvalue())
        with BytesIO(uploaded_file.getvalue()) as f:
            file_data = f.read()
            st.session_state["file_to_upload"] = file_data
            # st.session_state["proj_id"] = "633ad6ef7550f1c6479b4e5d"

            m = MultipartEncoder(
                fields={
                    "file": (
                        uploaded_file.name,
                        st.session_state.file_to_upload,
                        uploaded_file.type,
                    )
                }
            )
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
