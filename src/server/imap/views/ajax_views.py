import json
from django.http import HttpResponse
from imap.database import queries

def simple_request(request):
    object = {'test' : True, 'counter' : 5}
    return HttpResponse(json.dumps(object, indent=2))

def movables_objects(request):
    if request.GET.has_key('q') and request.GET['q'] != "*":
        pattern = request.GET['q']
        objects = queries.search_movables_objects(pattern)
    else:
        objects = queries.get_all_movables_objects()
    return HttpResponse(json.dumps(objects, indent=2))

def movables_objects_search(request,pattern):
    objects = queries.search_movables_objects(pattern)
    return HttpResponse(json.dumps(objects, indent=2))

def immobiles_objects(request):
    if request.GET.has_key('q') and request.GET['q'] != "*":
        pattern = request.GET['q']
        objects = queries.search_immobiles_objects(pattern)
    else:
        objects = queries.get_all_immobiles_objects()
    return HttpResponse(json.dumps(objects, indent=2))

def immobiles_objects_search(request, pattern):
    objects = queries.search_immobiles_objects(pattern)
    return HttpResponse(json.dumps(objects, indent=2))

def location_points_for(request, id):
    points = queries.get_all_location_points_for(id)
    return HttpResponse(json.dumps(points, indent=2))
