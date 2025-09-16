"""
Position calculation utilities for TkToolTip.

This module contains functions for calculating and adjusting tooltip positions
to ensure they stay within screen bounds and don't overlap with the mouse cursor.
"""

# Typing
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import TkToolTip

# Standard - GUI
from tkinter import Toplevel, Label, Widget, Event



def anchor_to_relative(anchor: str) -> tuple[float, float]:
    """Convert an anchor string to relative (x,y) within a rectangle."""
    a = (anchor or "nw").lower()
    if a in ("center", "c") or set(a) == set("nesw"):
        return 0.5, 0.5
    x_rel = 0.5
    y_rel = 0.5
    if "n" in a:
        y_rel = 0.0
    elif "s" in a:
        y_rel = 1.0
    if "w" in a:
        x_rel = 0.0
    elif "e" in a:
        x_rel = 1.0
    return x_rel, y_rel


def calculate_tooltip_position(tip: 'TkToolTip', event: Event) -> tuple[int, int]:
    """Calculate the position for the tooltip based on origin and anchor settings."""
    if tip.origin == "mouse":
        x: int = event.x_root + tip.padx
        y: int = event.y_root + tip.pady
        return adjust_position_for_screen_bounds(tip, x, y, event.x_root, event.y_root, tip.origin)
    # origin == "widget"
    widget = tip.widget
    x0, y0, w, h = _get_widget_geometry(widget)
    w_rel_x, w_rel_y = anchor_to_relative(getattr(tip, "widget_anchor", "nw"))
    # Anchor point on widget
    anchor_px_x = x0 + int(w_rel_x * w)
    anchor_px_y = y0 + int(w_rel_y * h)
    tip_w, tip_h = _estimate_tip_size(tip)
    t_rel_x, t_rel_y = anchor_to_relative(getattr(tip, "tooltip_anchor", "nw"))
    # Offset inside tooltip from its top-left to its anchor point
    tip_offset_x = int(t_rel_x * tip_w)
    tip_offset_y = int(t_rel_y * tip_h)
    x = anchor_px_x - tip_offset_x + tip.padx
    y = anchor_px_y - tip_offset_y + tip.pady
    return adjust_position_for_screen_bounds(tip, x, y, event.x_root, event.y_root, tip.origin)


def adjust_position_for_screen_bounds(tip: 'TkToolTip', x: int, y: int, mouse_x: int, mouse_y: int, origin: str) -> tuple[int, int]:
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


def _get_widget_geometry(widget: Widget) -> tuple[int, int, int, int]:
    """Get the geometry of a widget: (x, y, width, height)."""
    widget.update_idletasks()
    widget_width: int = widget.winfo_width()
    widget_height: int = widget.winfo_height()
    widget_x: int = widget.winfo_rootx()
    widget_y: int = widget.winfo_rooty()
    x: int = widget_x
    y: int = widget_y
    return x, y, widget_width, widget_height


def _estimate_tip_size(tip: 'TkToolTip') -> tuple[int, int]:
    """Estimate tooltip size by creating a temporary window."""
    temp_window = Toplevel(tip.widget)
    temp_window.withdraw()
    temp_window.wm_overrideredirect(True)
    temp_label = Label(temp_window,
        text=tip._get_text() if hasattr(tip, "_get_text") else tip.text,
        font=tip.font,
        relief=tip.relief,
        borderwidth=tip.borderwidth,
        justify=tip.justify,
        wraplength=tip.wraplength
    )
    temp_label.pack(ipadx=tip.ipadx, ipady=tip.ipady)
    temp_window.update_idletasks()
    tip_width = temp_window.winfo_reqwidth()
    tip_height = temp_window.winfo_reqheight()
    temp_window.destroy()
    return tip_width, tip_height


def _check_tip_overlaps_mouse(x: int, y: int, tip_width: int, tip_height: int, mouse_x: int, mouse_y: int, mouse_padding: int = 20) -> bool:
    """Check if tooltip overlaps with mouse cursor."""
    return (
        mouse_x >= x - mouse_padding and mouse_x <= x + tip_width + mouse_padding and
        mouse_y >= y - mouse_padding and mouse_y <= y + tip_height + mouse_padding
    )


def _reposition_away_from_mouse(x: int, y: int, tip_width: int, tip_height: int, mouse_x: int, mouse_y: int, screen_width: int, screen_height: int, mouse_padding: int = 20) -> tuple[int, int]:
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


def _adjust_for_screen_bounds(x: int, y: int, tip_width: int, tip_height: int, screen_width: int, screen_height: int) -> tuple[int, int]:
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
