import requests

def get_tests():
    url = "http://172.23.238.238/api/tests"
    response = requests.get(url)

    print(response.status_code)
    print(response.json())

def post_test():
    url = 'http://172.23.238.238/api/tests/'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "name": "sdfsdf",
        "description": "sdfsdf",
        "price": 123123123
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def update_test(num):
    url = f'http://172.23.238.238/api/tests/{num}'
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        "name": "update_tset",
        "description": "update_test",
        "price": 12380
    }

    response = requests.put(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

def delete_test():
    pass

update_test(1)


