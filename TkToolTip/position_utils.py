"""
Position calculation utilities for TkToolTip.

This module contains functions for calculating and adjusting tooltip positions
to ensure they stay within screen bounds. Note: tooltips are allowed to
be drawn over the mouse pointer (no avoidance/repositioning).
"""


from __future__ import annotations

# Standard
import sys

# Standard - GUI
from tkinter import Toplevel, Label, Widget, Event, Frame
from tkinter.ttk import Separator

# Typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import TkToolTip


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


def resolve_tooltip_anchor_offsets(tip: 'TkToolTip') -> tuple[int, int, int, int]:
    tip_width, tip_height = _estimate_tip_size(tip)
    t_rel_x, t_rel_y = anchor_to_relative(getattr(tip, "tooltip_anchor", "nw"))
    tip_offset_x = int(t_rel_x * tip_width)
    tip_offset_y = int(t_rel_y * tip_height)
    return tip_width, tip_height, tip_offset_x, tip_offset_y


def calculate_tooltip_position(tip: 'TkToolTip', event: Event) -> tuple[int, int]:
    """Calculate the position for the tooltip based on origin and anchor settings."""
    if tip.origin == "mouse":
        _, _, tip_offset_x, tip_offset_y = resolve_tooltip_anchor_offsets(tip)
        anchor_px_x = event.x_root
        anchor_px_y = event.y_root
        x = anchor_px_x - tip_offset_x + tip.padx
        y = anchor_px_y - tip_offset_y + tip.pady
        return adjust_position_for_screen_bounds(tip, x, y, event.x_root, event.y_root, tip.origin)
    # origin == "widget"
    widget = tip.widget
    tip_width, tip_height, tip_offset_x, tip_offset_y = resolve_tooltip_anchor_offsets(tip)
    x0, y0, w, h = _get_widget_geometry(widget)
    w_rel_x, w_rel_y = anchor_to_relative(getattr(tip, "widget_anchor", "nw"))
    # Anchor point on widget
    anchor_px_x = x0 + int(w_rel_x * w)
    anchor_px_y = y0 + int(w_rel_y * h)
    x = anchor_px_x - tip_offset_x + tip.padx
    y = anchor_px_y - tip_offset_y + tip.pady
    # Only clamp to screen — do not avoid the mouse pointer
    return adjust_position_for_screen_bounds(tip, x, y, event.x_root, event.y_root, tip.origin)


def adjust_position_for_screen_bounds(tip: 'TkToolTip', x: int, y: int, mouse_x: int, mouse_y: int, origin: str) -> tuple[int, int]:
    """Adjust tooltip position to keep it within screen bounds.

    NOTE: This function no longer performs any repositioning to avoid the mouse cursor.
    The tooltip may be drawn over the mouse; only screen-bound clamping is applied.
    """
    work_left, work_top, work_right, work_bottom = _get_screen_work_area(tip.widget)
    tip_width, tip_height = _estimate_tip_size(tip)

    # Ensure tooltip stays within screen bounds (clamp to work area with a small margin)
    return _adjust_for_screen_bounds(x, y, tip_width, tip_height, work_left, work_top, work_right, work_bottom)


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
    """Estimate tooltip size by creating a temporary window.

    For list/tuple text values, mirror the visual structure used in
    TkToolTip._build_tooltip_content so the size matches multi-line tooltips.
    """
    temp_window = Toplevel(tip.widget)
    temp_window.withdraw()
    temp_window.wm_overrideredirect(True)

    try:
        get_text = getattr(tip, "_get_text", None)
        parse_item_flags = getattr(tip, "_parse_item_flags", None)
        bg = getattr(tip, "bg", "white")
        fg = getattr(tip, "fg", "black")
        font = getattr(tip, "font", None)
        justify_default = getattr(tip, "justify", "center")
        wraplength = getattr(tip, "wraplength", 0)
        ipadx = getattr(tip, "ipadx", 2)
        ipady = getattr(tip, "ipady", 2)
        borderwidth = getattr(tip, "borderwidth", 1)
        relief = getattr(tip, "relief", "solid")
        # Get the value in a single place
        value = get_text() if callable(get_text) else tip.text
        # Normalize tuples to lists for consistency
        if isinstance(value, tuple):
            value = list(value)
        # Precompute justify-anchor map
        justify_to_anchor = {"left": "w", "center": "center", "right": "e"}
        if isinstance(value, (list, tuple)):
            # Create same container + labels + separators as the real tooltip
            container = Frame(temp_window, background=bg, relief=relief, borderwidth=borderwidth)
            container.pack()
            count = len(value)
            for idx, item in enumerate(value):
                if callable(parse_item_flags):
                    item_text, item_justify, item_anchor = parse_item_flags(str(item))
                else:
                    item_text, item_justify, item_anchor = str(item), None, None
                eff_justify = item_justify or justify_default
                eff_anchor = item_anchor or justify_to_anchor.get(eff_justify, "center")
                lbl = Label(container, text=item_text, background=bg, foreground=fg, font=font, justify=eff_justify, wraplength=wraplength, borderwidth=0, relief="flat", anchor=eff_anchor)
                lbl.pack(fill='x', ipadx=ipadx, ipady=ipady)
                if idx < count - 1:
                    sep = Separator(container, orient='horizontal')
                    sep.pack(fill='x')
        else:
            anchor_from_justify = justify_to_anchor.get(justify_default, "center")
            lbl = Label(temp_window, text=str(value), background=bg, foreground=fg, font=font, justify=justify_default, wraplength=wraplength, borderwidth=borderwidth, relief=relief, anchor=anchor_from_justify)
            lbl.pack(ipadx=ipadx, ipady=ipady)

        temp_window.update_idletasks()
        tip_width = temp_window.winfo_reqwidth()
        tip_height = temp_window.winfo_reqheight()
    finally:
        try:
            temp_window.destroy()
        except Exception:
            pass

    return tip_width, tip_height


def _adjust_for_screen_bounds(x: int, y: int, tip_width: int, tip_height: int, work_left: int, work_top: int, work_right: int, work_bottom: int) -> tuple[int, int]:
    """Adjust tooltip position for screen bounds."""
    margin = 5
    min_x = work_left + margin
    max_x = work_right - tip_width - margin
    min_y = work_top + margin
    max_y = work_bottom - tip_height - margin
    if max_x < min_x:
        x = work_left
    else:
        x = min(max(x, min_x), max_x)
    if max_y < min_y:
        y = work_top
    else:
        y = min(max(y, min_y), max_y)
    return x, y


def _get_screen_work_area(widget: Widget) -> tuple[int, int, int, int]:
    """Return the usable screen area, excluding the Windows taskbar when possible."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            SPI_GETWORKAREA = 0x0030
            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_int),
                    ("top", ctypes.c_int),
                    ("right", ctypes.c_int),
                    ("bottom", ctypes.c_int),
                ]
            rect = RECT()
            if ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
                return rect.left, rect.top, rect.right, rect.bottom
        except Exception:
            pass
    screen_width: int = widget.winfo_screenwidth()
    screen_height: int = widget.winfo_screenheight()
    return 0, 0, screen_width, screen_height
def _adjust_for_screen_bounds(x: int, y: int, tip_width: int, tip_height: int, work_left: int, work_top: int, work_right: int, work_bottom: int) -> tuple[int, int]:
    """Adjust tooltip position for screen bounds."""
    margin = 5
    min_x = work_left + margin
    max_x = work_right - tip_width - margin
    min_y = work_top + margin
    max_y = work_bottom - tip_height - margin
    if max_x < min_x:
        x = work_left
    else:
        x = min(max(x, min_x), max_x)
    if max_y < min_y:
        y = work_top
    else:
        y = min(max(y, min_y), max_y)
    return x, y


def _get_screen_work_area(widget: Widget) -> tuple[int, int, int, int]:
    """Return the usable screen area, excluding the Windows taskbar when possible."""
    if sys.platform.startswith("win"):
        try:
            import ctypes
            SPI_GETWORKAREA = 0x0030
            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_int),
                    ("top", ctypes.c_int),
                    ("right", ctypes.c_int),
                    ("bottom", ctypes.c_int),
                ]
            rect = RECT()
            if ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
                return rect.left, rect.top, rect.right, rect.bottom
        except Exception:
            pass
    screen_width: int = widget.winfo_screenwidth()
    screen_height: int = widget.winfo_screenheight()
    return 0, 0, screen_width, screen_height
