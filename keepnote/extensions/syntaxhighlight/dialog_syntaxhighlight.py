"""
    KeepNote
    Syntax highlight code insertion
"""

# -*- coding: utf-8 -*-
#  KeepNote
#  Copyright (c) 2008-2009 Matt Rasmussen
#  Author: Matt Rasmussen <rasmus@alum.mit.edu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
#

import pygtk
pygtk.require('2.0')
import gtk
from HTMLParser import HTMLParser

from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles
from pygments.util import ClassNotFound

def get_file_content(filename):
    with open(filename, "r") as fd:
        content = fd.read()
    return content

def error_dialog(window, error_message):
    message_dialog = gtk.MessageDialog(window, 
                                       gtk.DIALOG_DESTROY_WITH_PARENT, 
                                       gtk.MESSAGE_ERROR, 
                                       gtk.BUTTONS_CLOSE, 
                                       error_message)
    message_dialog.run()
    message_dialog.destroy()

class DialogSyntaxHighlight(object):
    """
    """
    automatic = "Automatic"

    def __init__(self, window):
        self.window = window
        self.create_dialog()
        self.reinitialize()

    def create_dialog(self):
        self.dialog = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.dialog.set_default_size(400, 400)
        self.dialog.set_title("")

        vbox = gtk.VBox()
        
        vbox.pack_start(gtk.Label("Select Language:"), False)

        self.lang_selector = self.create_lang_selector()  
        vbox.pack_start(self.lang_selector, False)

        vbox.pack_start(gtk.Label("Select Style:"), False)
        self.style_selector = self.create_style_selector()  
        vbox.pack_start(self.style_selector, False)

        self.from_file_button = gtk.Button("From file...")
        vbox.pack_start(self.from_file_button, False)
        
        scrolled_window, self.textview  = self.create_scrolled_textview()
        vbox.pack_start(scrolled_window)

        self.insert_button = gtk.Button("Insert it!")
        vbox.pack_start(self.insert_button, False)

        self.dialog.add(vbox)

        self.do_signal_connections()

    def create_lang_selector(self):
        lang_selector = gtk.combo_box_entry_new_text()
        lang_selector.append_text(self.automatic)
        
        completion = gtk.EntryCompletion()
        completion.set_model(lang_selector.get_model())
        completion.set_minimum_key_length(1)
        completion.set_text_column(0) 

        lang_selector.child.set_completion(completion)

        for name in self.get_lang_names():
            lang_selector.append_text(name)
        return lang_selector

    def get_lang_names(self):
        l = []
        for (longname, aliases, _, _) in get_all_lexers():
            if len(aliases) > 0:
                l.append(aliases[0])
        l.sort()
        return l

    def create_style_selector(self):
        style_selector = gtk.combo_box_entry_new_text()
        
        completion = gtk.EntryCompletion()
        completion.set_model(style_selector.get_model())
        completion.set_minimum_key_length(1)
        completion.set_text_column(0) 

        style_selector.child.set_completion(completion)
        defaultidx=0
        for idx,name in enumerate(self.get_style_names()):
            style_selector.append_text(name)
            if(name=="default"):
                defaultidx=idx
        style_selector.set_active(defaultidx)

        return style_selector

    def get_style_names(self):
        l = []        
        for name in get_all_styles():
            l.append(name)
        l.sort()
        return l

    def create_scrolled_textview(self):
        textview = gtk.TextView(gtk.TextBuffer())
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.add_with_viewport(textview)
        return scrolledwindow, textview

    def do_signal_connections(self):
        self.insert_button.connect("clicked", self.on_insert_button_clicked)
        self.from_file_button.connect("clicked",
             self.on_from_file_button_clicked)
        self.dialog.connect("delete-event", self.on_delete_dialog)

    def on_insert_button_clicked(self, button):
        start, end = self.textview.get_buffer().get_bounds()
        text = self.textview.get_buffer().get_text(start, end)
        lang = self.lang_selector.get_active_text()
        style = self.style_selector.get_active_text()
        self.insert_it(text.decode(), lang, style)
        self.hide()

    def insert_it(self, text, lang, style):
        editor = self.window.get_viewer().get_editor()
        textview = editor._textview
        try:
            if lang == self.automatic:
                lexer = guess_lexer(text)
            else:
                lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            textview.insert_html(text)
        else:
            formatter = HtmlFormatter(noclasses=True, lineseparator="<br>",style=style)
            result = highlight(text, lexer, formatter)
            #fix encoding
            result = result.replace("&quot;",'"');
            result = result.replace("&#39;","'");
            #fix leading spaces
            result = result.replace("\x09",'&#09;')
            result = result.replace("    ","&nbsp;&nbsp;&nbsp;&nbsp;")
            textview.insert_html(result)
    
    def on_from_file_button_clicked(self, button):
        chooser = self.create_file_chooser()        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
            chooser.destroy()

            try:
                content = get_file_content(filename)
            except IOError:
                error_dialog(self.window,
                            "File not found : %s" % (filename,))
                return
            
            self.load_textview_from_str(content)
            try:
                lexer = guess_lexer_for_filename(filename, content)
            except ClassNotFound:
                pass
            else:
                if len(lexer.aliases) > 0:
                    self.lang_selector.child.set_text(lexer.aliases[0])

    def create_file_chooser(self):
        chooser = gtk.FileChooserDialog("Open...",
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,
             gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        return chooser

    def load_textview_from_str(self, s):
        self.textview.get_buffer().set_text(s)

    def on_delete_dialog(self, window, eventt):
        window.hide()
        return True
    
    def reinitialize(self):
        self.textview.get_buffer().set_text("")
        #self.lang_selector.set_active(0)
        #always focus on the combo box
        #self.lang_selector.grab_focus()
        #focus on the text editor instead
        self.textview.grab_focus()

    def show(self):
        self.dialog.show_all()

    def hide(self):
        self.dialog.hide()

