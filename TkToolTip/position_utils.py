"""
Position calculation utilities for TkToolTip.

This module contains functions for calculating and adjusting tooltip positions
to ensure they stay within screen bounds and don't overlap with the mouse cursor.
"""

from tkinter import Toplevel, Label, Widget, Event

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import TkToolTip


def calculate_position(tooltip_instance: 'TkToolTip', event: Event):
    """Calculate the position for the tooltip based on origin and anchor settings."""
    if tooltip_instance.origin == "mouse":
        x: int = event.x_root + tooltip_instance.padx
        y: int = event.y_root + tooltip_instance.pady
    else:  # origin is "widget"
        widget: Widget = tooltip_instance.widget
        x, y, widget_width, widget_height = _get_widget_geometry(widget)
        anchor_value = tooltip_instance.anchor.lower() if tooltip_instance.anchor else ""
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
        x += tooltip_instance.padx
        y += tooltip_instance.pady
    # Ensure tooltip stays within screen bounds and away from mouse
    return adjust_position_for_screen_bounds(tooltip_instance, x, y, event.x_root, event.y_root)


def adjust_position_for_screen_bounds(tooltip_instance: 'TkToolTip', x: int, y: int, mouse_x: int, mouse_y: int):
    """Adjust tooltip position to keep it within screen bounds and away from mouse."""
    widget: Widget = tooltip_instance.widget
    screen_width: int = widget.winfo_screenwidth()
    screen_height: int = widget.winfo_screenheight()
    tooltip_width, tooltip_height = _estimate_tooltip_size(tooltip_instance)
    mouse_padding = 20
    tooltip_overlaps_mouse = _check_tooltip_overlaps_mouse(x, y, tooltip_width, tooltip_height, mouse_x, mouse_y, mouse_padding)
    if tooltip_overlaps_mouse:
        x, y = _reposition_away_from_mouse(x, y, tooltip_width, tooltip_height, mouse_x, mouse_y, screen_width, screen_height, mouse_padding)
    x, y = _adjust_for_screen_bounds(x, y, tooltip_width, tooltip_height, screen_width, screen_height)
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


def _estimate_tooltip_size(tooltip_instance: 'TkToolTip'):
    """Estimate tooltip size by creating a temporary window."""
    temp_window = Toplevel(tooltip_instance.widget)
    temp_window.withdraw()
    temp_window.wm_overrideredirect(True)
    temp_label = Label(temp_window,
        text=tooltip_instance.text,
        font=tooltip_instance.font,
        relief=tooltip_instance.relief,
        borderwidth=tooltip_instance.borderwidth,
        justify=tooltip_instance.justify,
        wraplength=tooltip_instance.wraplength
    )
    temp_label.pack(ipadx=tooltip_instance.ipadx, ipady=tooltip_instance.ipady)
    temp_window.update_idletasks()
    tooltip_width = temp_label.winfo_reqwidth()
    tooltip_height = temp_label.winfo_reqheight()
    temp_window.destroy()
    return tooltip_width, tooltip_height


def _check_tooltip_overlaps_mouse(x, y, tooltip_width, tooltip_height, mouse_x, mouse_y, mouse_padding=20):
    """Check if tooltip overlaps with mouse cursor."""
    return (
        mouse_x >= x - mouse_padding and mouse_x <= x + tooltip_width + mouse_padding and
        mouse_y >= y - mouse_padding and mouse_y <= y + tooltip_height + mouse_padding
    )


def _reposition_away_from_mouse(x, y, tooltip_width, tooltip_height, mouse_x, mouse_y, screen_width, screen_height, mouse_padding=20):
    """Try to reposition tooltip away from mouse cursor."""
    # Try positioning below the mouse first
    new_y = mouse_y + mouse_padding
    if new_y + tooltip_height <= screen_height - 5:
        y = new_y
    else:
        # If below doesn't work, try above
        new_y = mouse_y - tooltip_height - mouse_padding
        if new_y >= 5:
            y = new_y
        else:
            # If neither above nor below works, try to the side
            new_x = mouse_x + mouse_padding
            if new_x + tooltip_width <= screen_width - 5:
                x = new_x
            else:
                x = mouse_x - tooltip_width - mouse_padding
    return x, y


def _adjust_for_screen_bounds(x, y, tooltip_width, tooltip_height, screen_width, screen_height):
    """Adjust tooltip position for screen bounds."""
    if x + tooltip_width > screen_width:
        x = screen_width - tooltip_width - 5
    if x < 0:
        x = 5
    if y + tooltip_height > screen_height:
        y = screen_height - tooltip_height - 5
    if y < 0:
        y = 5
    return x, y
