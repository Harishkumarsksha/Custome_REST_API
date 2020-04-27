from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from django.core.serializers import serialize
from API_App.models import EmployeeData
from API_App.mixins import serializedata, render_to_http_response
from API_App.utils import is_json
from API_App.forms import EmployeeForm


def GetallRecords(request):
    emp = EmployeeData.objects.all()
    # emp_data = {'eno': emp.eno, 'ename': emp.ename,
    #             'esal': emp.esal, 'eaddr': emp.eaddr}
    # json_data = json.dumps(emp)

    emp_data = serializedata(emp)
    # return JsonResponse(emp_data)
    return render_to_http_response(emp_data)


def get(request, id):
    try:
        qs = get_object_by_id(id)
    except Employee.DoesNotExist:
        json_data = json.dumps(
            {'msg': 'the required resource not available'})
        return render_to_http_response(json_data, status=404)

    else:
        json_data = serializedata([qs, ])
        # json_data = serialize('json', [emp, ])

        # provide the status code to the response
        # return HttpResponse(json_data, content_type='application/json', status=200)
        return render_to_http_response(json_data)


def get_object_by_id(id):
    try:
        emp = EmployeeData.objects.get(id=id)
    except Employee.DoesNotExist:
        emp = None
    return emp


@csrf_exempt
def put(request, id):

    emp = get_object_by_id(id)

    if emp is None:
        json_data = json.dumps(
            {'msg': 'No Matched Resource found ,Not possible to performe updattion'})
        return render_to_http_response(json_data, status=404)

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
            return render_to_http_response(json_data)

        if form.errors:
            json_data = json.dumps(form.errors)
            return render_to_http_response(json_data, status=404)
    else:
        json_data = json.dumps({'msg': 'please send valid data'})
        return render_to_http_response(json_data, status=404)


@csrf_exempt
def post(request):
    data = request.body
    # empdata = json.loads(data)
    if is_json(data):

        empdata = json.loads(data)
        # create the employee form object by the provided data
        form = EmployeeForm(empdata)

        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({'msg': 'this resource is created '})
            return render_to_http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return render_to_http_response(json_data, status=404)

        json_data = json.dumps({'msg': 'this is data is valid'})
        return render_to_http_response(json_data)
    else:
        json_data = json.dumps({'msg': 'please send valid data'})
        return render_to_http_response(json_data, status=404)


@csrf_exempt
def delete(request, id):
    emp = get_object_by_id(id)

    if emp is None:
        json_data = json.dumps(
            {'msg': 'No Matched Resource found ,Not possible to performe updattion'})
        return self.render_to_http_response(json_data, status=404)

    else:
        status, deleted_item = emp.delete()

        if status == 1:
            json_data = json.dumps(
                {'msg': 'the selected resource is deleted'})
            return render_to_http_response(json_data)
        else:
            json_data = json.dumps(
                {'msg': 'the selected resource is not deleted deleted tryagian'})
            return render_to_http_response(json_data)
