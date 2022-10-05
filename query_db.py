import requests
import pandas as pd
from app.components.endpoints import urls

url_local = "http://localhost:8001/api/v1/project/query/"
response = requests.get(url_local)  # urls.query


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


result = get_df(response)
result = result.drop(columns=["files"])
print(result.columns)
print(result)
