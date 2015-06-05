#!/usr/bin/env python

import numpy
import cv2

from threading import Thread


# A typical range for skin colors
SKIN_COLORS = (numpy.array((0, 133, 77)), numpy.array((255, 173, 127)))

class VideoCapture(Thread):

  def __init__(self, listener, roi, target = None, debug=True):

    Thread.__init__(self)
    self._listener = listener
       
    if target: # Open a specific cam / video
      self.cam=cv2.VideoCapture(target)
    else: # Open the default cam
      self.cam=cv2.VideoCapture(0)
    
    self.roi = roi
         
      
  def run(self):    


    if self.cam.isOpened():

      counter = 0
          
      # The first frame is used as a reference frame for background extraction
      frame = self._get_frame()
      virtual_button_bg = self._extract_roi(frame, self.roi)
      width = frame.shape[0]
      height = frame.shape[1]
      

      while self._listener.is_capture_enabled():
        frame = self._get_frame()
        
        if counter % 2 == 0: 
            virtual_buttons = self._extract_roi(frame, self.roi)
            
            for i in range(len(self.roi)):
              is_clicked = self._is_clicked(virtual_buttons[i], virtual_button_bg[i])
              if is_clicked:
                self._listener.on_click_virtual_button(i)

        # For efficiency, send to the view only 1 of every 4 frame
        if counter % 1 == 0: 
          self._draw_buttons(frame, self.roi)
          frame_resized = cv2.resize(frame, (height/2, width/2)) # Half-size frame 
          frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
          self._listener.display_frame(numpy.array(frame_rgb))

        counter = counter + 1
  
    else:
      print "Error: cam not opened"
      
      

  def _get_frame(self):
     _, frame = self.cam.read()  
     frame_flipped = cv2.flip(frame, 1)
     return frame_flipped

  def _draw_buttons(self, frame, roi, color=(255,0,255)):
    i = 0
    for r in roi:
      cv2.rectangle(frame, (r[0],r[1]), (r[2],r[3]), color,4)
      if i > 1:
        cv2.putText(frame, str(i-2) , (r[0]+10,r[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, thickness=4)
      else:
        if i == 0:
          cv2.putText(frame, "P" , (r[0]+10,r[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, thickness=4)
        else: # i = 1
          cv2.putText(frame, ">" , (r[0]+10,r[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, thickness=4)
      i+=1
      
  def _extract_roi(self, frame, roi):
    images = []
    for r in roi:
      images.append(frame[r[1]:r[3], r[0]: r[2]])
    return images
    
    
  def _is_clicked(self,button, bg):

    # Compute the correlation between the current region and the background:
    # if the background does not change, the correlation value will be 1
    # if something has appeared in the image, the correlation value will be lower than 1
    correlation = cv2.matchTemplate(button, bg, cv2.TM_CCOEFF_NORMED)
    
    if correlation < 0.5: # The appearance of the button has changed!
      # Check if it is "skin"
      im_ycrcb = cv2.cvtColor(button, cv2.COLOR_BGR2YCR_CB)
      skin_ycrcb = cv2.inRange(im_ycrcb, SKIN_COLORS[0], SKIN_COLORS[1])
      skin_pixels = cv2.countNonZero(skin_ycrcb)
      pixels_region = button.shape[0] * button.shape[1]
      if skin_pixels > pixels_region / 2:
        return True

    return False
    




