import requests


def download(url: str):
    data = requests.get(url)
    if data.ok:
        return data.content
    return None
