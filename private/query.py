import streamlit as st



#2022-11-20T11:26:55.952000

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

def get_df2(response):
    import pandas as pd
    
    list_doc = []
    for doc in response.json():
        dt = get_date(doc["date_creation"])
        current_doc = {
            "iemap_id": doc.get("iemap_id", None),
            "project": doc.get("project_name", None),
            "formula": doc.get("material", None),
            "created at": dt
            }
        list_doc.append(current_doc)
    df = pd.DataFrame(list_doc)
    return df
    

# def on_click():
#     from components.endpoints import urls
#     import requests

#     response = requests.get(urls.query)
#     df = get_df(response)

#     st.dataframe(df)


def get_date(datestring):
    from datetime import datetime 
    if datestring == None:
        return None
    else:
        return datetime.strptime(datestring, "%Y-%m-%d")


st.title("Query DB")
#st.markdown("Click button to query the Database")

tab1, tab2 = st.tabs(["All Projects", "Your Projects"])

with tab1:
    st.header("All Projects")
    if st.button("Get all data"):
        from components.endpoints import urls
        import requests

        response = requests.get(urls.query)
        df = get_df(response)

        st.dataframe(df, use_container_width=True)

with tab2:
    st.header("Your Projects")        
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
            
            df = get_df2(response)
            st.dataframe(df, use_container_width=True)
        else:
            st.write(f"An error occurred!")


