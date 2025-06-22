"""
Position calculation utilities for TkToolTip.

This module contains functions for calculating and adjusting tooltip positions
to ensure they stay within screen bounds and don't overlap with the mouse cursor.
"""

from tkinter import Toplevel, Label

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import TkToolTip


def calculate_position(tooltip_instance: 'TkToolTip', event):
    """Calculate the position for the tooltip based on origin and anchor settings."""
    if tooltip_instance.origin == "mouse":
        x, y = event.x_root + tooltip_instance.padx, event.y_root + tooltip_instance.pady
    else:  # origin is "widget"
        widget_width = tooltip_instance.widget.winfo_width()
        widget_height = tooltip_instance.widget.winfo_height()
        widget_x = tooltip_instance.widget.winfo_rootx()
        widget_y = tooltip_instance.widget.winfo_rooty()
        x, y = widget_x, widget_y
        is_centered = all(d in tooltip_instance.anchor for d in ['n', 's', 'e', 'w'])
        if is_centered:
            x += widget_width // 2
            y += widget_height // 2
        else:
            # Horizontal
            if "e" in tooltip_instance.anchor:
                x += widget_width
            elif "w" not in tooltip_instance.anchor:
                x += widget_width // 2
            # Vertical
            if "s" in tooltip_instance.anchor:
                y += widget_height
            elif "n" not in tooltip_instance.anchor:
                y += widget_height // 2
        x += tooltip_instance.padx
        y += tooltip_instance.pady
    # Ensure tooltip stays within screen bounds and away from mouse
    return adjust_position_for_screen_bounds(tooltip_instance, x, y, event.x_root, event.y_root)


def adjust_position_for_screen_bounds(tooltip_instance: 'TkToolTip', x, y, mouse_x, mouse_y):
    """Adjust tooltip position to keep it within screen bounds and away from mouse."""
    # Get screen dimensions
    screen_width = tooltip_instance.widget.winfo_screenwidth()
    screen_height = tooltip_instance.widget.winfo_screenheight()
    # Estimate tooltip size (create temporary window to measure)
    temp_window = Toplevel(tooltip_instance.widget)
    temp_window.withdraw()  # Hide it immediately
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
    # Update to get actual size
    temp_window.update_idletasks()
    tooltip_width = temp_label.winfo_reqwidth()
    tooltip_height = temp_label.winfo_reqheight()
    # Clean up temporary window
    temp_window.destroy()
    # Check if tooltip would overlap with mouse cursor (with some padding)
    mouse_padding = 20  # Minimum distance from mouse cursor
    tooltip_overlaps_mouse = (
        mouse_x >= x - mouse_padding and mouse_x <= x + tooltip_width + mouse_padding and
        mouse_y >= y - mouse_padding and mouse_y <= y + tooltip_height + mouse_padding
    )
    # If overlapping with mouse, try to reposition
    if tooltip_overlaps_mouse:
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
    # Adjust horizontal position for screen bounds
    if x + tooltip_width > screen_width:
        x = screen_width - tooltip_width - 5  # 5px margin from edge
    if x < 0:
        x = 5
    # Adjust vertical position for screen bounds
    if y + tooltip_height > screen_height:
        y = screen_height - tooltip_height - 5  # 5px margin from edge
    if y < 0:
        y = 5
    return x, y
