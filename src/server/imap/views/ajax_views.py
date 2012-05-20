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

def del_location_points_for(request, id):
    queries.delete_all_location_points_for(id)
    answer = 'OK'
    return HttpResponse(json.dumps(answer))

def save_location_points_for(request, id):
    points = json.loads(request.GET['data'])

    #validation
    valid = True
    for point in points:
        hour, minute, second = point['hour'].strip(), point['minute'].strip(), point['second'].strip()

        if not hour.isalnum() or int(hour) < 0 or int(hour) > 23:
            valid = False
            break
        if not minute.isalnum() or int(minute) < 0 or int(minute) > 59:
            valid = False
            break
        if not second.replace('.','').isalnum() or float(second) < 0 or float(second) >= 60:
            valid = False
            break
    if not valid:
        result = {'result' : 'wrong' }
        return HttpResponse(json.dumps(result))

    for point in points:
        hour, minute, second = point['hour'].strip(), point['minute'].strip(), point['second'].strip()
        latitude, longitude = point['latitude'].strip(), point['longitude'].strip()
        queries.add_location_point(id, hour, minute, second, latitude, longitude)

    result = {'result' : 'OK' }
    return HttpResponse(json.dumps(result))

