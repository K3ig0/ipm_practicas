#!/usr/bin/env python

import pygtk
import os
import gtk, gobject, webkit


class VideoUI():

    def __init__(self, controller):
        self.controller = controller
        self.videos = []
        self.current = 0
        
        # Widgets    
        self.win = gtk.Window()
        self.win.set_title("Lazy video player")
        self.win.resize(400,450)
        
        #menubar
        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(filemenu)
       
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", controller.quit)
        filemenu.append(exit)

        mb.append(filem)
        
        helpmenu = gtk.Menu()
        helpm = gtk.MenuItem("Help")
        helpm.set_submenu(helpmenu)
       
        about = gtk.MenuItem("About")
        about.connect("activate", controller.on_acercade)
        helpmenu.append(about)
        
        
        controlsmenu = gtk.Menu()
        controlsm = gtk.MenuItem("Controls")
        controlsm.set_submenu(controlsmenu)
       
        playpause = gtk.MenuItem("Play/Pause")
        playpause.connect("activate", controller.on_playPause)
        controlsmenu.append(playpause)
        stop = gtk.MenuItem("Stop")
        stop.connect("activate", controller.on_stop)
        controlsmenu.append(stop)
        next = gtk.MenuItem("Next")
        next.connect("activate", controller.on_next)
        controlsmenu.append(next)
        mb.append(controlsm)
        mb.append(helpm)
        
        vbox = gtk.VBox()
        self.win.add(vbox)
        vbox.pack_start(mb, False, False, 0)
        hbox = gtk.HBox()
        vbox.pack_start(hbox, True, True, 0)
        self.webcam_display = gtk.Image()
        hbox.pack_start(self.webcam_display, False, False, 0)
        vbox = gtk.VBox()
        self.webview = webkit.WebView()
        vbox.pack_start(self.webview, False, False, 0)
        store = gtk.ListStore(int, str)
        
        if len(os.listdir("movies")) == 0:
            md = gtk.MessageDialog(self.win, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, "No hay ningun video en la carpeta movies")
            md.run()
            md.destroy()
            quit()
            
        i = 0
        for movie in os.listdir("movies"):
            store.append([i,movie])
            self.videos.append(movie)
            i+=1
            
        self.treeView = gtk.TreeView(store)
        self.treeView.set_rules_hint(True)
        sw = gtk.ScrolledWindow()
        sw.add(self.treeView)
        vbox.pack_start(sw, True, True, 0)
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("id", rendererText, text=0)
        column.set_sort_column_id(0)
        self.treeView.append_column(column)
 
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Name", rendererText, text=1)
        column.set_sort_column_id(1)    
        self.treeView.append_column(column)
        hbox.pack_start(vbox, True, True, 0)
        
        self.treeView.set_cursor(self.current)
        self.treeView.get_selection().connect("changed", self.controller.on_changed)

        # other Signals
        self.win.connect("delete-event", controller.main_quit)
        
        html = '''<html><body><video id="video1" width="320" height="240" controls>
                    <source src="movies/''' + self.videos[0] + '''" type="video/mp4">
                    Tu navegador no soporta video en html5
                </video>
                <script> 
                var myVideo=document.getElementById("video1"); 
                var video = 0;

                function playPause() { 
                    if (myVideo.paused) 
                      myVideo.play(); 
                    else 
                      myVideo.pause(); 
                } 
                
                function set(video) {
                    myVideo.src = "movies/" + video;
                }
                
                function stop() {
                    myVideo.currentTime = 0;
                    myVideo.pause(); 
                }   
            </script></body></html>'''
                
        self.webview.load_html_string(html, 'file:///home/4m1g0/ipm/otra/')

    def showAcercade(self):
        about = gtk.AboutDialog()
        about.set_program_name("Lazy video player")
        about.set_version("0.1")
        about.set_copyright("o.blanco@udc.es\nmanuel.sanchez.naveira@udc.es")
        about.set_comments("Kinnetical controll for video player")
        about.set_website("http://www.todohacker.com")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("logo.png"))
        about.run()
        about.destroy()
    
    def display_frame(self, img):
        # Convert an OpenCV image to a Gtk Image
        pixbuf = gtk.gdk.pixbuf_new_from_array(img, gtk.gdk.COLORSPACE_RGB, 8)
        self.webcam_display.set_from_pixbuf(pixbuf)


    def clicked_button(self, index, count):
        # IMPORTANT: ANY CALL TO A WEBKIT FUNCTION SHOULD BE MADE INSIDE THE
        # GOBJECT.IDLE_ADD FUNCTION. OTHERWISE, IT WILL NOT WORK!!!
        if index == 0:
            gobject.idle_add(self.playPause)
        elif index == 1:
            gobject.idle_add(self.next)
        else:
            gobject.idle_add(self.setVideo, index-2)
    
    def playPause(self):
        self.webview.execute_script('playPause()')
    
    def stop(self):
        self.webview.execute_script('stop()')
    
    def next(self):
        self.current += 1
        if self.current == len(self.videos):
            self.current = 0
        self.webview.execute_script('set("' + self.videos[self.current] + '")')
        self.treeView.set_cursor(self.current)
        
    def setVideo(self, video):
        self.current = video
        self.webview.execute_script('set("' + self.videos[self.current] + '")')
        self.treeView.set_cursor(self.current)
    
    def changed(self, i):
        self.current = int(i)
        self.webview.execute_script('set("' + self.videos[self.current] + '")')

    def start(self):
        self.win.show_all()
        gtk.main()

    def quit(self):
        gtk.main_quit()

