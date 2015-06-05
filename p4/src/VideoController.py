#!/usr/bin/env python

from VideoCapture import VideoCapture
from VideoUI import VideoUI

from datetime import datetime

import pygtk
pygtk.require('2.0')
import gobject
import os
gobject.threads_init()

class VideoController():

  def __init__(self):

    # roi = region of interest: array with the coordinates of the virtual buttons on the image
    # TODO: Add new virtual bottoms by selecting new regions on the frame! 
    roi = [(0,0, 50, 50), (590, 0, 640, 50)]
    
    self._view = VideoUI(self)
    
    n = len(os.listdir("movies"))
    ini = 100
    fin = 500
    step = (fin-ini)/n
    for i in range(n):
        roi.append([ini, 0, ini+step, 50])
        ini += step
    
    self._capture_from_webcam = True

    self._capture = VideoCapture(self, roi)

    # Store the time where the last click was performed in each virtual button
    self.last_click = [0, 0]
    for i in range(n):
        self.last_click.append(0)
    
    # EXAMPLE
    # Store the number of clicks performed in each virtual button
    self.click_counter = [0, 0]
    for i in range(n):
        self.click_counter.append(0)
  
  def start(self):
    self._capture.start()    
    self._view.start()
    
  def on_close(self,w,e=None):
        self._view.quit()
    
  def on_acercade(self,w):
      self._view.showAcercade()

  def on_playPause(self,w):
      self._view.playPause()

  def on_stop(self,w):
      self._view.stop()
      
  def on_next(self,w):
    self._view.next()
    
  def on_changed(self,selection):
    (model, i) = selection.get_selected()
    self._view.changed(model[i][0])
  
  def is_capture_enabled(self):
    return self._capture_from_webcam
    
    
  def display_frame(self, frame):
    gobject.idle_add(self._view.display_frame, frame)
    
       
  def on_click_virtual_button(self, index):    

    now = datetime.now()
    if self.last_click[index] == 0 or self._is_a_new_click(self.last_click[index], now):       
       self.last_click[index] = now
  
       # EXAMPLE: display the number of clicks in the View    
       self._view.clicked_button(index, self.click_counter[index])
    else:
      print "Click virtual button {i} discarded".format(i=index)
      pass

  
  def main_quit(self, arg1, arg2):  
    print "exit!"
    self._capture_from_webcam = False
    gobject.idle_add(self._view.quit)
  
  def quit(self, arg1):  
    print "exit!"
    self._capture_from_webcam = False
    gobject.idle_add(self._view.quit)
    
    
  def _is_a_new_click(self, t1, t2):
    # Discard clicks very close in time (< 0.5 seconds)
    c = t2 - t1
    if c.seconds > 0.5:
      return True
    else:
      return False
  
