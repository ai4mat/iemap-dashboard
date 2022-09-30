######################################
# Example on how using API endpoints
######################################
from this import d
from requests_toolbelt import MultipartEncoder
import requests
from os.path import dirname, abspath, join, isfile
from enum import Enum
import json
from typing import List, Optional
from PyQt5.QtWidgets import QFileDialog

# Enum for each endpoint
class endpoints(Enum):
    base_url = "http://0.0.0.0:8001/api/"
    get_token = f"{base_url}v1/health/jwt"
    check_auth = f"{base_url}v1/health/checkauth"
    post_metadata = f"{base_url}v1/project/add"
    post_project_file = f"{base_url}v1/project/add/file/"
    post_property_file = f"{base_url}v1/project/add/propertyfile/"
    get_file = f"{base_url}v1/files"
    get_data_paginated = f"{base_url}v1/project/list/"
    get_proc_properties = f"{base_url}v1/project/file/list/"
    # endpoints to use in MULTI-PART FORM DATA
    post_form_data_project_file = f"{base_url}v1/project/add_file_and_data"
    post_form_data_property_file = f"{base_url}v1/project/add_property_file_and_data"


# CREDENTIALS to get JWT
paylod_user_account = {
    "fullname": "AI4Mat USER",
    "email": "ai4mat@enea.it",
    "affiliation": "ENEA",
}

# POST CREDENTIALS (AUTHENTICATE USER) as JSON and get JWT
jwt_response = requests.post(
    endpoints.get_token.value,
    json=paylod_user_account,
)

# if credentials are correct, the response is a JWT
if jwt_response.status_code == 200:
    token = jwt_response.json()
    # print JWT
    print(f"Succefully got JWT:\n{json.dumps(token, indent=4)}")
    print("Checking auth...", end="")

    # USE JWT to check test authentication
    auth_response = requests.get(
        endpoints.check_auth.value,
        headers={"Authorization": f"Bearer {token['access_token']}"},
    )
    if auth_response.status_code == 200:
        print("GRANTED!!")
        print(json.dumps(json.loads(auth_response.text), indent=4))


# POST METADATA as JSON

add_project_metadata = True
payload_metadata = {
    "user": {"email": "user1@cnr.it", "affiliation": "CNR"},
    "project": {
        "name": "Battery Project CNR",
        "description": "Descrizione estesa",
        "label": "BPJ CNR",
    },
    "projectWP": "WP Battery Test",
    "process": {
        "isExperiment": "False",
        "isSimulation": "True",
        "parameters": [{"name": "param1", "type": "type 1", "value": 45465.9}],
        "calculation": {
            "method": "method1",
            "swAgent": {"name": "Orcad", "version": "1.0.5"},
        },
        "experiment": {
            "method": "exp method 1",
            "swAgent": {"name": "software1", "version": "4.7"},
        },
        "material": {
            "formula": "CO2-NO2-Zn",
            "elements": ["Zn", "NO2", "CO2"],
            "chemicalComposition": [{"element": "O2", "percentage": "20%"}],
            # INPUT AND OUTPUT ARE OPTIONAL
            # # "input": {
            # #     "lattice": {
            # #         "a": "11.050",
            # #         "b": "10365",
            # #         "c": "5.635",
            # #         "alpha": "81.59",
            # #         "beta": "68.114",
            # #         "gamma": "30296",
            # #     },
            # #     "sites": "[ [x1,y1,z1], [x2, y2, z2], [x3, y3, z3] ]",
            # #     "species": "[H,H,H]",
            # # },
            # # "output": {
            # #     "lattice": {
            # #         "a": "11.050",
            # #         "b": "10365",
            # #         "c": "5.635",
            # #         "alpha": "81.59",
            # #         "beta": "68.114",
            # #         "gamma": "30296",
            # #     },
            # #     "sites": "[ [x1,y1,z1], [x2, y2, z2], [x3, y3, z3] ]",
            # #     "species": "[H,H,H]",
            # },
        },
        "properties": [
            {
                "name": "Prop 1",
                "type": "2D",
                "axis": {"labelX": "Wavelength", "labelY": "Transmittance"},
                "value": 255.89,
                "units": {"x": "UnitX", "y": "UnitY"},
                "isCalculated": "True",
                "isPhysical": "False",
            }
        ],
        "iemapID": "iemap-1",
    },
    "files": [
        {
            "description": "Proj file 1",
            "name": "File di progetto 1",
            "extention": "cif",
            "type": "Code",
            "isProcessed": "False",
            "size": "10Mb",
            "publication": {"name": "Research paper", "date": "2022-04-25"},
            "url": "https://elsevier/fjhasgjhdf",
        }
    ],
    # "_v": "1.0",
}
if add_project_metadata:
    proj_metadata_response = requests.post(
        endpoints.post_metadata.value,
        # json=payload_metadata
    )
    if proj_metadata_response.status_code == 200:
        print(
            f"Succefully added project metadata:\n{json.dumps( proj_metadata_response.json(), indent=4)}"
        )
    else:
        print(
            f"Error adding project metadata:\n{json.dumps( proj_metadata_response.json(), indent=4)}"
        )


# POST PROJECT FILE
# AFTER METADATA IS ADDED, POST PROJECT FILE by providing the project id and the file name
# file name already exists in the project
add_project_file = False

if add_project_file:
    # read file from file system
    test_file = open("./mi-paper.pdf", "rb")
    # set file name as already in document in DB
    test_file_name = "TEST 2"
    id_project_doc = (
        proj_metadata_response.json()["inserted_id"]
        if "proj_metadata_response" in locals()
        else "62761c48856da47202945e05"
    )

    print(
        f'\nSENDING POST request to: {endpoints.post_project_file.value +"?project_id="+ str(id_project_doc)+"&file_name="+test_file_name}'
    )

    m = MultipartEncoder(
        fields={"file": ("mi-paper.pdf", test_file, "application/pdf")}
    )

    response = requests.post(
        endpoints.post_project_file.value
        + "?project_id="
        + str(id_project_doc)
        + "&file_name="
        + test_file_name,
        data=m,
        headers={"Content-Type": m.content_type},
    )
    if response.status_code == 200:
        print(
            f"Succefully added project file:\n{json.dumps( response.json(), indent=4)}"
        )
    else:
        print(f"Error adding project file:\n{json.dumps(response.json(), indent=4)}")


# POST PROPERTY FILE
# AFTER METADATA IS ADDED, POST PROPERTY FILE by providing the project id and property name and type
add_proc_property_file = False

if add_proc_property_file:
    # read file from file system
    test_file = open("./mi-paper.pdf", "rb")
    prop_name = "proprietà 3"
    prop_type = "tipo 3"
    id_project_doc = (
        proj_metadata_response.json()["inserted_id"]
        if "proj_metadata_response" in locals()
        else "62761c48856da47202945e05"
    )

    # ${'local_url'}v1/project/add/propertyfile/?project_id=62a99caa080ad5fcec6f93a8&property_name=H2o&property_type=2D
    print(
        f"\nSENDING POST request to: {endpoints.post_property_file.value}"
        + "?project_id="
        + str(id_project_doc)
        + "&property_name="
        + prop_name
        + "&property_type="
        + prop_type
    )

    m = MultipartEncoder(
        fields={"file": ("mi-paper.pdf", test_file, "application/pdf")}
    )

    response = requests.post(
        endpoints.post_property_file.value
        + "?project_id="
        + str(id_project_doc)
        + "&property_name="
        + prop_name
        + "&property_type="
        + prop_type,
        data=m,
        headers={"Content-Type": m.content_type},
    )

    if response.status_code == 200:
        print(
            f"Succefully added process property file:\n{json.dumps( response.json(), indent=4)}"
        )
    else:
        print(
            f"Error adding process property file:\n{json.dumps(response.json(), indent=4)}"
        )


# TO POST METADATA AND FILE THERE ARE THREE POSSIBLE SOLUTIONS:

# 1) Base64 encode the file, at the expense of increasing the data size by around 33%,
#    and add processing overhead in both the server and the client for encoding/decoding.
#    HTML FORM MULTI-PART
# 2) Send the file first in a multipart/form-data POST, and return an ID to the client.
#    The client then sends the metadata with the ID, and the server re-associates the file and the metadata.
# 3) Send the metadata first, and return an ID to the client.
#    The client then sends the file with the ID, and the server re-associates the file and the metadata.


# USE MULTI-PART FORM DATA to upload project files and metadata

# TO ADD FORM DATA & FILE IS NECESSARY TO USE https://github.com/requests/toolbelt
# https://toolbelt.readthedocs.io/en/latest/
# https://toolbelt.readthedocs.io/en/latest/user.html?highlight=multipart%20encoder#multipart-form-data-encoder


# DEFINE METADATA AND FILE TO ADD TO PROJECT
m_project = MultipartEncoder(
    fields={
        "fileupload": "gnn_benchmark.pdf",
        "name": "Articolo test1",
        "description": "GNN benckmark pubblication",
        "type": "Code",
        "isProcessed": "False",
        "publication_name": "Articolo 5",
        "publication_date": "2022-01-01",
        "publication_url": "https://www.enea.it",
        "fileupload": (
            "gnn_benckmark.pdf",
            open("./gnn_benchmark.pdf", "rb"),
            "application/pdf",
        ),
    }
)


docID = "62a99b84bee73ad702301579"

addFileProject = False
addProperty = False

if addFileProject:
    add_proj_file_multi_part_response = requests.post(
        # build full url with docID
        endpoints.post_form_data_project_file.value + "/" + docID,
        # Multipart data
        data=m_project,
        headers={"Content-Type": m_project.content_type},
        verify=False,
    )
    if add_proj_file_multi_part_response.status_code == 200:
        print("Project file uploaded successfully!")
        print(add_proj_file_multi_part_response.text)
    else:
        print("Error while uploading project file!")
        print(add_proj_file_multi_part_response.text)


# ADD PROPERTY AND FILE TO PROJECT
# DEFINE METADATA AND FILE TO ADD TO PROPERTY
m_property = MultipartEncoder(
    fields={
        "name": "Property TEST 1",
        "type": "Moleculus",
        "unit_x": "m3",
        "unit_y": "%",
        "isCalculates": "False",
        "isPhysical": "True",
        "axis_labelX": "prediction",
        "axis_labelY": "target",
        "value": "200.78",
        "fileupload": (
            "ML_SMELL.pdf",
            open("./ML_SMELL.pdf", "rb"),
            "application/pdf",
        ),
    }
)

if addProperty:
    add_property_file_multi_part_response = requests.post(
        # build full url with docID
        endpoints.post_form_data_property_file.value + "/" + docID,
        # Multipart data
        data=m_property,
        headers={"Content-Type": m_property.content_type},
        verify=False,
    )
    if add_property_file_multi_part_response.status_code == 200:
        print("Project file uploaded successfully!")
        print(
            json.dumps(json.loads(add_property_file_multi_part_response.text), indent=4)
        )
    else:
        print("Error while uploading project file!")
        print(
            json.dumps(json.loads(add_property_file_multi_part_response.text), indent=4)
        )


# RETRIEVE A FILE (ASSOCIATED TO A PROJECT OR A PROPERTY)
downloadFile = False
if downloadFile:

    file_to_download = "19af82973b785c66c3033377eebca4513e106879.pdf"
    download_file_response = requests.get(
        # build full url with docID
        endpoints.get_file.value
        + "/"
        + file_to_download,
    )
    if download_file_response.status_code == 200:
        try:
            print(download_file_response.headers)
            open(file_to_download, "wb").write(download_file_response.content)
            print("File downloaded successfully!")

        except Exception as e:
            print(e)
            print("Error while downloading file!")

# GET ALL DATA FROM DB (PAGINATED)
getAllData = False
if getAllData:
    pageSize = 2
    pageNumber = 1

    get_all_data_response = requests.get(
        endpoints.get_data_paginated.value
        + f"?page_size={pageSize}&page_number={pageNumber}"
    )
    if get_all_data_response.status_code == 200:
        print(json.dumps(json.loads(get_all_data_response.text), indent=4))
        data = json.loads(get_all_data_response.text)["data"]

    # show a specific document/project
    print("FILTER RESULTS")
    projV2 = [p for p in data if p["project"]["name"] == "Progetto AI4MAT versione 2"]
    print(json.dumps(projV2, indent=4))


# GET ALL PROCESS PROPERTIES BY PROJECT NAME AND USER AFFILIATION
processProps = False
if processProps:
    affiliation = "ENEA"
    projName = "Progetto AI4MAT"
    get_process_properties_response = requests.get(
        endpoints.get_proc_properties.value
        + f"?affiliation={affiliation}&projectName={projName}"
    )
    if get_process_properties_response.status_code == 200:
        print(json.dumps(get_process_properties_response.json(), indent=4))


# https://stackoverflow.com/questions/4083702/posting-a-file-and-associated-data-to-a-restful-webservice-preferably-as-json
# https://stackoverflow.com/questions/3938569/how-do-i-upload-a-file-with-metadata-using-a-rest-web-service
# mime types
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
