# main.py
#
# Copyright 2022 Fyodor Sobolev
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE X CONSORTIUM BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Except as contained in this notice, the name(s) of the above copyright
# holders shall not be used in advertising or otherwise to promote the sale,
# use or other dealings in this Software without prior written
# authorization.
#
# SPDX-License-Identifier: MIT

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import CavalierWindow
from .preferences_window import CavalierPreferencesWindow


class CavalierApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.fsobolev.Cavalier',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action, ['<primary>question'])
        self.create_action('preferences', self.on_preferences_action,
            ['<primary>p'])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = CavalierWindow(application=self)
        self.win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='cavalier',
                                application_icon='io.github.fsobolev.Cavalier',
                                developer_name='Fyodor Sobolev',
                                version='0.1.0',
                                developers=['Fyodor Sobolev'],
                                copyright='© 2022 Fyodor Sobolev')
        about.present()

    def on_preferences_action(self, widget, _):
        self.pref_win = CavalierPreferencesWindow(application=self)
        self.pref_win.present()

    def on_quit_action(self, widget, _):
        self.win.close()
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = CavalierApplication()
    return app.run(sys.argv)
