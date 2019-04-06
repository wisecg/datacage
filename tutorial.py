#!/usr/bin/env python3
"""
Python GTK3+ Tutorial
- https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html

Prerequisites:
- brew install pygobject3 gtk+3
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def main():
    """
    run the tutorial program
    """
    # create empty window
    win = SimpleWindow()

    # kill the window when we click on the red X in macOS
    win.connect("destroy", Gtk.main_quit)

    # display the window
    win.show_all()

    # start the GTK+ processing loop
    Gtk.main()


class SimpleWindow(Gtk.Window):
    """
    a simple window with a button.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World")


if __name__=="__main__":
    main()

