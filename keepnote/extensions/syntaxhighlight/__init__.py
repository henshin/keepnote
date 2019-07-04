"""
    KeepNote
    Syntax highlight code insertion
"""
# -*- coding: utf-8 -*-
#
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
import sys
import os

# python imports
import gettext
_ = gettext.gettext


# keepnote imports
from keepnote.gui import extension


sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from dialog_syntaxhighlight import DialogSyntaxHighlight


class Extension (extension.Extension):

    def __init__(self, app):
        """Initialize extension"""
        extension.Extension.__init__(self, app)
        self.dialogs_syntax_highlight = {}

    #================================
    # UI setup

    def on_add_ui(self, window):

        menu_label = "Insert code with syntax highlighting..."
        # add menu options
        self.add_action(window, menu_label, 
          menu_label,
          lambda w: self.on_insert_syntax_highlight(window))

        self.add_ui(window,
                """
                <ui>
                <menubar name="main_menu_bar">
                   <menu action="Edit">
                      <placeholder name="Viewer">
                      <placeholder name="Editor">
                      <placeholder name="Extension">
                        <menuitem action="%s"/>
                      </placeholder>
                      </placeholder>
                      </placeholder>

                   </menu>
                </menubar>
                </ui>
                """ % (menu_label,))

    #================================
    # actions

    def on_insert_syntax_highlight(self, window):
        dialog = self.dialogs_syntax_highlight.get(window,
            DialogSyntaxHighlight(window))
        self.dialogs_syntax_highlight[window] = dialog

        dialog.reinitialize()
        dialog.show()

