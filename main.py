import re

from fastapi import FastAPI, Request


app = FastAPI()


def parse_key_string_to_list(s: str):
    parts = re.findall(r"\[([^\]]+)\]", s)
    parts.insert(0, s.split("[")[0])
    return parts


def parse_list_to_dict(lst: list[str], value: str):
    result = None

    for key in reversed(lst):
        if key.isdigit():
            result = [value] if result is None else [result]
        else:
            result = {key: value} if result is None else {key: result}

    return result


def merge_dicts(*dicts):
    def merge(a, b):
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    merge(a[key], b[key])
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    a[key].extend(b[key])
                elif isinstance(a[key], list):
                    a[key].append(b[key])
                elif isinstance(b[key], list):
                    b[key].insert(0, a[key])
                    a[key] = b[key]
                else:
                    a[key] = [a[key], b[key]]
            else:
                a[key] = b[key]

    result = {}
    for d in dicts:
        merge(result, d)

    return result


@app.get("/")
def root(request: Request):
    params = request.query_params
    endpoint_query_parameters = list()

    for key, value in params.items():
        args = parse_key_string_to_list(key)
        dictionary = parse_list_to_dict(args, value)
        endpoint_query_parameters.append(dictionary)

    result = merge_dicts(*endpoint_query_parameters)
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
