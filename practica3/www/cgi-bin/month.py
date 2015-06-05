#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import couchdb
import DAO
import json

def get_database_connection():
    server = couchdb.Server()
    db = server["calendar"]
    dao = DAO.CouchDBDAO(db)
    return dao
    
def get_date():
    form = cgi.FieldStorage()
    if form.has_key("year") and form.has_key("month"):  
        return (form["year"].value, form["month"].value)
    return ("","")
    
def main():
    dao = get_database_connection()
    year, month = get_date()
    if year == "" or month == "":
        print "[]"
    else:
        events = dao.getMonthEvents(year, month)
        print json.dumps(events)

try:
    print "Content-Type: application/json\n\n"
    main()
    
except:
    cgi.print_exception()
