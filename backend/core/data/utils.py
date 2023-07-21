import json

def delete_empty_keys(data):
    if isinstance(data, dict):
        for key in list(data.keys()):
            if isinstance(data[key], dict):
                delete_empty_keys(data[key])
                if not data[key]:
                    del data[key]
            elif isinstance(data[key], list):
                for item in data[key]:
                    delete_empty_keys(item)
    elif isinstance(data, list):
        for item in data:
            delete_empty_keys(item)