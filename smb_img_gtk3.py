#!/usr/bin/env python

# A gui script to download images from a samba server with their name and open them with an image viewer.

import gi,sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from cStringIO import StringIO
from smb.SMBConnection import SMBConnection
from smb import smb_structs
from nmb.NetBIOS import NetBIOS
import os
from socket import gethostname
import subprocess

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="GBS IMAGE VIEWER", application=app)
        self.set_default_size(300, 100)
        self.set_border_width(10)
        #self.set_icon(Gtk.STOCK_FLOPPY)
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)
        listbox=Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)
        # a single line entry


        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)
        label = Gtk.Label("Enter the invoice number you want to view")

        name_box = Gtk.Entry()
        # emits a signal when the Enter key is pressed, connected to the
        # callback function cb_activate
        name_box.connect("activate", self.cb_activate)

        # add the Gtk.Entry to the window
        listbox.add(label)
        listbox.add(name_box)

    # the content of the entry is used to write in the terminal
    def cb_activate(self, entry):
        # retrieve the content of the widget
		filename = entry.get_text()
		filename = filename + ".tif"
		path ='/gbss/fmdscandata/invoice/'
		smb_structs.SUPPORT_SMB2 =False #smb2 True or False
		conn = SMBConnection("#username", "#passwd", "#client_machine_name", "#remote_machine_name", use_ntlm_v2=False)
		assert conn.connect("#IP,#Port)

		file_obj=StringIO()
		file_attributes, filesize = conn.retrieveFile('IMAGES', path+filename, file_obj)
		fw = open(filename, 'w')
		file_obj.seek(0)
		for line in file_obj:
    			fw.write(line)
		fw.close()
		print 'download finished'
		conn.close()

		p=subprocess.Popen(["evince",filename])
		returncode =p.wait()
        # print it in a nice form in the terminal
		print("Hello ")
		self.destroy()


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
