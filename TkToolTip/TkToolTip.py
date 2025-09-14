"""
Name:     TkToolTip
Author:   github.com/Nenotriple
Version:  1.12

Description:
------------
Add customizable tooltips to any tkinter widget.

Usage:
------
A) Directly create a tooltip:
     TkToolTip.create(widget, text="example")

B) Create and store a tooltip for later configuration:
     tooltip = TkToolTip.create(widget, text="example")
     tooltip.config(text="Example!")
"""


#region Imports

# Standard
from typing import Optional, Tuple

# Standard - GUI
from tkinter import Toplevel, Label

# Local
from .position_utils import calculate_position

#endregion
#region TkToolTip


class TkToolTip:
    """
    Attach a Tooltip to any tkinter widget.

    Parameters
    ----------
    widget : tkinter.Widget, optional
        The widget to attach the tooltip to

    text : str, optional
        Tooltip text ("")

    state : str, optional
        Tooltip state, "normal" or "disabled" ("normal")

    bg : str, optional
        Background color ("#ffffee")

    fg : str, optional
        Foreground (text) color ("black")

    font : tuple, optional
        Font of the text (("TkDefaultFont", 8, "normal"))

    borderwidth : int, optional
        Border width (1)

    relief : str, optional
        Border style ("solid")

    justify : str, optional
        Text justification ("center")

    wraplength : int, optional
        Maximum line width for text wrapping (0 disables wrapping)

    padx : int, optional
        X-offset of the tooltip from the origin (1)

    pady : int, optional
        Y-offset of the tooltip from the origin (1)

    ipadx : int, optional
        Horizontal internal padding (2)

    ipady : int, optional
        Vertical internal padding (2)

    origin : str, optional
        Origin point of the tooltip, "mouse" or "widget" ("mouse")

    anchor : str, optional
        Position of the tooltip relative to the widget when origin is "widget" ("nw").
        Valid values are combinations of n, e, s, w (north, east, south, west). For example,
        "ne" positions at top-right, "sw" at bottom-left. The special values "center" or
        "c" explicitly center the tooltip relative to the widget. For backward compatibility,
        specifying all four directions together ("nesw") is also treated as center.

    follow_mouse : bool, optional
        When True, the tooltip follows the mouse while hovering over the widget.
        This ignores "origin" and "anchor" when active. (False)

    show_delay : int, optional
        Delay before showing the tooltip in milliseconds (10)

    hide_delay : int, optional
        Force hiding the tooltip after this many milliseconds (3000). After hiding
        due to this timeout, the tooltip will not reappear until the mouse leaves
        the widget and hovers back over it.

    fade_in : int, optional
        Fade-in time in milliseconds (125)

    fade_out : int, optional
        Fade-out time in milliseconds (50)

    Methods
    -------
    create(cls, widget, **kwargs)
        Create a tooltip for the widget with the given parameters.

    config(**kwargs)
        Update the tooltip configuration.
    """


    #region Defaults


    # Class-level default parameters
    TEXT = ""
    STATE = "normal"
    BG = "#ffffee"
    FG = "black"
    FONT: Optional[Tuple[str, int, str]]  = ("TkDefaultFont", 8, "normal")
    BORDERWIDTH = 1
    RELIEF = "solid"
    JUSTIFY = "center"
    WRAPLENGTH = 0
    PADX = 1
    PADY = 1
    IPADX = 2
    IPADY = 2
    ORIGIN = "mouse"
    ANCHOR = "nw"
    FOLLOW_MOUSE = False
    SHOW_DELAY = 10
    HIDE_DELAY = 3000
    FADE_IN = 125
    FADE_OUT = 50

    #endregion
    #region Init


    def __init__(self,
                widget=None,
                text=None,
                state=None,
                bg=None,
                fg=None,
                font=None,
                borderwidth=None,
                relief=None,
                justify=None,
                wraplength=None,
                padx=None,
                pady=None,
                ipadx=None,
                ipady=None,
                origin=None,
                anchor=None,
                follow_mouse=None,
                show_delay=None,
                hide_delay=None,
                fade_in=None,
                fade_out=None
                ):
        # Use class-level defaults if not provided
        self.widget = widget
        self.text = self.TEXT if text is None else text
        self.state = self.STATE if state is None else state
        self.bg = self.BG if bg is None else bg
        self.fg = self.FG if fg is None else fg
        self.font = self.FONT if font is None else font
        self.borderwidth = self.BORDERWIDTH if borderwidth is None else borderwidth
        self.relief = self.RELIEF if relief is None else relief
        self.justify = self.JUSTIFY if justify is None else justify
        self.wraplength = self.WRAPLENGTH if wraplength is None else wraplength
        self.padx = self.PADX if padx is None else padx
        self.pady = self.PADY if pady is None else pady
        self.ipadx = self.IPADX if ipadx is None else ipadx
        self.ipady = self.IPADY if ipady is None else ipady
        self.origin = self.ORIGIN if origin is None else origin
        self.anchor = self.ANCHOR if anchor is None else anchor
        self.follow_mouse = self.FOLLOW_MOUSE if follow_mouse is None else follow_mouse
        self.show_delay = self.SHOW_DELAY if show_delay is None else show_delay
        self.hide_delay = self.HIDE_DELAY if hide_delay is None else hide_delay
        self.fade_in = self.FADE_IN if fade_in is None else fade_in
        self.fade_out = self.FADE_OUT if fade_out is None else fade_out
        # Internal states
        self.tip_window = None
        self.widget_id = None
        self.hide_id = None
        self._suppress_until_leave = False

        if widget:
            self._bind_widget()


    #endregion
    #region Public API


    @classmethod
    def create(cls,
            widget,
            text=None,
            state=None,
            bg=None,
            fg=None,
            font=None,
            borderwidth=None,
            relief=None,
            justify=None,
            wraplength=None,
            padx=None,
            pady=None,
            ipadx=None,
            ipady=None,
            origin=None,
            anchor=None,
            follow_mouse=None,
            show_delay=None,
            hide_delay=None,
            fade_in=None,
            fade_out=None
            ):
        """Create a tooltip for the specified widget with the given parameters."""
        return cls(
            widget,
            text if text is not None else cls.TEXT,
            state if state is not None else cls.STATE,
            bg if bg is not None else cls.BG,
            fg if fg is not None else cls.FG,
            font if font is not None else cls.FONT,
            borderwidth if borderwidth is not None else cls.BORDERWIDTH,
            relief if relief is not None else cls.RELIEF,
            justify if justify is not None else cls.JUSTIFY,
            wraplength if wraplength is not None else cls.WRAPLENGTH,
            padx if padx is not None else cls.PADX,
            pady if pady is not None else cls.PADY,
            ipadx if ipadx is not None else cls.IPADX,
            ipady if ipady is not None else cls.IPADY,
            origin if origin is not None else cls.ORIGIN,
            anchor if anchor is not None else cls.ANCHOR,
            follow_mouse if follow_mouse is not None else cls.FOLLOW_MOUSE,
            show_delay if show_delay is not None else cls.SHOW_DELAY,
            hide_delay if hide_delay is not None else cls.HIDE_DELAY,
            fade_in if fade_in is not None else cls.FADE_IN,
            fade_out if fade_out is not None else cls.FADE_OUT
        )


    def config(self,
            text: Optional[str] = None,
            state: Optional[str] = None,
            bg: Optional[str] = None,
            fg: Optional[str] = None,
            font: Optional[Tuple[str, int, str]] = None,
            borderwidth: Optional[int] = None,
            relief: Optional[str] = None,
            justify: Optional[str] = None,
            wraplength: Optional[int] = None,
            padx: Optional[int] = None,
            pady: Optional[int] = None,
            ipadx: Optional[int] = None,
            ipady: Optional[int] = None,
            origin: Optional[str] = None,
            anchor: Optional[str] = None,
            follow_mouse: Optional[bool] = None,
            show_delay: Optional[int] = None,
            hide_delay: Optional[int] = None,
            fade_in: Optional[int] = None,
            fade_out: Optional[int] = None
            ) -> None:
        """Update the tooltip configuration with the given parameters."""
        incoming = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        for param, value in incoming.items():
            if param == 'state':
                assert value in ["normal", "disabled"], "Invalid state"
            setattr(self, param, value)
        if self.tip_window:
            self._update_visible_tooltip()
            # If follow_mouse is active, reposition to the current pointer
            if self.follow_mouse:
                x, y = self._current_follow_position()
                self._move_tip(x, y)
            # If hide_delay changed, reschedule auto-hide
            if 'hide_delay' in incoming:
                self._schedule_auto_hide()


    def hide(self, event=None):
        """Hide the tooltip and cancel any scheduled events."""
        self._cancel_tip()
        self._cancel_auto_hide()
        self._hide_tip()


    #endregion
    #region Bindings


    def _bind_widget(self):
        """Setup event bindings for the widget."""
        self.widget.bind('<Motion>', self._schedule_show_tip, add="+")
        self.widget.bind('<Enter>', self._schedule_show_tip, add="+")
        self.widget.bind('<Leave>', self._on_leave, add="+")
        self.widget.bind("<Button-1>", self.hide, add="+")
        self.widget.bind('<B1-Motion>', self.hide, add="+")


    def _on_leave(self, event=None):
        """Handle mouse leaving the widget: hide and clear suppression."""
        self._suppress_until_leave = False
        self.hide(event)


    #endregion
    #region Show/Pos


    def _schedule_show_tip(self, event):
        """Schedule the tooltip to be shown after the specified delay."""
        # Suppress showing until mouse leaves if auto-hidden recently
        if self._suppress_until_leave:
            self._cancel_tip()
            return
        # If following mouse and already visible, just move the tip
        if self.follow_mouse and self.tip_window:
            self._cancel_tip()
            x, y = self._calculate_follow_position(event)
            self._move_tip(x, y)
            return
        if self.widget_id:
            self.widget.after_cancel(self.widget_id)
        self.widget_id = self.widget.after(self.show_delay, lambda: self._show_tip(event))


    def _show_tip(self, event):
        """Display the tooltip at the specified position."""
        if self.state == "disabled" or not self.text or self._suppress_until_leave:
            return
        if self.follow_mouse:
            x, y = self._calculate_follow_position(event)  # ignores origin/anchor
        else:
            x, y = calculate_position(self, event)
        self._create_tip_window(x, y)


    def _calculate_follow_position(self, event):
        """Compute position to place the tooltip near the mouse cursor."""
        return event.x_root + self.padx, event.y_root + self.pady


    def _current_follow_position(self):
        """Compute follow position based on current pointer location."""
        return self.widget.winfo_pointerx() + self.padx, self.widget.winfo_pointery() + self.pady


    def _move_tip(self, x, y):
        """Move the tooltip window to the given coordinates."""
        if self.tip_window:
            self.tip_window.wm_geometry(f"+{x}+{y}")


    #endregion
    #region Window


    def _create_tip_window(self, x, y):
        """Create and display the tooltip window."""
        if self.tip_window:
            return
        self.tip_window = Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.attributes("-alpha", 0.0 if self.fade_in else 1.0)
        label = Label(
            self.tip_window,
            text=self.text,
            background=self.bg,
            foreground=self.fg,
            font=self.font,
            relief=self.relief,
            borderwidth=self.borderwidth,
            justify=self.justify,
            wraplength=self.wraplength
        )
        label.pack(ipadx=self.ipadx, ipady=self.ipady)
        if self.fade_in:
            self._fade(self.fade_in, 0.0, 1.0)
        self._schedule_auto_hide()


    def _remove_tip_window(self):
        """Destroy and remove the tooltip window."""
        if self.tip_window:
            try:
                self.tip_window.destroy()
            finally:
                self.tip_window = None


    def _hide_tip(self):
        """Hide or fade out the tooltip window."""
        if self.tip_window:
            if self.fade_out:
                self._fade(self.fade_out, 1.0, 0.0, on_complete=self._remove_tip_window)
            else:
                self._remove_tip_window()


    #endregion
    #region Effects


    def _fade(self, duration, start_alpha, end_alpha, on_complete=None):
        """Fade the tooltip window in or out."""
        if self.tip_window is None:
            return
        steps = max(1, duration // 10)
        alpha_step = (end_alpha - start_alpha) / steps

        def step(current_step):
            if self.tip_window is None:
                return
            alpha = max(0.0, min(1.0, start_alpha + current_step * alpha_step))
            try:
                self.tip_window.attributes("-alpha", alpha)
            except Exception:
                pass
            if current_step < steps:
                self.tip_window.after(10, step, current_step + 1)
            else:
                try:
                    if self.tip_window is not None:
                        self.tip_window.attributes("-alpha", max(0.0, min(1.0, end_alpha)))
                except Exception:
                    pass
                if on_complete:
                    on_complete()

        step(0)


    #endregion
    #region Auto-hide


    def _cancel_tip(self):
        """Cancel the scheduled display of the tooltip."""
        if self.widget_id:
            self.widget.after_cancel(self.widget_id)
            self.widget_id = None


    def _cancel_auto_hide(self):
        """Cancel the scheduled auto-hide if any."""
        if self.hide_id:
            try:
                self.widget.after_cancel(self.hide_id)
            except Exception:
                pass
            self.hide_id = None


    def _schedule_auto_hide(self):
        """Schedule auto-hide if hide_delay is active."""
        self._cancel_auto_hide()
        if self.hide_delay and self.hide_delay > 0:
            self.hide_id = self.widget.after(self.hide_delay, self._auto_hide)


    def _auto_hide(self):
        """Auto-hide triggered by hide_delay and suppress re-show until leave."""
        self._suppress_until_leave = True
        self._cancel_tip()
        self._hide_tip()


    #endregion
    #region Update


    def _update_visible_tooltip(self):
        """Update the tooltip if it's currently visible."""
        if not self.tip_window:
            return
        label = self.tip_window.winfo_children()[0]
        label.config(
            text=self.text,
            background=self.bg,
            foreground=self.fg,
            font=self.font,
            relief=self.relief,
            borderwidth=self.borderwidth,
            justify=self.justify,
            wraplength=self.wraplength
        )
        label.pack(ipadx=self.ipadx, ipady=self.ipady)
        x, y = self.tip_window.winfo_x(), self.tip_window.winfo_y()
        self.tip_window.wm_geometry(f"+{x}+{y}")
        current_alpha = self.tip_window.attributes("-alpha")
        self.tip_window.attributes("-alpha", current_alpha)


    #endregion
#endregion
