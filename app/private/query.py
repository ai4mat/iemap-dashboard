import streamlit as st
import pandas as pd


def get_df(response):
    list_doc = []
    get_file_info = lambda x: x["name"] + "." + x["extention"] + " (" + x["size"] + ")"
    get_name_value = lambda x: x["name"] + ":" + str(x["value"])
    for doc in response.json():
        provenance = doc["provenance"]
        isExperiment = bool(doc["process"]["isExperiment"])
        current_doc = {
            "iemap_id": doc.get("iemap_id", None),
            "email": provenance["email"],
            "affiliation": provenance["affiliation"],
            "created_at": provenance.get("created_at", None),
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


def on_click(nr, nc):

    from app.components.endpoints import urls

    # import numpy as np
    import requests

    response = requests.get(urls.query)
    df = get_df(response)
    # pd.DataFrame(
    #     np.random.randn(nr, nc),
    #     columns=('col %d' % i for i in range(nc)))
    st.dataframe(df)


st.title("Query DB")
st.markdown("Click button to query DB and get all data")

n_row = st.number_input("Number of rows", 1, 100, 10)
n_col = st.number_input("Number of columns", 1, 100, 10)
choose = st.button("Query")
if choose:
    on_click(n_row, n_col)


# https://discuss.streamlit.io/t/how-to-set-page-config-default-layout-to-wide-without-calling-set-page-config/13872/2
