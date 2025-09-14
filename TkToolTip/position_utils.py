"""
Position calculation utilities for TkToolTip.

This module contains functions for calculating and adjusting tooltip positions
to ensure they stay within screen bounds and don't overlap with the mouse cursor.
"""

from tkinter import Toplevel, Label, Widget, Event

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import TkToolTip


def calculate_position(tip: 'TkToolTip', event: Event):
    """Calculate the position for the tooltip based on origin and anchor settings."""
    if tip.origin == "mouse":
        x: int = event.x_root + tip.padx
        y: int = event.y_root + tip.pady
    else:  # origin is "widget"
        widget: Widget = tip.widget
        x, y, widget_width, widget_height = _get_widget_geometry(widget)
        anchor_value = tip.anchor.lower() if tip.anchor else ""
        is_centered = (all(d in anchor_value for d in ['n', 's', 'e', 'w']) or anchor_value in {"center", "c"})
        if is_centered:
            x += widget_width // 2
            y += widget_height // 2
        else:
            # Horizontal
            if "e" in anchor_value:
                x += widget_width
            elif "w" not in anchor_value:
                x += widget_width // 2
            # Vertical
            if "s" in anchor_value:
                y += widget_height
            elif "n" not in anchor_value:
                y += widget_height // 2
        x += tip.padx
        y += tip.pady
    # Ensure tooltip stays within screen bounds and away from mouse (unless origin is widget)
    return adjust_position_for_screen_bounds(tip, x, y, event.x_root, event.y_root, tip.origin)


def adjust_position_for_screen_bounds(tip: 'TkToolTip', x: int, y: int, mouse_x: int, mouse_y: int, origin: str):
    """Adjust tooltip position to keep it within screen bounds and away from mouse."""
    widget: Widget = tip.widget
    screen_width: int = widget.winfo_screenwidth()
    screen_height: int = widget.winfo_screenheight()
    tip_width, tip_height = _estimate_tip_size(tip)
    # Only avoid mouse overlap when origin is "mouse"
    if origin == "mouse":
        mouse_padding = 20
        tip_overlaps_mouse = _check_tip_overlaps_mouse(x, y, tip_width, tip_height, mouse_x, mouse_y, mouse_padding)
        if tip_overlaps_mouse:
            x, y = _reposition_away_from_mouse(x, y, tip_width, tip_height, mouse_x, mouse_y, screen_width, screen_height, mouse_padding)
    # Always ensure tooltip stays within screen bounds
    x, y = _adjust_for_screen_bounds(x, y, tip_width, tip_height, screen_width, screen_height)
    return x, y


def _get_widget_geometry(widget: Widget):
    """Get the geometry of a widget: (x, y, width, height)."""
    widget_width: int = widget.winfo_width()
    widget_height: int = widget.winfo_height()
    widget_x: int = widget.winfo_rootx()
    widget_y: int = widget.winfo_rooty()
    x: int = widget_x
    y: int = widget_y
    return x, y, widget_width, widget_height


def _estimate_tip_size(tip: 'TkToolTip'):
    """Estimate tooltip size by creating a temporary window."""
    temp_window = Toplevel(tip.widget)
    temp_window.withdraw()
    temp_window.wm_overrideredirect(True)
    temp_label = Label(temp_window,
        text=tip.text,
        font=tip.font,
        relief=tip.relief,
        borderwidth=tip.borderwidth,
        justify=tip.justify,
        wraplength=tip.wraplength
    )
    temp_label.pack(ipadx=tip.ipadx, ipady=tip.ipady)
    temp_window.update_idletasks()
    tip_width = temp_label.winfo_reqwidth()
    tip_height = temp_label.winfo_reqheight()
    temp_window.destroy()
    return tip_width, tip_height


def _check_tip_overlaps_mouse(x, y, tip_width, tip_height, mouse_x, mouse_y, mouse_padding=20):
    """Check if tooltip overlaps with mouse cursor."""
    return (
        mouse_x >= x - mouse_padding and mouse_x <= x + tip_width + mouse_padding and
        mouse_y >= y - mouse_padding and mouse_y <= y + tip_height + mouse_padding
    )


def _reposition_away_from_mouse(x, y, tip_width, tip_height, mouse_x, mouse_y, screen_width, screen_height, mouse_padding=20):
    """Try to reposition tooltip away from mouse cursor."""
    # Try positioning below the mouse first
    new_y = mouse_y + mouse_padding
    if new_y + tip_height <= screen_height - 5:
        y = new_y
    else:
        # If below doesn't work, try above
        new_y = mouse_y - tip_height - mouse_padding
        if new_y >= 5:
            y = new_y
        else:
            # If neither above nor below works, try to the side
            new_x = mouse_x + mouse_padding
            if new_x + tip_width <= screen_width - 5:
                x = new_x
            else:
                x = mouse_x - tip_width - mouse_padding
    return x, y


def _adjust_for_screen_bounds(x, y, tip_width, tip_height, screen_width, screen_height):
    """Adjust tooltip position for screen bounds."""
    if x + tip_width > screen_width:
        x = screen_width - tip_width - 5
    if x < 0:
        x = 5
    if y + tip_height > screen_height:
        y = screen_height - tip_height - 5
    if y < 0:
        y = 5
    return x, y
