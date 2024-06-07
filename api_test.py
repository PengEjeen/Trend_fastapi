import requests

def create_user():
    url = 'http://127.0.0.1:8000/createUser/'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "user_id": "chony96",
        "password": "test"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def login():
    url = 'http://127.0.0.1:8000/login/'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "user_id": "chony96",
        "password": "test"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

login()



