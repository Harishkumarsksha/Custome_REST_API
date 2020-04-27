import requests
import json
from faker import Faker

fake = Faker()

BASE_URL = 'http://127.0.0.1:8000/'

END_POINT = 'employee/api/'


def get_resource(id):
    # data = {}

    # if id is not None:
    #     data = {
    #         'id': id,
    #     }

    resp = requests.get(BASE_URL+END_POINT+'get/', str(id)+'/')

    # print(resp.statuscode)
    print(resp.json())


def get_all():

    resp = requests.get(BASE_URL+END_POINT)
    print(resp.json())


def create_resource():
    new_emp = {'eno': fake.random_int(), 'ename': fake.name(),
               'esal': fake.random_int(1000, 10000000), 'eaddr': fake.address()}

    json_data = json.dumps(new_emp)
    resp = requests.post(BASE_URL+END_POINT + 'post/', data=json_data)
    print(resp.status_code)
    print(resp.json())


def update_resource(id):
    new_emp = {

        'ename': 'Jhon',
        'eaddr': 'norway',

    }
    json_data = json.dumps(new_emp)
    resp = requests.put(BASE_URL+END_POINT + 'put/' +
                        str(id)+'/', data=json_data)
    print(resp.status_code)
    print(resp.json())


def delete_resource(id):
    resp = requests.delete(BASE_URL+END_POINT + 'delete/' + str(id)+'/')
    print(resp.status_code)
    print(resp.json())


# get_resource()


# get_all()

# create_resource()

# update_resource(1)
# delete_resource(1)


choise = int(input('please enter the api choise you want to performe\
                    1.get_resource\
                    2.create_resource\
                    3.update_resource\
                    4.delete_resource\
                    5.get_all\
                    \n'))
if choise == 1:
    id = int(input('enter id\n'))
    get_resource(id)
elif choise == 2:
    num = int(input('Number of records wants to create '))
    for _ in range(num):
        create_resource()
elif choise == 3:
    id = int(input('enter id\n'))
    update_resource(id)
elif choise == 4:
    id = int(input('enter id\n'))
    delete_resource(id)
else:
    get_all()
