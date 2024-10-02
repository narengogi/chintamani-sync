import requests
import os
import json


def insert_child(child_label, child_json, parent_path, relationship, parent_title=None):
    url = os.getenv("CHINTAMANI_API_URL") + "/api/data-sync/child"
    headers = {"Content-Type": "application/json"}
    data = {"label": child_label, "data": json.dumps(child_json), "parentPath": parent_path, "relationship": relationship, "parentTitle": parent_title}
    data = {k: v for k, v in data.items() if v is not None}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(response.json())
    return response
