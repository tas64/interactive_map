# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json

import psycopg2
import sys

from models import  ImmobileObject, MovableObject
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
    for movable in MovableObject.objects.all():
        result.append( movable.get_json() )
    return HttpResponse(json.dumps(result, indent=2))

def immobiles_objects(request):
    result = []
    for immobile in ImmobileObject.objects.all():
        result.append( immobile.get_json() )
    return HttpResponse(json.dumps(result, indent=2))

def location_points_for(request, id):
    result = []
    try:
        m_object = MovableObject.objects.get(id=id)
    except:
        return HttpResponse(json.dumps(result, indent=2))
    for point in m_object.locationpoint_set.all():
        result.append(point.get_json())
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
