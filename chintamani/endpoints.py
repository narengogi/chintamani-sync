import requests
import os
import json


def insert_child(child_label, child_json, parent_path, relationship):
    url = os.getenv("CHINTAMANI_API_URL") + "/api/data-sync/child"
    headers = {"Content-Type": "application/json"}
    data = {"label": child_label, "data": json.dumps(child_json), "parentPath": parent_path, "relationship": relationship}
    response = requests.post(url, headers=headers, json=data)
    return response
