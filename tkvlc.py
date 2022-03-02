#! /usr/bin/python
# tkinter example for VLC Python bindings
# This has been adapted from the original distribution from VideoLAN team

#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

# import external libraries
import vlc
# import standard libraries
import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
    from Tkinter.tkMessageBox import showerror
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showerror
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time

_isMacOS   = sys.platform.startswith('darwin')
_isWindows = sys.platform.startswith('win')
_isLinux   = sys.platform.startswith('linux')

if _isMacOS:
    from ctypes import c_void_p, cdll
    # libtk = cdll.LoadLibrary(ctypes.util.find_library('tk'))
    # returns the tk library /usr/lib/libtk.dylib from macOS,
    # but we need the tkX.Y library bundled with Python 3+,
    # to match the version number of tkinter, _tkinter, etc.
    try:
        libtk = 'libtk%s.dylib' % (Tk.TkVersion,)
        prefix = getattr(sys, 'base_prefix', sys.prefix)
        libtk = joined(prefix, 'lib', libtk)
        dylib = cdll.LoadLibrary(libtk)
        # getNSView = dylib.TkMacOSXDrawableView is the
        # proper function to call, but that is non-public
        # (in Tk source file macosx/TkMacOSXSubwindows.c)
        # and dylib.TkMacOSXGetRootControl happens to call
        # dylib.TkMacOSXDrawableView and return the NSView
        _GetNSView = dylib.TkMacOSXGetRootControl
        # C signature: void *_GetNSView(void *drawable) to get
        # the Cocoa/Obj-C NSWindow.contentView attribute, the
        # drawable NSView object of the (drawable) NSWindow
        _GetNSView.restype = c_void_p
        _GetNSView.argtypes = c_void_p,
        del dylib

    except (NameError, OSError):  # image or symbol not found
        def _GetNSView(unused):
            return None
        libtk = "N/A"

    C_Key = "Command-"  # shortcut key modifier

else:  # *nix, Xwindows and Windows, UNTESTED
    libtk = "N/A"
    C_Key = "Control-"  # shortcut key modifier


class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    _geometry = ''
    _stopped  = None

    def __init__(self, parent, title=None, video=''):
        Tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title(title or "tkVLCplayer")
        self.video = expanduser(video)

        # Menu Bar
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Play", command=self.OnPlay)
        fileMenu.add_command(label="Stop", command=self.OnStop)
        fileMenu.add_separator()
        fileMenu.add_command(label="Silenciar", command=self.OnMute)
        fileMenu.add_separator()
        fileMenu.add_command(label="Cerrar", command=self.OnClose)
        menubar.add_cascade(label="Controles", menu=fileMenu)

        self.fileMenu = fileMenu
        self.playIndex = fileMenu.index("Play")
        self.muteIndex = fileMenu.index("Silenciar")

        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)
        self.canvas.pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # VLC player
        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        self.volMuted = False


        self.parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        self.parent.update()

        # Start playing the video
        self.OnPlay()

    def OnClose(self, *unused):
        """Closes the window and quit.
        """
        #print("LOLA says bye!")
        #self._stopped = True
        
        self.OnStop()
        self.parent.destroy()

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?

    def OnMute(self, *unused):
        """Mute/Unmute audio.
        """
        # audio un/mute may be unreliable, see vlc.py docs.
        self.volMuted = m = not self.volMuted  # self.player.audio_get_mute()
        self.player.audio_set_mute(m)
        u = "No silenciar" if m else "Silenciar"
        self.fileMenu.entryconfig(self.muteIndex, label=u)

    def _Pause_Play(self, playing):
        # re-label menu item and button, adjust callbacks
        p = 'Pause' if playing else 'Play'
        c = self.OnPlay if playing is None else self.OnPause
        self.fileMenu.entryconfig(self.playIndex, label=p, command=c)
        # self.fileMenu.bind_shortcut('p', c)  # XXX handled
        self._stopped = False

    def _Play(self, video):
        # helper for OnOpen and OnPlay
        if isfile(video):  # Creation
            m = self.Instance.media_new(str(video))  # Path, unicode
            self.player.set_media(m)
            self.parent.title("tkVLCplayer - %s" % (basename(video),))

            # set the window id where to render VLC's video output
            h = self.videopanel.winfo_id()  # .winfo_visualid()?
            if _isWindows:
                self.player.set_hwnd(h)
            elif _isMacOS:
                # XXX 1) using the videopanel.winfo_id() handle
                # causes the video to play in the entire panel on
                # macOS, covering the buttons, sliders, etc.
                # XXX 2) .winfo_id() to return NSView on macOS?
                v = _GetNSView(h)
                if v:
                    self.player.set_nsobject(v)
                else:
                    self.player.set_xwindow(h)  # plays audio, no video
            else:
                self.player.set_xwindow(h)  # fails on Windows
            # FIXME: this should be made cross-platform
            self.OnPlay()

    def OnPause(self, *unused):
        """Toggle between Pause and Play.
        """
        if self.player.get_media():
            self._Pause_Play(not self.player.is_playing())
            self.player.pause()  # toggles

    def OnPlay(self, *unused):
        """Play video, if none is loaded, open the dialog window.
        """
        # if there's no video to play or playing,
        # open a Tk.FileDialog to select a file
        if not self.player.get_media():
            if self.video:
                self._Play(expanduser(self.video))
                self.video = ''
            else:
                self.OnOpen()
        # Try to play, if this fails display an error message
        elif self.player.play():  # == -1
            self.showError("Unable to play the video.")
        else:
            self._Pause_Play(True)
            # set volume slider to audio level
            vol = self.player.audio_get_volume()

    def OnResize(self, *unused):
        """Adjust the window/frame to the video aspect ratio.
        """
        g = self.parent.geometry()
        if g != self._geometry and self.player:
            u, v = self.player.video_get_size()  # often (0, 0)
            if v > 0 and u > 0:
                # get window size and position
                g, x, y = g.split('+')
                w, h = g.split('x')
                # alternatively, use .winfo_...
                # w = self.parent.winfo_width()
                # h = self.parent.winfo_height()
                # x = self.parent.winfo_x()
                # y = self.parent.winfo_y()
                # use the video aspect ratio ...
                if u > v:  # ... for landscape
                    # adjust the window height
                    h = round(float(w) * v / u)
                else:  # ... for portrait
                    # adjust the window width
                    w = round(float(h) * u / v)
                self.parent.geometry("%sx%s+%s+%s" % (w, h, x, y))
                self._geometry = self.parent.geometry()  # actual

    def OnStop(self, *unused):
        """Stop the player, resets media.
        """
        if self.player:
            self.player.stop()
            self._Pause_Play(None)
            self._stopped = True

    def showError(self, message):
        """Display a simple error dialog.
        """
        self.OnStop()
        showerror(self.parent.title(), message)
