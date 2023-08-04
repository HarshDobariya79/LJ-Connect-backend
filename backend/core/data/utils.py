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


def permissions_assign(obj, keys, value):
    try:
        original_obj = obj
        for idx in range(len(keys) - 1):
            tmp = obj.get(keys[idx])
            if not tmp:
                obj[keys[idx]] = {}
            obj = obj[keys[idx]]
        obj[keys[len(keys) - 1]] = value

    except Exception as e:
        pass
