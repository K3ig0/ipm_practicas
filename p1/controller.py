import threading
import time
from gi.repository import GObject
from gi.repository import Notify
from datetime import datetime

from view import *
from model import *

_ = gettext.gettext
N_ = gettext.ngettext

class Controller():
    def __init__(self):
        self.model = Model(self)
        self.view1 = View(self)
        self.fecha = self.view1.getDate()
        self.subjects = []
        Notify.init(_("Calendario"))
        GetEvents(self.fecha, self.subjects, self.model, self.view1).start()
        self.showNotifications() # timer
    
    def on_close(self,w,e=None):
        Gtk.main_quit()
    
    def on_acercade(self,w):
        self.view1.showAcercade()
        
    def on_monthChanged(self,w):
        self.view1.clearMarks()
        self.fecha = self.view1.getDate()
        self.view1.setStatus(_("Obteniendo dias marcados para el mes actual..."), 1)
        GetEvents(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_daySelected(self,w):
        self.view1.clearDescription()
        self.fecha = self.view1.getDate()
        if self.fecha.day in self.view1.getMarkedDays():
            self.view1.setStatus(_("Obteniendo eventos para el dia seleccionado..."), 1)
            GetDescription(self.fecha, self.subjects, self.model, self.view1).start()
    
    def on_callLogin(self,w):
        if self.view1.showLogin() == 1:
            self.view1.hideUserMenu() # ocultamos hasta que recibamos info valida
            self.view1.cleanSubjects()
            user = self.view1.getLoginText()
            self.subjects = []
            self.view1.setStatus(_("Obteniendo asignaturas para el usuario ") + user + "...", 1)
            GetSubjects(user, self, self.model, self.view1).start()
    
    def on_callSubjectDialog(self,w):
        if self.view1.showSubjectsDialog() == 1:
            subject = self.view1.getTeacherSubject()
            self.updateSubjects(subject)
            self.view1.setStatus( _("Viendo eventos de ") + subject, 0)
    
    def on_callStudentDialog(self,w):
        if self.view1.showStudentsDialog() == 1:
            student = self.view1.getTeacherStudent()
            self.subjects = []
            self.view1.setStatus(_("Obteniendo asignaturas para el usuario ") + student + "...", 1)
            GetSubjects(student, self, self.model, self.view1).start()
            
    def on_logout(self,w):
        self.view1.hideUserMenu()
        self.updateSubjects([])
        self.view1.clearStatus()
        
    def updateSubjects(self, subjects):
        self.subjects = subjects
        self.on_monthChanged(None)
        self.on_daySelected(None)
    
    def showNotifications(self):
        now = datetime.now()
        events = self.model.getCloseEvents(now)
        if events != []:
            eventStr = _("Falta poco para los siguientes eventos:\n")
            for event in events:
                eventStr += event + "\n"
            notification = Notify.Notification.new(_("Calendario"), eventStr, 'dialog-information')
            notification.show()
        

class GetEvents(threading.Thread):
    def __init__(self, fecha, subjects, model, view):
        super(GetEvents, self).__init__()
        self.fecha = fecha
        self.model = model
        self.view = view
        self.subjects = subjects
    
    def run(self):
        self.markedDays = self.model.getEventDays(self.fecha, self.subjects)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.markDays(self.markedDays, self.fecha)
        self.view.statusPop()
        
class GetDescription(threading.Thread):
    def __init__(self, fecha, subjects, model, view):
        super(GetDescription, self).__init__()
        self.fecha = fecha
        self.model = model
        self.view = view
        self.text = []
        self.subjects = subjects
    
    def run(self):
        self.text = self.model.getEventDesc(self.fecha, self.subjects)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.showDescription(self.text, self.fecha)
        self.view.statusPop()
        
        
class GetSubjects(threading.Thread):
    def __init__(self, user, controller, model, view):
        super(GetSubjects, self).__init__()
        self.user = user
        self.model = model
        self.subjects = []
        self.controller = controller
        self.view = view
        
    def run(self):
        (subjects, subtype) = self.model.getSubjects(self.user)
        self.subjects = subjects
        GObject.idle_add(self.controller.updateSubjects, self.subjects)
        if subtype == 1:# teacher
            GObject.idle_add(self.informar)
        elif subtype == -1:
            GObject.idle_add(self.controller.updateSubjects, self.subjects)
            GObject.idle_add(self.error)
                  
        if (subtype != -1):
            GObject.idle_add(self.view.setStatus, _("Viendo eventos de ") + self.user, 0)
    
    def informar(self):
        self.view.setTeacherSubjects(self.subjects)
        self.view.showSubjectsMenu()
        GetStudents(self.subjects, self.model, self.view).start()
    
    def error(self):
        self.view.clearStatus()
        self.view.showError()
        self.view.hideUserMenu()
        
class GetStudents(threading.Thread):
    def __init__(self, subjects, model, view):
        super(GetStudents, self).__init__()
        self.subjects = subjects
        self.model = model
        self.view = view
        self.students = []
    
    def run(self):
        self.students = self.model.getStudents(self.subjects)
        GObject.idle_add(self.informar)
    
    def informar(self):
        self.view.setTeacherStudents(self.students)
        self.view.showStudentsMenu()
        
        
        
        
    
