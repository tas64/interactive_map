#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import sys
 
def main():
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
    except:
        # Get the most recent exception
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        # Exit the script and print an error telling what happened.
        sys.exit("Database connection failed!\n ->%s" % (exceptionValue))
 
 
if __name__ == "__main__":
    sys.exit(main())

