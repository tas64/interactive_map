import sys
import psycopg2
from imap.database import queries

from django.shortcuts import render_to_response
from django.http import HttpResponse

def ajaxtest(request):
    return render_to_response('test/ajaxtest.html')

def mapsapi(request):
    return render_to_response('test/mapsapi.html')

def all_immobiles_on_map(request):
    return render_to_response("test/all_immobiles.html")

def format_point(s, before, after):
    result = str(s)
    if result.find('.') == -1:
        result += '.' + '0'*after
        return result
    b, a = result.split('.')
    if len(b) < before:
        b = '0'*(before - len(b)) + b
    if len(a) < after:
        a = '0'*(after - len(a)) + a
    a = a[:after]
    return "%s.%s" % (b, a)

def locationpoints_file(request):
    points = queries.get_all_location_points()
    results = []
    for point in points:
        id = point['movable_id']
        h,m,s = point['hour'], point['minute'], point['second']

        real_latitude = point['latitude']
        real_longitude = point['longitude']

        p = 'S'
        if real_latitude < 0:
            p = 'N'
            real_latitude *= -1
        j = 'E'
        if real_longitude < 0:
            j = 'W'
            real_longitude *= -1

        latitude_degree, latitude_minute = int(real_latitude), (real_latitude - int(real_latitude))*60
        longitude_degree, longitude_minute = int(real_longitude), (real_longitude - int(real_longitude))*60

        s = format_point(s, 2,2)
        latitude_minute = format_point(latitude_minute, 2,2)
        longitude_minute = format_point(longitude_minute, 2,2)

        result = "$%d, %s%s%s, %s%s, %s, %s%s, %s" % (id, h,m,s, latitude_degree, latitude_minute, p, longitude_degree, longitude_minute, j)
        results.append(result)
    return render_to_response("test/locationpoints_file.html", {'results' : results})

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
