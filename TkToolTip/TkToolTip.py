"""
Name:     TkToolTip
Author:   github.com/Nenotriple
Version:  1.12

Description:
------------
Add customizable tooltips to any tkinter widget.
"""


#region Imports

# Standard - GUI
from tkinter import Toplevel, Label, Widget, Event

# Typing
from __future__ import annotations
from typing import Optional, Tuple, Any, Callable, Dict, Union

# Local
from .position_utils import calculate_tooltip_position, adjust_position_for_screen_bounds
from .animation_utils import animate_tip_window, SLIDE_ANIM_DISTANCE


#endregion
#region TkToolTip


class TkToolTip:
    #region Defaults
    # Class-level default parameters
    TEXT = ""
    STATE = "normal"
    BG = "#ffffee"
    FG = "black"
    FONT: Optional[Tuple[str, int, str]]  = ("TkDefaultFont", 8, "normal")
    BORDERWIDTH = 1
    OPACITY = 1.0
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
    SHOW_DELAY = 100
    HIDE_DELAY = 5000
    ANIMATION = "fade"
    ANIM_IN = 75
    ANIM_OUT = 50

    # list of public parameters
    PARAMS = [
        "text", "state", "bg", "fg", "font", "borderwidth", "opacity", "relief",
        "justify", "wraplength", "padx", "pady", "ipadx", "ipady", "origin", "anchor",
        "follow_mouse", "show_delay", "hide_delay", "animation", "anim_in", "anim_out"
    ]

    # For IDEs and type checkers
    widget: Optional[Widget]
    text: Union[str, Callable[[], str]]
    state: str
    bg: str
    fg: str
    font: Optional[Tuple[str, int, str]]
    borderwidth: int
    opacity: float
    relief: str
    justify: str
    wraplength: int
    padx: int
    pady: int
    ipadx: int
    ipady: int
    origin: str
    anchor: str
    follow_mouse: bool
    show_delay: int
    hide_delay: int
    animation: str
    anim_in: int
    anim_out: int


    #endregion
    #region Init


    def __init__(self, widget: Optional[Widget] = None, **kwargs: Any) -> None:
        """Initialize tooltip; kwargs must be among PARAMS."""
        # use unified kwargs processor
        self._apply_kwargs(kwargs, initialize=True)
        # Instance vars
        self.tip_window: Optional[Toplevel] = None
        self.show_after_id: Optional[int] = None
        self.hide_id: Optional[int] = None
        self._suppress_until_leave: bool = False
        # Bind events if widget provided
        self.widget = widget
        if widget:
            self._bind_widget()


    #endregion
    #region Public API


    @classmethod
    def bind(cls, widget: Widget, **kwargs: Any) -> 'TkToolTip':
        """Binds a tooltip for widget; kwargs limited to PARAMS."""
        return cls(widget, **kwargs)


    def unbind(self) -> None:
        """Remove all tooltip-related event bindings from the widget."""
        if self.widget:
            self.widget.unbind('<Motion>')
            self.widget.unbind('<Enter>')
            self.widget.unbind('<Leave>')
            self.widget.unbind('<Button-1>')
            self.widget.unbind('<B1-Motion>')
            self.widget.unbind('<ButtonPress>')
            self.widget.unbind('<ButtonRelease>')
        self.hide()


    def config(self, **kwargs: Any) -> None:
        """Update configuration; only keys in PARAMS are accepted."""
        if not kwargs:
            return
        self._apply_kwargs(kwargs, initialize=False)
        if self.tip_window:
            self._update_visible_tooltip()
            # If follow_mouse is active, reposition to the current pointer
            if self.follow_mouse:
                x, y = self._current_follow_position()
                self._move_tip(x, y)
            # If hide_delay changed, reschedule auto-hide
            if 'hide_delay' in kwargs:
                self._schedule_auto_hide()


    def hide(self, event: Optional[Event] = None) -> None:
        """Hide the tooltip and cancel any scheduled events."""
        self._cancel_tip()
        self._cancel_auto_hide()
        self._hide_tip()


    #endregion
    #region Bindings


    def _bind_widget(self) -> None:
        """Setup event bindings for the widget."""
        self.widget.bind('<Motion>', self._schedule_show_tip, add="+")
        self.widget.bind('<Enter>', self._schedule_show_tip, add="+")
        self.widget.bind('<Leave>', self._on_leave, add="+")
        self.widget.bind("<Button-1>", self.hide, add="+")
        self.widget.bind('<B1-Motion>', self.hide, add="+")
        self.widget.bind('<ButtonPress>', self.hide, add="+")
        self.widget.bind('<ButtonRelease>', self.hide, add="+")


    def _on_leave(self, event: Optional[Event] = None) -> None:
        """Handle mouse leaving the widget: hide and clear suppression."""
        self._suppress_until_leave = False
        self.hide(event)


    #endregion
    #region Show/Pos


    def _schedule_show_tip(self, event: Event) -> None:
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
        if self.show_after_id:
            self.widget.after_cancel(self.show_after_id)
        self.show_after_id = self.widget.after(self.show_delay, lambda: self._show_tip(event))


    def _show_tip(self, event: Event) -> None:
        """Display the tooltip at the specified position."""
        if self.state == "disabled" or not self._get_text() or self._suppress_until_leave:
            return
        if self.follow_mouse:
            x, y = self._calculate_follow_position(event)  # ignores origin/anchor
            x, y = adjust_position_for_screen_bounds(self, x, y, event.x_root, event.y_root, "mouse")
        else:
            x, y = calculate_tooltip_position(self, event)
        self._create_tip_window(x, y)


    def _calculate_follow_position(self, event: Event) -> tuple[int, int]:
        """Compute position to place the tooltip near the mouse cursor."""
        return event.x_root + self.padx, event.y_root + self.pady


    def _current_follow_position(self) -> tuple[int, int]:
        """Compute follow position based on current pointer location."""
        return self.widget.winfo_pointerx() + self.padx, self.widget.winfo_pointery() + self.pady


    def _move_tip(self, x: int, y: int) -> None:
        """Move the tooltip window to the given coordinates."""
        if self.tip_window:
            mouse_x = self.widget.winfo_pointerx()
            mouse_y = self.widget.winfo_pointery()
            x, y = adjust_position_for_screen_bounds(self, x, y, mouse_x, mouse_y, self.origin)
            self.tip_window.wm_geometry(f"+{x}+{y}")


    #endregion
    #region Window


    def _create_tip_window(self, x: int, y: int) -> None:
        """Create and display the tooltip window."""
        if self.tip_window:
            return
        self.tip_window = Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        label = Label(self.tip_window)
        label.pack(ipadx=self.ipadx, ipady=self.ipady)
        self.update_tip_label(label)
        self._animate(show=True)
        self._schedule_auto_hide()


    def _remove_tip_window(self) -> None:
        """Destroy and remove the tooltip window."""
        if self.tip_window:
            try:
                self.tip_window.destroy()
            finally:
                self.tip_window = None


    def _hide_tip(self) -> None:
        """Hide and/or animate hiding the tooltip window."""
        if self.tip_window:
            self._animate(show=False)


    def _animate(self, show: bool) -> None:
        """Unified animation handler for fade and slide."""
        animate_tip_window(
            tip_window=self.tip_window,
            animation=getattr(self, 'animation', 'fade') or 'none',
            show=show,
            opacity=self.opacity,
            anim_in=self.anim_in,
            anim_out=self.anim_out,
            remove_tip_window=self._remove_tip_window
        )


    #endregion
    #region Auto-hide


    def _cancel_tip(self) -> None:
        """Cancel the scheduled display of the tooltip."""
        if self.show_after_id:
            self.widget.after_cancel(self.show_after_id)
            self.show_after_id = None


    def _cancel_auto_hide(self) -> None:
        """Cancel the scheduled auto-hide if any."""
        if self.hide_id:
            try:
                self.widget.after_cancel(self.hide_id)
            except Exception:
                pass
            self.hide_id = None


    def _schedule_auto_hide(self) -> None:
        """Schedule auto-hide if hide_delay is active."""
        self._cancel_auto_hide()
        if self.hide_delay and self.hide_delay > 0:
            self.hide_id = self.widget.after(self.hide_delay, self._auto_hide)


    def _auto_hide(self) -> None:
        """Auto-hide triggered by hide_delay and suppress re-show until leave."""
        self._suppress_until_leave = True
        self._cancel_tip()
        self._hide_tip()


    #endregion
    #region Update


    def _update_visible_tooltip(self) -> None:
        """Update the tooltip if it's currently visible."""
        if not self.tip_window:
            return
        label: Label = self.tip_window.winfo_children()[0]
        self.update_tip_label(label)
        x, y = self.tip_window.winfo_x(), self.tip_window.winfo_y()
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.attributes("-alpha", self.opacity)


    def update_tip_label(self, label: Label) -> None:
        label.config(
            text=self._get_text(),
            background=self.bg,
            foreground=self.fg,
            font=self.font,
            relief=self.relief,
            borderwidth=self.borderwidth,
            justify=self.justify,
            wraplength=self.wraplength
        )


    def _get_text(self) -> str:
        """Return the current tooltip text, calling if it's a function."""
        if callable(self.text):
            try:
                return self.text()
            except Exception:
                return ""
        return self.text


    #endregion
    #region Internal helpers


    def _apply_kwargs(self, kwargs: Dict[str, Any], initialize: bool) -> None:
        """Validate and apply kwargs. If initialize=True, fill unspecified params with defaults."""
        if not kwargs and not initialize:
            return
        # Validate types
        invalid = [k for k in kwargs if k not in self.PARAMS]
        if invalid:
            raise TypeError(f"Invalid parameter(s): {', '.join(invalid)}")
        if initialize:
            # set every param either from kwargs or class-level defaults
            for name in self.PARAMS:
                value = kwargs.get(name, getattr(self, name.upper()))
                if name == 'state':
                    assert value in ["normal", "disabled"], "Invalid state"
                if name == 'opacity':
                    assert 0.0 <= value <= 1.0, "Opacity must be between 0.0 and 1.0"
                setattr(self, name, value)
        # Only set provided params
        else:
            for name, value in kwargs.items():
                if name == 'state':
                    assert value in ["normal", "disabled"], "Invalid state"
                if name == 'opacity':
                    assert 0.0 <= value <= 1.0, "Opacity must be between 0.0 and 1.0"
                setattr(self, name, value)


    #endregion
#endregion
