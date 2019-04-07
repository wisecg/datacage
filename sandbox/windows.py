#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio


def main():
    """
    master class:
    https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Window.html
    """
    # try again to set the theme to match a mac
    # settings = Gtk.Settings.get_default()
    # settings.set_property("gtk-theme-name", "Raleigh")
    # settings.set_property("gtk-application-prefer-dark-theme", False)
    # exit()
    # ugggggg

    # try_windows()
    # open_two()


def try_windows():

    w1 = FlowBoxWindow()
    w2 = HeaderBarWindow()
    w3 = NotebookWindow()
    w2.show_all()
    Gtk.main()


def open_two():
    def but_call(widget, data=None):
        win.show_all()  # shows new window

    win = Gtk.Window()
    win.connect("destroy",
                Gtk.main_quit)  # oh, this should only be in the master
    mywin = Gtk.Window()
    mywin.connect("destroy", Gtk.main_quit)

    # now show this window when somebody presses a button in ur main window
    button = Gtk.Button()
    button.connect("clicked", but_call)
    mywin.add(button)
    mywin.show_all()

    Gtk.main()


class HeaderBarWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="HeaderBar Demo")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        self.set_default_size(400, 200)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "HeaderBar example"
        self.set_titlebar(hb)

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        hb.pack_end(button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        button = Gtk.Button()
        button.add(
            Gtk.Arrow(
                arrow_type=Gtk.ArrowType.LEFT,
                shadow_type=Gtk.ShadowType.NONE))
        box.add(button)

        button = Gtk.Button()
        button.add(
            Gtk.Arrow(
                arrow_type=Gtk.ArrowType.RIGHT,
                shadow_type=Gtk.ShadowType.NONE))
        box.add(button)

        hb.pack_start(box)

        self.add(Gtk.TextView())


class FlowBoxWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="FlowBox Demo")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(10)
        self.set_default_size(300, 250)

        header = Gtk.HeaderBar(title="Flow Box")
        header.set_subtitle("Sample FlowBox app")
        header.props.show_close_button = True

        self.set_titlebar(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(20)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.create_flowbox(flowbox)

        scrolled.add(flowbox)

        self.add(scrolled)
        self.show_all()

    def on_draw(self, widget, cr, data):
        context = widget.get_style_context()
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        Gtk.render_background(context, cr, 0, 0, width, height)

        r, g, b, a = data['color']
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle(0, 0, width, height)
        cr.fill()

    def color_swatch_new(self, str_color):
        color = Gdk.color_parse(str_color)
        rgba = Gdk.RGBA.from_color(color)
        button = Gtk.Button()
        area = Gtk.DrawingArea()
        area.set_size_request(24, 24)
        area.connect("draw", self.on_draw, {'color': rgba})
        button.add(area)
        return button

    def create_flowbox(self, flowbox):
        colors = [
            'aquamarine',
            'azure',
            'beige',
            'bisque',
            'black',
            'BlanchedAlmond',
            'blue',
            'BlueViolet',
            'brown',
            'burlywood',
            'CadetBlue',
            'chartreuse',
            'chocolate',
            'coral',
        ]
        for color in colors:
            button = self.color_swatch_new(color)
            flowbox.add(button)


class NotebookWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simple Notebook Example")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(3)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label(label='Default Page!'))
        self.notebook.append_page(self.page1, Gtk.Label(label='Plain Title'))

        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label(label='A page with an image for a Title.'))
        self.notebook.append_page(
            self.page2,
            Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))


if __name__ == "__main__":
    main()
