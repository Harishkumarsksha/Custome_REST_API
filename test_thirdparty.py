import requests
import json

BASE_URL = 'http://127.0.0.1:8000/'

END_POINT = 'api/'


def get_resource(id=None):
    data = {}

    if id is not None:
        data = {
            'id': id,
        }

    resp = requests.get(BASE_URL+END_POINT, data=json.dumps(data))

   # print(resp.statuscode)
    print(resp.json())


def get_all():

    resp = requests.get(BASE_URL+END_POINT)
    print(resp.json())


def create_resource():
    new_emp = {

        'eno': 600,
        'ename': 'rana',
        'esal': 15000,
        'eaddr': 'Delih',

    }
    json_data = json.dumps(new_emp)
    resp = requests.post(BASE_URL+END_POINT, data=json_data)
    print(resp.status_code)
    print(resp.json())


def update_resource(id):
    new_emp = {
        'ename': 'ravi',
        'esal': 1500000000,

    }
    json_data = json.dumps(new_emp)
    resp = requests.put(BASE_URL+END_POINT + str(id)+'/', data=json_data)
    print(resp.status_code)
    print(resp.json())


def delete_resource(id):
    resp = requests.delete(BASE_URL+END_POINT + str(id)+'/')
    print(resp.status_code)
    print(resp.json())


get_resource()


# get_all()

# create_resource()

# update_resource(1)
delete_resource(1)
