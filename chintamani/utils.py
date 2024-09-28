import uuid

def create_node(data, label_key):
    data['uuid'] = str(uuid.uuid4())
    data['title'] = data[label_key]
    return {key: value for key, value in data.items() if value is not None}