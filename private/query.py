import streamlit as st


def get_df(response):
    import pandas as pd
    
    list_doc = []
    get_file_info = lambda x: x["name"] + "." + x["extention"] + " (" + x["size"] + ")"
    get_name_value = lambda x: x["name"] + ":" + str(x["value"])
    for doc in response.json():
        provenance = doc["provenance"]
        isExperiment = bool(doc["process"]["isExperiment"])
        current_doc = {
            "iemap_id": doc.get("iemap_id", None),
    #        "email": provenance["email"],
            "affiliation": provenance["affiliation"],
            "created at": provenance.get("createdAt", None),
            "project": doc["project"]["name"],
            "process": "Experiment" if isExperiment else "Computation",
            "method": doc["process"].get("method", None),
            "formula": doc.get("material", None).get("formula", None),
            "parameters": ", ".join([get_name_value(p) for p in doc["parameters"]])
            if doc.get("parameters", None) != None
            else None,
            "properties": ", ".join([get_name_value(p) for p in doc["properties"]])
            if doc.get("properties", None) != None
            else None,
            "files": [
                get_file_info(p)
                # p["name"] + "." + p["extention"] + " (" + p["size"] + ")"
                for p in doc["files"]
            ]
            if doc.get("files", None) != None
            else None,
        }
        list_doc.append(current_doc)
    df = pd.DataFrame(list_doc)
    return df


def on_click():
    from components.endpoints import urls
    import requests

    response = requests.get(urls.query)
    df = get_df(response)

    st.dataframe(df)



st.title("Query DB")
st.markdown("Click button to query DB and get all data")

if st.button("Get all data"):
    from components.endpoints import urls
    import requests

    response = requests.get(urls.query)
    df = get_df(response)

    st.dataframe(df, use_container_width=True)
#    on_click()

if st.button("Get your data"):
    from components.endpoints import urls
    import requests

    #ep = urls.get_user_projects_info.value
    response = requests.get(
        urls.get_user_projects_info,
        headers={"Authorization": f"Bearer "+st.session_state["token"]},
        # verify=False
    )
    if response.status_code == 200:
        docs = response
        st.echo(docs)
    else:
        print(f"An error occurred!")
    #response = requests.get(urls.get_user_projects_info+st.session_state["token"])
    #df = get_df(response)
    #st.dataframe(df, use_container_width=True)
# https://discuss.streamlit.io/t/how-to-set-page-config-default-layout-to-wide-without-calling-set-page-config/13872/2
