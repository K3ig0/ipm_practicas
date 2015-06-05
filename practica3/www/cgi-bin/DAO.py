#!/usr/bin/python
# --*-- coding: utf-8 --*--
import couchdb

class CouchDBDAO():

    def __init__(self, database):
        self._db = database
    
    def __view_to_list(self, view_result):
        docs = []
        for row in view_result:
            docs.append(row.value)        
    
        return docs
        
    def getMonthEvents(self, year, month): #'2013-11-30'
         f = '''
            function (doc) {
                if (doc.type =='Event') {
                    emit(doc.date.substring(0,8), [doc.date.substring(8,10), doc.description, doc.tags]);
                }
            }''' # comparamos 2013-11
         
         date = ""
         if int(month) < 10:
            date = str(year) + "-0" + str(month) + "-"
         else:
            date = str(year) + "-" + str(month) + "-"
         
         return self.__view_to_list(self._db.query(f, key=date))
       
    def getUser(self, user):
        f = '''
            function (doc) {
                if (doc.type =='User') {
                    emit(doc.description ,[doc.subtype, doc.subjects]);
                }
            }'''
            
        return self.__view_to_list(self._db.query(f, key=user))
        
