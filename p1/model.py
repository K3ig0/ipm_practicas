import pycouchdb
from datetime import datetime, timedelta

class Model():
    def __init__(self, controller):
        self.connect()
    
    def connect(self):
        try:
            couch = pycouchdb.Server("http://localhost:5984")
            self.db = couch.database("prueba")
            self.connected = True
        except:
            self.connected = False
            print("Error: No se pudo conectar con la base de datos")
    
    def getEventDays(self, fechaCalendario, subjects):
        if not self.connected:
            return []
        
        map_fun = '''function(doc) {
            if (doc.type == "Event") {
                emit(doc.id, {date: doc.date, tags: doc.tags});
            }
        }'''
        result = self.db.temporary_query(map_fun)
        days = []
        for row in result:
            fecha = datetime.strptime(row['value']['date'], "%Y-%m-%d")
            if fecha.month == fechaCalendario.month and fecha.year == fechaCalendario.year:
                if subjects == [] or row['value']['tags'][0] in subjects:
                    days.append(fecha.day)
        return days
    
    def getEventDesc(self, fechaCalendario, subjects):
        if not self.connected:
            return []
        map_fun = '''function(doc) {
            if (doc.type == "Event") {
                emit(doc.date, [doc.description, doc.tags]);
            }
        }'''
        result = self.db.temporary_query(map_fun)
        desc = []
        for row in result:
            fecha = datetime.strptime(row['key'], "%Y-%m-%d")
            if fecha.month == fechaCalendario.month and fecha.year == fechaCalendario.year and fecha.day == fechaCalendario.day:
                if subjects == [] or row['value'][1][0] in subjects:
                    desc.append(row['value'])
        return desc
        
   
    def getSubjects(self, user):
        if not self.connected:
            return ([],-1)
        
        map_fun = '''map_fun = function(doc) {
            if (doc.type == "User") {
		        emit(doc.description, {Subtype: doc.subtype, Subjects: doc.subjects});
	            }
            }'''
        
        result = self.db.temporary_query(map_fun)
        for row in result:
            if row["key"] == user:
                if row["value"]["Subtype"] == "student":
                    return (row["value"]["Subjects"],0) # 0 = student
                else:
                    return (row["value"]["Subjects"],1) # 1 = teacher
        return ([],-1) # -1 no encontrado


    def getCloseEvents(self, now):
        if not self.connected:
            return ([])
        
        map_fun = '''map_fun = function(doc) {
            if (doc.type == "Event") {
		        emit(doc.date, doc.description);
	            }
            }'''
        
        result = self.db.temporary_query(map_fun)
        desc = []
        for row in result:
            fecha = datetime.strptime(row['key'], "%Y-%m-%d")
            if abs(fecha - now) < timedelta(days = 30):
                desc.append(row['value'])
            
        return desc
    
    
    def getStudents(self, subjects):
        if not self.connected:
            return ([])
        
        map_fun = '''map_fun = function(doc) {
            if (doc.subtype == "student") {
		        emit(doc.subjects, doc.description);
	            }
            }'''
        
        result = self.db.temporary_query(map_fun)
        students = []
        for row in result:
            if list(set(row['key']) & set(subjects)) != []: # interseccion de ambas listas de asignaturas
                students.append(row['value'])
            
        return students
            
            
            
