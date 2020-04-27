import json
from django.core.serializers import serialize
from django.http import HttpResponse


def serializedata(qs):
    json_data = serialize('json', qs)
    p_data = json.loads(json_data)
    final_list = []
    for obj in p_data:
        emp_data = obj['fields']
        final_list.append(emp_data)
    json_data = json.dumps(final_list)
    #json_data = final_list
    return json_data


def render_to_http_response(json_data, status=200):
    return HttpResponse(json_data, content_type='text/json', status=status)
