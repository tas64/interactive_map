import json
from django.http import HttpResponse
from imap.database import queries

def simple_request(request):
    object = {'test' : True, 'counter' : 5}
    return HttpResponse(json.dumps(object, indent=2))

def movables_objects(request):
    objects = queries.get_all_movables_objects()
    return HttpResponse(json.dumps(objects, indent=2))

def immobiles_objects(request):
    objects = queries.get_all_immobiles_objects()
    return HttpResponse(json.dumps(objects, indent=2))

def location_points_for(request, id):
    points = queries.get_all_location_points_for(id)
    return HttpResponse(json.dumps(points, indent=2))
