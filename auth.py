import requests as r
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import json
import base64


def basicauth():
    url = "https://httpbin.org/basic-auth/user/passwd"
    resp = r.get(url, auth=HTTPBasicAuth("user", "passwd"))
    print("Basic Authentication:", resp.status_code, resp.json())


def digestauth():
    url = "https://httpbin.org/digest-auth/auth/user/passwd"
    resp = r.get(url, auth=HTTPDigestAuth("user", "passwd"))
    print("Digest Authentication:", resp.status_code, resp.json())


def bearer():
    url = "https://httpbin.org/bearer"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"
    headers = {"Authorization": f"Bearer {token}"}
    resp = r.get(url, headers=headers)
    print("Bearer: ", resp.status_code, resp.json())

    if resp.status_code == 200:
        print("Расшифровка:")
        payload = token.split('.')[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = json.loads(base64.b64decode(payload).decode('utf-8'))
        print(json.dumps(decoded, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    basicauth()
    bearer()
    digestauth()