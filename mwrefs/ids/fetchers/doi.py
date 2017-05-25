import requests

CITOID_HOST = 'https://citoid.wikimedia.org'


def lookup_via_citoid(doi):
    url = CITOID_HOST + "/api"
    params = {
        'format': "mediawiki",
        'search': doi
    }
    response = requests.get(url, params=params)
    doc = response.json()
    if 'Error' in doc:
        raise RuntimeError(doc['Error'])
    else:
        return doc


def lookup_via_doidotorg(doi):
    url = "http://doi.org"
    data = {
        "hdl": doi
    }
    response = requests.post(
        url, data=data, headers={'Accept': "application/json"})
    if response.status_code == 404:
        raise RuntimeError("DOI not found")
    elif response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError("Unknown error")

METHODS = {
    'doi.org': lookup_via_doidotorg,
    'citoid.wikimedia.org': lookup_via_citoid
}


def lookup(doi, methods=['doi.org']):
    for i, method in enumerate(methods):
        try:
            return METHODS[method](doi)
        except RuntimeError as e:
            if i+1 == len(methods):
                raise e
            else:
                continue
