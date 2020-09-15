import requests
import os

def get(url):
    base_url = os.getenv("CANVAS_BASE_URL")
    auth_token = os.getenv("CANVAS_ACCESS_TOKEN")
    r = requests.get(
        base_url + "/" + url,
        headers={ "Authorization" : f"Bearer {auth_token}" },)
    return r.json()
