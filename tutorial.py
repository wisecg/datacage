#!/usr/bin/env python3

# -- gi: PyGObject3 / Gtk3+ --
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

# -- use the MPL API directly --
import matplotlib
matplotlib.use("Gtk3Agg") # MacOSX, Gtk3Cairo, Gtk3Agg (fastest)
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavBar

import numpy as np
from pprint import pprint

def main():
    """
    Python Gtk3+ Tutorial
    - https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html

    Matplotlib integration:
    - https://matplotlib.org/gallery/index.html#embedding-matplotlib-in-graphical-user-interfaces
    - https://matplotlib.org/api/index.html

    Prerequisites:
    - brew install pygobject3 gtk+3
    """

    # settings = Gtk.Settings.get_default()
    # settings.set_property("gtk-theme-name", "Zukitwo")
    # settings.set_property("gtk-application-prefer-dark-theme", True)
    # pprint(settings.list_properties()) # print all properties
    # for val in settings.list_properties():
    #     if "theme" in str(val):
    #         print(val)

    css = Gtk.CssProvider.load_from_file("dark.css")

    # css_provider = Gtk.CssProvider()
    # mysheet = Gio.File.new_for_path("dark.css")
    # css_provider.load_from_file(mysheet)
    screen = Gdk.Screen.get_default()
    style_context = window.get_style_context()
    style_context.add_provider_for_screen(screen, css_provider,
                                          Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    exit()

    # win = SimpleWindow()
    # win = PanZoomWindow()
    # win = ScrolledWindow()
    win = DataManager()
    # win = PyplotWindow()

    # display the window
    win.show_all()

    # start the Gtk+ processing loop
    Gtk.main()


class SimpleWindow(Gtk.Window):
    """
    a simple window with a button.
    https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html
    """
    def __init__(self):

        # declare the window
        Gtk.Window.__init__(self, title="SimpleWindow")

        # kill the window when we click on the red X in macOS
        self.connect("destroy", Gtk.main_quit)

        # add a button
        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        print("Hello World") # prints to terminal


class PanZoomWindow(Gtk.Window):
    """
    Create an interactive (pan/zoom) matplotlib Figure.
    Doesn't use pyplot, so we can't easily play some of the normal
    formatting tricks like plt.tight_layout.
    - https://matplotlib.org/gallery/user_interfaces/embedding_in_gtk3_panzoom_sgskip.html
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Plot Window Name")
        self.connect("delete-event", Gtk.main_quit)

        xpix, ypix, dpi = 600, 400, 100
        self.set_default_size(xpix*1.1, ypix*1.1)

        # create the plot
        f = Figure(figsize=(xpix/dpi, ypix/dpi), dpi=dpi)
        p = f.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        p.plot(t, s)

        # draw the plot in the window
        canvas = FigureCanvas(f)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        vbox.pack_start(canvas, True, True, 0)

        # create matplotlib nav bar (makes the window interactive)
        toolbar = NavBar(canvas, self)
        vbox.pack_start(toolbar, False, False, 0)


class ScrolledWindow(Gtk.Window):
    """
    display a matplotlib plot in a Gtk.ScrolledWindow.
    Not sure why, but I couldn't make this class inherit directly from
    Gtk.ScrolledWindow, I had to declare one in the init.
    https://matplotlib.org/gallery/user_interfaces/embedding_in_gtk3_sgskip.html
    """
    def __init__(self):

        # -- this part is identical to PanZoomWindow above
        Gtk.Window.__init__(self, title="Plot Window Name")
        self.connect("delete-event", Gtk.main_quit)
        xpix, ypix, dpi = 600, 400, 100
        self.set_default_size(xpix*1.1, ypix*1.1)
        f = Figure(figsize=(xpix/dpi, ypix/dpi), dpi=dpi)
        p = f.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2*np.pi*t)
        p.plot(t, s)

        # -- create a ScrolledWindow.
        self.sw = Gtk.ScrolledWindow()
        self.add(self.sw)
        self.sw.set_border_width(10)

        # if canvas is shrunk smaller than (xpix, ypix), the content
        # isn't resized and scrollbars pop up in the window
        canvas = FigureCanvas(f)
        canvas.set_size_request(xpix, ypix)
        self.sw.add(canvas)


class DataManager(Gtk.Window):
    """
    https://matplotlib.org/gallery/user_interfaces/gtk_spreadsheet_sgskip.html
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="GtkListStore demo")
        self.connect("delete-event", Gtk.main_quit)
        # self.connect("destroy", Gtk.main_quit) # no difference?

        xpix, ypix, dpi = 600, 600, 100
        self.set_default_size(xpix, ypix)
        self.set_border_width(8)

        # -- overall window box
        # docs recommend we switch this Gtk.Box to a Gtk.Grid
        # https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/VBox.html#Gtk.VBox
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        label = Gtk.Label(label='Double click a row to plot the data')
        vbox.pack_start(label, False, False, 0)

        # -- ScrolledWindow to hold our data table
        self.sw = Gtk.ScrolledWindow()
        self.sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(self.sw, True, True, 0)

        # set data
        self.nrows, self.ncols = 20, 10
        self.data = np.random.random((self.nrows, self.ncols))

        # declare the model (a Gtk.ListStore) and TreeView for our data table
        model = self.create_table()
        self.treeview = Gtk.TreeView(model=model)

        # -- Figure for the plot of each row
        fig = Figure(figsize=(xpix/dpi, ypix/dpi), dpi=dpi)
        self.set_default_size(xpix, ypix)
        self.canvas = FigureCanvas(fig)
        vbox.pack_start(self.canvas, True, True, 0)

        ax = fig.add_subplot(111)
        self.line, = ax.plot(self.data[0,:], 'go') # plot first row

        # -- set an action: update plot when you dblclick a row
        self.treeview.connect('row-activated', self.plot_row)
        self.sw.add(self.treeview)

        self.add_columns() # load our data

        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.KEY_RELEASE_MASK)

    def create_table(self):
        """
        create a Gtk.ListStore from a big tuple.
        I bet we could convert this to a pd.DataFrame
        """
        types = [float]*self.ncols
        store = Gtk.ListStore(*types)
        for row in self.data:
            store.append(tuple(row))
        return store

    def add_columns(self):
        for i in range(self.ncols):
            column = Gtk.TreeViewColumn(str(i), Gtk.CellRendererText(), text=i)
            self.treeview.append_column(column)

    def plot_row(self, treeview, path, view_column):
        idx, = path
        points = self.data[idx, :]
        self.line.set_ydata(points)
        self.canvas.draw()


class PyplotWindow(Gtk.Window):
    """
    try using the pyplot interface, even though matplotlib's gallery
    says you can't.  wtf do they know?  their own example says you can.
    https://matplotlib.org/gallery/user_interfaces/pylab_with_gtk_sgskip.html
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Plot Window Name")
        self.connect("delete-event", Gtk.main_quit)

        xpix, ypix, dpi = 600, 400, 100
        self.set_default_size(xpix*1.1, ypix*1.1)

        # dummy pyplot
        import matplotlib.pyplot as plt
        fig = plt.Figure(figsize=(xpix/dpi, ypix/dpi), dpi=dpi)
        plt.plot([1, 2, 3], 'ro-', label='easy as 1 2 3')
        plt.plot([1, 4, 9], 'gs--', label='easy as 1 2 3 squared')
        plt.legend()
        plt.tight_layout()

        # grab the underlying gtk widgets that pyplot uses
        manager = plt.get_current_fig_manager()
        tbar = manager.toolbar # same as NavBar above
        vbox = manager.vbox

        # -- add a button to the matplotlib NavBar
        button = Gtk.Button(label="Click Me!")
        button.show()
        def clicked(button):
            print("hi mom")
        button.connect('clicked', clicked)
        ti = Gtk.ToolItem(tooltip_text="Click me for fun and profit")
        ti.add(button)
        ti.show()
        tbar.insert(ti, 9) # NavBar index number

        # -- add a widget to the vbox that senses mouse position
        label = Gtk.Label()
        label.set_markup('Drag mouse over axes for position')
        label.show()
        vbox.pack_start(label, False, False, 0)
        vbox.reorder_child(manager.toolbar, -1)
        def update(event):
            if event.xdata is None:
                label.set_markup('Drag mouse over axes for position')
            else:
                label.set_markup('<span color="#ef0000">x,y=(%f, %f)</span>' % (event.xdata, event.ydata))
        plt.connect('motion_notify_event', update)

        # -- draw stuff.  Works except I get this warning:
        # "(tutorial.py:78024): Gtk-WARNING **: 16:38:14.702: gtk_window_present_with_time() should not be called with 0, or GDK_CURRENT_TIME as a timestamp, the timestamp should instead be gathered at the time the user initiated the request for the window to be shown"
        #
        # it might be that this message is about to be removed in GTK 3.24:
        # https://gitlab.gnome.org/GNOME/gtk/commit/a8bbcf33ecf162528e9b48e609f1131a8e52f072
        plt.show()


if __name__=="__main__":
    main()

