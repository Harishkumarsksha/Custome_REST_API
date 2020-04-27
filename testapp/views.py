from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
from testapp.models import Employee
from django.views.generic import View
import json
from django.http import HttpResponse
# from django.core.serializers import serialize # django inbuilt serializer


from testapp.mixins import SerializeMixin, HttpResponseMixin
from testapp.utils import is_json
from testapp.forms import EmployeeForm


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeDetails(View, SerializeMixin, HttpResponseMixin):

    def get_object_by_id(self, id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, id, *args, **kwargs):
        try:
            qs = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data = json.dumps(
                {'msg': 'the required resource not available'})
            return self.render_to_http_response(json_data, status=404)

        else:
            json_data = self.serialize([qs, ])
            # json_data = serialize('json', [emp, ])

            # provide the status code to the response
            # return HttpResponse(json_data, content_type='application/json', status=200)
            return self.render_to_http_response(json_data)

    def put(self, request, id, *args, **kwargs):

        emp = self.get_object_by_id(id)

        if emp is None:
            json_data = json.dumps(
                {'msg': 'No Matched Resource found ,Not possible to performe updattion'})
            return self.render_to_http_response(json_data, status=404)

        data = request.body
        valid_json = is_json(data)
        if valid_json:

            provided_data = json.loads(data)

            original_data = {
                'eno': emp.eno,
                'ename': emp.ename,
                'esal': emp.esal,
                'eaddr': emp.eaddr,
            }

            original_data.update(provided_data)
            form = EmployeeForm(original_data, instance=emp)

            if form.is_valid():
                form.save(commit=True)
                json_data = json.dumps({'msg': 'this resource is updated '})
                return self.render_to_http_response(json_data)

            if form.errors:
                json_data = json.dumps(form.errors)
                return self.render_to_http_response(json_data, status=404)
        else:
            json_data = json.dumps({'msg': 'please send valid data'})
            return self.render_to_http_response(json_data, status=404)

    def delete(self, request, id, *args, **kwargs):
        emp = self.get_object_by_id(id)

        if emp is None:
            json_data = json.dumps(
                {'msg': 'No Matched Resource found ,Not possible to performe updattion'})
            return self.render_to_http_response(json_data, status=404)

        else:
            status, deleted_item = emp.delete()

            if status == 1:
                json_data = json.dumps(
                    {'msg': 'the selected resource is deleted'})
                return self.render_to_http_response(json_data)
            else:
                json_data = json.dumps(
                    {'msg': 'the selected resource is not deleted deleted tryagian'})
                return self.render_to_http_response(json_data)


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeListCBV(View, SerializeMixin, HttpResponseMixin):

    def get(self, request, *args, **kwargs):
        try:
            qs = Employee.objects.all()
       # json_data = serialize('json', emp, fields=('eno', 'ename', 'eaddr'))

        except:
            json_data = json.dumps(
                {'msg': 'the required resource not available'})
            # return HttpResponse(json_data, content_type='application/json', status=404)
            print('###################')
            return self.render_to_http_response(json_data, status=404)
        else:

            # geting the particular employee fields
            # json_data = serialize('json', emp)
            json_data = self.serialize(qs)
            # getiing only fields
            '''final_list = []
            for data in emp:
                emp_data = data['fields']
                final_list.append(final_list)
            json_data = json.dumps(final_list)'''

            # return HttpResponse(json_data, content_type='application/json', status=200)
            return self.render_to_http_response(json_data)

    def post(self, request, *args, **kwargs):
        data = request.body

        if is_json(data):

            empdata = json.loads(data)
            # create the employee form object by the provided data
            form = EmployeeForm(empdata)

            if form.is_valid():
                form.save(commit=True)
                json_data = json.dumps({'msg': 'this resource is created '})
                return self.render_to_http_response(json_data)
            if form.errors:
                json_data = json.dumps(form.errors)
                return self.render_to_http_response(json_data, status=404)

            json_data = json.dumps({'msg': 'this is data is valid'})
            return self.render_to_http_response(json_data)
        else:
            json_data = json.dumps({'msg': 'please send valid data'})
            return self.render_to_http_response(json_data, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCRUDCBV(View, SerializeMixin, HttpResponseMixin):

    def get_object_by_id(self, id):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp = None
        return emp

    def get(self, request, *args, **kwargs):
        data = request.body

        if is_json(data):
            json_data = json.dumps(
                {'msg': 'please provide the valid json data '})
            return self.render_to_http_response(json_data, status=404)

        pdata = json.loads(data)
        id = pdata.get('id', None)
        print(id, '###################')
        if id is not None:
            emp = self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps(
                    {'msg': 'No Matched resource is not found  '})
                return self.render_to_http_response(json_data, status=404)
            json_data = self.serialize([emp, ])
            return self.render_to_http_response(json_data)

        qs = Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_response(json_data)


''' dumping the data into the datbase


1.py manage.py dumpdata testapp.employee
    empoyee data to the console 
    default format is json 


        python3 manage.py dumpda[a testapp.Employee --indent 4 
{
    "model": "testapp.employee",
    "pk": 1,
    "fields": {
        "eno": 10,
        "ename": "hari",
        "esal": "10000",
        "eaddr": "Banglore"
    }
},
{
    "model": "testapp.employee",
    "pk": 2,
    "fields": {
        "eno": 1000,
        "ename": "ashu",
        "esal": "25000",
        "eaddr": "Hydhrabadh"
    }
}
]


we can see the data in the form of the json or  xml 

python3 manage.py dumpdata testapp.Employee --format json --indent 4

python3  manage.py dumpdata testapp.Employee --format json --indent 4
[
{
    "model": "testapp.employee",
    "pk": 1,
    "fields": {
        "eno": 10,
        "ename": "hari",
        "esal": "10000",
        "eaddr": "Banglore"
    }
},
{
    "model": "testapp.employee",
    "pk": 2,
    "fields": {
        "eno": 1000,
        "ename": "ashu",
        "esal": "25000",
        "eaddr": "Hydhrabadh"
    }
}
]

for the xml fomrat 

     python3  manage.py dumpdata testapp.Employee --format xml --indent 4
<?xml version="1.0" encoding="utf-8"?>
<django-objects version="1.0">
    <object model="testapp.employee" pk="1">
        <field name="eno" type="IntegerField">10</field>
        <field name="ename" type="CharField">hari</field>
        <field name="esal" type="CharField">10000</field>
        <field name="eaddr" type="TextField">Banglore</field>
    </object>
    <object model="testapp.employee" pk="2">
        <field name="eno" type="IntegerField">1000</field>
        <field name="ename" type="CharField">ashu</field>
        <field name="esal" type="CharField">25000</field>
        <field name="eaddr" type="TextField">Hydhrabadh</field>
    </object>


    data is copied to the xml file 
    python3  manage.py dumpdata testapp.Employee --format xml >emp.xml --indent 4
    convert the emp.xml to the json data :
    python3  manage.py dumpdata testapp.Employee --format >emp.json --indent 4

    when we do the post request then csrf verification will be done if the csrf verfiuaction niot done then the third party application will throw an error 

    csrf exempt can done at :
    1.Method Level 
    2.Class Level 
    3.project level 

    1. To disable at the method level:'
    ---------------------------------
    from django.views .decoratos.csrf import csrf_exempt 

    @csrf_exempt
    def my_view(request):
        .....

    2.To disable at class level:
    ---------------------------
    from django.views.decorators.csrf import csrf_exempt
    from django.utils.decorators import method_decorator

    @method_decorator(csrf_exempt,name='dispatch')
    class Employee(View)


    3.At the the project level we need to remove the csrf middle ware:
    ----------------------------------------------------------------
    comment the csrf middle ware in the settings.py  middlewares 

    partner application is sending the data :
    ----------------------------------------
    *django views function is resposible for check the sent data in the format ?


    create the utils.py file in the testapp:

all the crud operations must be performed with the single endpoint that is the sucessfull api developent 

1.To get a particular record based on id :

http://127.0.0.1:8000/api/1

2.To get a all the records  :

http://127.0.0.1:8000/api/

3.To create new record :

http://127.0.0.1:8000/api/1

4.To update a particular record based on id :

http://127.0.0.1:8000/api/1

1.To delete a particular record based on id :

http://127.0.0.1:8000/api/1
    '''
