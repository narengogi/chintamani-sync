import uuid

def create_chintamani_node(data, label_key):
    data['id'] = str(uuid.uuid4())
    data['title'] = data[label_key]
    del data[label_key]
    return {key: value for key, value in data.items() if value is not None}