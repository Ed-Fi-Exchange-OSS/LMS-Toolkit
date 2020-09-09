import requests
import os
import jwt
import time


def get(url):
    base_url = os.getenv("ZOOM_BASE_URL")
    auth_token = generate_jwt(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    r = requests.get(
        f"{base_url}/{url}",
        headers={"Authorization": f"Bearer {auth_token}"},)
    print(auth_token)
    return r.json()


def generate_jwt(key, secret):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"iss": key, "exp": int(time.time() + 3600)}
    token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
    return token.decode("utf-8")
