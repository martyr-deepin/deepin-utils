#! /usr/bin/env python
import gtk
from dtk.ui.utils import color_hex_to_cairo
from deepin_font_icon import font_face_create

def draw_font_img(text, cr, x, y, face, text_size, text_color="#000000"):
    cr.set_font_face(face)
    cr.set_source_rgb(*color_hex_to_cairo(text_color))
    cr.set_font_size(text_size)
    cr.move_to(x, y)
    cr.show_text(text)

class Example(gtk.Window):

    def __init__(self):
        super(Example, self).__init__()
        
        self.init_ui()
        gtk.main()

    def init_ui(self):    
        darea = gtk.DrawingArea()
        darea.connect("expose-event", self.on_draw)
        self.add(darea)

        self.set_title("GTK window")
        self.set_size_request(450, 180)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("delete-event", gtk.main_quit)
        self.show_all()
    
    def on_draw(self, widget, event):
        cr = widget.window.cairo_create()
        rect = widget.allocation

        face = font_face_create("/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf")
        draw_font_img(
                "ABCDEFGHIJKLM",
                cr,
                rect.x,
                rect.y+40,
                face,
                40,
            )
    
if __name__ == '__main__':
    Example()
