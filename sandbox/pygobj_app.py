#!/usr/bin/env python3

from gi.repository import GObject, Gio, Gdk, Gtk

def main():
    """
    initialize GTK Application and start GUI
    """
	Application = MyApplication("com.bachsau.example", Gio.ApplicationFlags.FLAGS_NONE)
	Application.run()


class MyApplication(Gtk.Application):
    """
	main initialization routine
    """
	def __init__(self, application_id, flags):
		Gtk.Application.__init__(self, application_id=application_id, flags=flags)
		self.connect("activate", self.new_window)

	def new_window(self, *args):
		AppWindow(self)

class AppWindow(object):
	def __init__(self, application):
		self.Application = application

		# Read GUI from file and retrieve objects from Gtk.Builder
		try:
			GtkBuilder = Gtk.Builder.new_from_file("gui.glade")
			GtkBuilder.connect_signals(self)
		except GObject.GError:
			print("Error reading GUI file")
			raise

		# Fire up the main window
		self.MainWindow = GtkBuilder.get_object("MainWindow")
		self.MainWindow.set_application(application)
		self.MainWindow.show()

	def close(self, *args):
		self.MainWindow.destroy()


if __name__ == "__main__":
    main()