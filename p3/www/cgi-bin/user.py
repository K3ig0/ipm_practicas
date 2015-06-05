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
    
def get_user():
    form = cgi.FieldStorage()
    if form.has_key("user"):  
        return form["user"].value
    return ""
    
def main():
    dao = get_database_connection()
    user = get_user()
    if user == "":
        print "[]"
    else:
        print json.dumps(dao.getUser(user))

try:
    print "Content-Type: application/json\n\n"
    main()
    
except:
    cgi.print_exception()
