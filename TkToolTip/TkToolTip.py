"""
# Name:     TkToolTip
# Version:  v1.08
# Author:   github.com/Nenotriple

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


# Standard
import time
from typing import Optional, Tuple

# Standard - GUI
from tkinter import Toplevel, Label


class TkToolTip:
    """
    Attach a Tooltip to any tkinter widget.

    Parameters
    ----------
    widget : tkinter.Widget, optional
        The widget to attach the tooltip to

    text : str, optional
        Tooltip text ("")

    delay : int, optional
        Delay before showing the tooltip in milliseconds (10)

    padx : int, optional
        X-offset of the tooltip from the origin (1)

    pady : int, optional
        Y-offset of the tooltip from the origin (1)

    ipadx : int, optional
        Horizontal internal padding (2)

    ipady : int, optional
        Vertical internal padding (2)

    state : str, optional
        Tooltip state, "normal" or "disabled" (None)

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
        Text justification "center")

    wraplength : int, optional
        Maximum line width for text wrapping, "value=0" disables wrapping (0)

    fade_in : int, optional
        Fade-in time in milliseconds (125)

    fade_out : int, optional
        Fade-out time in milliseconds (50)

    origin : str, optional
        Origin point of the tooltip, "mouse" or "widget" ("mouse")

    anchor : str, optional
        Position of the tooltip relative to the widget when origin is "widget" ("nw").
        Valid values are combinations of n, e, s, w (north, east, south, west).
        For example, "ne" positions at top-right, "sw" at bottom-left, "nesw" centers.


    Methods
    -------
    create(cls, widget, **kwargs)
        Create a tooltip for the widget with the given parameters.

    config(**kwargs)
        Update the tooltip configuration.
    """

    # Class-level default parameters
    TEXT = ""
    DELAY = 10
    PADX = 1
    PADY = 1
    IPADX = 2
    IPADY = 2
    STATE = "normal"
    BG = "#ffffee"
    FG = "black"
    FONT: Optional[Tuple[str, int, str]]  = ("TkDefaultFont", 8, "normal")
    BORDERWIDTH = 1
    RELIEF = "solid"
    JUSTIFY = "center"
    WRAPLENGTH = 0
    FADE_IN = 125
    FADE_OUT = 50
    ORIGIN = "mouse"
    ANCHOR = "nw"

    def __init__(self,
                widget=None,
                text=None,
                delay=None,
                padx=None,
                pady=None,
                ipadx=None,
                ipady=None,
                state=None,
                bg=None,
                fg=None,
                font=None,
                borderwidth=None,
                relief=None,
                justify=None,
                wraplength=None,
                fade_in=None,
                fade_out=None,
                origin=None,
                anchor=None
                ):
        # Use class-level defaults if not provided
        self.widget = widget
        self.text = self.TEXT if text is None else text
        self.delay = self.DELAY if delay is None else delay
        self.padx = self.PADX if padx is None else padx
        self.pady = self.PADY if pady is None else pady
        self.ipadx = self.IPADX if ipadx is None else ipadx
        self.ipady = self.IPADY if ipady is None else ipady
        self.state = self.STATE if state is None else state
        self.bg = self.BG if bg is None else bg
        self.fg = self.FG if fg is None else fg
        self.font = self.FONT if font is None else font
        self.borderwidth = self.BORDERWIDTH if borderwidth is None else borderwidth
        self.relief = self.RELIEF if relief is None else relief
        self.justify = self.JUSTIFY if justify is None else justify
        self.wraplength = self.WRAPLENGTH if wraplength is None else wraplength
        self.fade_in = self.FADE_IN if fade_in is None else fade_in
        self.fade_out = self.FADE_OUT if fade_out is None else fade_out
        self.origin = self.ORIGIN if origin is None else origin
        self.anchor = self.ANCHOR if anchor is None else anchor

        self.tip_window = None
        self.widget_id = None
        self.hide_id = None
        self.hide_time = None

        if widget:
            self._bind_widget()


    def _bind_widget(self):
        """Setup event bindings for the widget."""
        self.widget.bind('<Motion>', self._schedule_show_tip, add="+")
        self.widget.bind('<Enter>', self._schedule_show_tip, add="+")
        self.widget.bind('<Leave>', self._leave_event, add="+")
        self.widget.bind("<Button-1>", self._leave_event, add="+")
        self.widget.bind('<B1-Motion>', self._leave_event, add="+")


    def _leave_event(self, event):
        """Hide the tooltip and cancel any scheduled events."""
        self._cancel_tip()
        self._hide_tip()


    def _schedule_show_tip(self, event):
        """Schedule the tooltip to be shown after the specified delay."""
        if self.widget_id:
            self.widget.after_cancel(self.widget_id)
        self.widget_id = self.widget.after(self.delay, lambda: self._show_tip(event))


    def _calculate_position(self, event):
        """Calculate the position for the tooltip based on origin and anchor settings."""
        if self.origin == "mouse":
            return event.x_root + self.padx, event.y_root + self.pady
        else:  # origin is "widget"
            widget_width = self.widget.winfo_width()
            widget_height = self.widget.winfo_height()
            widget_x = self.widget.winfo_rootx()
            widget_y = self.widget.winfo_rooty()
            x, y = widget_x, widget_y
            is_centered = all(d in self.anchor for d in ['n', 's', 'e', 'w'])
            if is_centered:
                x += widget_width // 2
                y += widget_height // 2
            else:
                # Horizontal
                if "e" in self.anchor:
                    x += widget_width
                elif "w" not in self.anchor:
                    x += widget_width // 2
                # Vertical
                if "s" in self.anchor:
                    y += widget_height
                elif "n" not in self.anchor:
                    y += widget_height // 2
            return x + self.padx, y + self.pady


    def _show_tip(self, event):
        """Display the tooltip at the specified position."""
        if self.state == "disabled" or not self.text:
            return
        x, y = self._calculate_position(event)
        self._create_tip_window(x, y)


    def _create_tip_window(self, x, y):
        """Create and display the tooltip window."""
        if self.tip_window:
            return
        self.tip_window = Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.attributes("-alpha", 0.0 if self.fade_in else 1.0)
        label = Label(self.tip_window,
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


    def _hide_tip(self):
        """Hide or fade out the tooltip window."""
        if self.tip_window:
            if self.fade_out:
                self._fade(self.fade_out, 1.0, 0.0, on_complete=self._remove_tip_window)
            else:
                self._remove_tip_window()


    def _cancel_tip(self):
        """Cancel the scheduled display of the tooltip."""
        if self.widget_id:
            self.widget.after_cancel(self.widget_id)
            self.widget_id = None


    def _remove_tip_window(self):
        """Withdraw and remove the tooltip window."""
        if self.tip_window:
            self.tip_window.withdraw()
            self.tip_window = None
            self.hide_time = time.time()


    def _fade(self, duration, start_alpha, end_alpha, on_complete=None):
        """Fade the tooltip window in or out."""
        if self.tip_window is None:
            return
        steps = max(1, duration // 10)
        alpha_step = (end_alpha - start_alpha) / steps

        def step(current_step):
            if self.tip_window is None:
                return
            alpha = start_alpha + current_step * alpha_step
            self.tip_window.attributes("-alpha", alpha)
            if current_step < steps:
                self.tip_window.after(10, step, current_step + 1)
            else:
                if on_complete:
                    on_complete()
        step(0)


    def _update_visible_tooltip(self):
        """Update the tooltip if it's currently visible"""
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


    def config(self,
            text: Optional[str] = None,
            delay: Optional[int] = None,
            padx: Optional[int] = None,
            pady: Optional[int] = None,
            ipadx: Optional[int] = None,
            ipady: Optional[int] = None,
            state: Optional[str] = None,
            bg: Optional[str] = None,
            fg: Optional[str] = None,
            font: Optional[Tuple[str, int, str]] = None,
            borderwidth: Optional[int] = None,
            relief: Optional[str] = None,
            justify: Optional[str] = None,
            wraplength: Optional[int] = None,
            fade_in: Optional[int] = None,
            fade_out: Optional[int] = None,
            origin: Optional[str] = None,
            anchor: Optional[str] = None
            ) -> None:
        """Update the tooltip configuration with the given parameters."""
        needs_update = False
        for param, value in locals().items():
            if value is not None:
                if param == 'state':
                    assert value in ["normal", "disabled"], "Invalid state"
                if param != 'self':
                    setattr(self, param, value)
                    needs_update = True

        if needs_update and self.tip_window:
            self._update_visible_tooltip()


    @classmethod
    def create(cls,
            widget,
            text=None,
            delay=None,
            padx=None,
            pady=None,
            ipadx=None,
            ipady=None,
            state=None,
            bg=None,
            fg=None,
            font=None,
            borderwidth=None,
            relief=None,
            justify=None,
            wraplength=None,
            fade_in=None,
            fade_out=None,
            origin=None,
            anchor=None
            ):
        """Create a tooltip for the specified widget with the given parameters."""
        return cls(
            widget,
            text if text is not None else cls.TEXT,
            delay if delay is not None else cls.DELAY,
            padx if padx is not None else cls.PADX,
            pady if pady is not None else cls.PADY,
            ipadx if ipadx is not None else cls.IPADX,
            ipady if ipady is not None else cls.IPADY,
            state if state is not None else cls.STATE,
            bg if bg is not None else cls.BG,
            fg if fg is not None else cls.FG,
            font if font is not None else cls.FONT,
            borderwidth if borderwidth is not None else cls.BORDERWIDTH,
            relief if relief is not None else cls.RELIEF,
            justify if justify is not None else cls.JUSTIFY,
            wraplength if wraplength is not None else cls.WRAPLENGTH,
            fade_in if fade_in is not None else cls.FADE_IN,
            fade_out if fade_out is not None else cls.FADE_OUT,
            origin if origin is not None else cls.ORIGIN,
            anchor if anchor is not None else cls.ANCHOR
        )
