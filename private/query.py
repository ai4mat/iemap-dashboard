import streamlit as st


def get_df(response):
    import pandas as pd
    from datetime import datetime
    
    list_doc = []
    get_file_info = lambda x: x["name"] + "." + x["extention"] + " (" + x["size"] + ")"
    get_name_value = lambda x: x["name"] + ":" + str(x["value"])
    for doc in response.json():
        provenance = doc["provenance"]
        dt = datetime.fromisoformat(provenance["createdAt"])
        isExperiment = bool(doc["process"]["isExperiment"])
        current_doc = {
            "iemap_id": doc.get("iemap_id", None),
            "affiliation": provenance["affiliation"],
            "created at": dt.date(),
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

def get_df2(response):
    import pandas as pd
    from datetime import datetime
    
    list_doc = []
    for doc in response.json():
        dt = datetime.fromisoformat(doc["date_creation"])
        current_doc = {
            "iemap_id": doc.get("iemap_id", None),
            "project": doc.get("project_name", None),
            "formula": doc.get("material", None),
            "created at": dt.date()
            }
        list_doc.append(current_doc)
    df = pd.DataFrame(list_doc)
    return df
    





st.title("Query DB")

tab1, tab2 = st.tabs(["All Projects", "Your Projects"])

with tab1:
    st.header("All Projects")
    with st.spinner("Loading data..."):
        if st.button("Get all data"):
            from components.endpoints import urls
            import requests

            response = requests.get(urls.query)
            if response.status_code == 200:
                df = get_df(response)
                st.dataframe(df, use_container_width=True)
            else:
                st.write(f"An error occurred!")

with tab2:
    st.header("Your Projects") 
    with st.spinner("Loading data..."):       
        if st.button("Get your data"):
            from components.endpoints import urls
            import requests

            response = requests.get(
                urls.get_user_projects_info,
                headers={"Authorization": f"Bearer "+st.session_state["token"]}
            )
            if response.status_code == 200:           
                df = get_df2(response)
                st.dataframe(df, use_container_width=True)
            else:
                st.write(f"An error occurred!")


