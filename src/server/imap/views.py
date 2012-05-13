# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json

import psycopg2
import sys

from db import DBWrapper
from queries import Q

def main(request):
    return render_to_response('imap/main.html')

def ajaxtest(request):
    return render_to_response('imap/ajaxtest.html')

def mapsapi(request):
    return render_to_response('imap/mapsapi.html')

def simple_ajax_request(request):
    object = {'test' : True, 'counter' : 5}
    return HttpResponse(json.dumps(object, indent=2))

def movables_objects(request):
    result = []
    db_wrapper = DBWrapper()
    movables = db_wrapper.fetch_all(Q.SELECT_ALL_MOVABLES)
    db_wrapper.dispose()
    for movable in movables:
        id, name, type = movable
        result.append({'id' : id, 'name' : name, 'type' : type})
    return HttpResponse(json.dumps(result, indent=2))

def immobiles_objects(request):
    result = []
    db_wrapper = DBWrapper()
    immobiles = db_wrapper.fetch_all(Q.SELECT_ALL_IMMOBILES)
    db_wrapper.dispose()
    for immobile in immobiles:
        id, name, phone, latitude, longitude = immobile
        result.append({'id' : id, 'name' : name, 'phone' : phone, 'latitude' : latitude, 'longitude' : longitude})
    return HttpResponse(json.dumps(result, indent=2))

def location_points_for(request, id):
    result = []
    try:
         db_wrapper = DBWrapper()
         points = db_wrapper.fetch_all(Q.LOCATION_POINTS_FOR % id)
         db_wrapper.dispose()
    except:
        return HttpResponse(json.dumps(result, indent=2))
    for point in points:
        id, movable_id, hour, minute, second, latitude, longitude = point
        result.append({'id' : id, 'movable_id' : movable_id, 'hour' : hour, 'minute' : minute, 'second' : second,
                       'latitude' : latitude, 'longitude' : longitude})
    return HttpResponse(json.dumps(result, indent=2))

def db_connection_test(request):
    #start of script
    #Define our connection string
    conn_string = "host='localhost' dbname='test_db' user='test_user' password='test_pass'"
    # print the connection string we will use to connect
    print "Connecting to database\n ->%s" % (conn_string)
    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)
        # conn.cursor will return a cursor oject, you can use this cursor to perform queries
        cursor = conn.cursor()
        print "Connected!\n"
    
        return HttpResponse("<html> Connection status: OK </html>")
    except:
        # Get the most recent exception
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        # Exit the script and print an error telling what happened.
        sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

        return HttpResponse("<html> Connection status: ERROR </html>")

def all_immobiles_on_map(request):
    return render_to_response("imap/all_immobiles.html")
