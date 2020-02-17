import click
import requests
import urllib

ENDPOINT = "https://api.clockify.me/api/"
HEADERS = {
    "X-Api-Key": None,
    }

def set_api(api_key):
    HEADERS["X-Api-Key"] = api_key

def name_or_id_to_id(name, name_to_id):
    try:
        # name is a valid name
        return name_to_id[name]
    except KeyError:
        for valid_id in name_to_id.values():
            if valid_id == name:
                # name is a valid id
                return valid_id
        raise ValueError(f"Given name {name} is not a valid name or id")

def call(path, json={}, method="GET", response_required=True):
    rq = getattr(requests, method.lower(), None)
    if rq == None:
        raise click.UsageError(f"Cannot perform http request with {method} method")

    params = None
    if method=="GET":
        params=json
    url = urllib.parse.urljoin(ENDPOINT, path)
    #print('DEBUGG: ', url)
    #print('DEBUG: ', json)
    try:
        r = rq(url, json=json, headers=HEADERS, params=params)
        if (r.status_code // 100) * 100 != 200:
            click.echo(f"DEBUGGG: {r.text}")
            return None, r.status_code
    except requests.exceptions.RequestException as e:
        raise click.UsageError(f"Cannot load requested api endpoint {path} with data {json}. Call failed with the following error: {str(e)}")

    try:
        return r.json(), r.status_code
    except ValueError:
        if response_required:
            raise click.UsageError(f"Cannot decode response body as json {method} {url} [{json}]")
        return None, r.status_code

