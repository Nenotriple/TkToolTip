"""
Animation utilities for TkToolTip.

This module contains functions for handling tooltip animations (fade, slide, etc).
"""


# Standard - GUI
from tkinter import Toplevel

# Typing
from typing import Optional, Callable, Tuple


# Magic Numbers
SLIDE_ANIM_DISTANCE = 8


def animate_tip_window(tip_window: Optional[Toplevel], animation: str, show: bool, opacity: float, anim_in: int, anim_out: int, remove_tip_window: Callable[[], None]) -> None:
    """Unified animation handler for fade and slide."""
    if not tip_window:
        return
    duration = anim_in if show else anim_out
    if not duration or animation == 'none':
        tip_window.attributes("-alpha", opacity if show else 0.0)
        if not show:
            remove_tip_window()
        return
    start_alpha = 0.0 if show else opacity
    end_alpha = opacity if show else 0.0
    if animation == 'fade':
        animate_fade(tip_window, duration, start_alpha, end_alpha, opacity, on_complete=None if show else remove_tip_window)
    elif animation == 'slide':
        base_x, start_y, end_y = get_slide_coords(tip_window, show)
        animate_slide_fade(tip_window, duration, base_x, start_y, base_x, end_y, start_alpha, end_alpha, opacity, on_complete=None if show else remove_tip_window)


def animate_fade(tip_window: Toplevel, duration: int, start_alpha: float, end_alpha: float, opacity: float, on_complete: Optional[Callable[[], None]] = None) -> None:
    """Fade animation."""
    if not tip_window:
        return
    steps = max(1, duration // 10)
    alpha_step = (end_alpha - start_alpha) / steps

    def step(i):
        if not tip_window:
            return
        alpha = max(0.0, min(opacity, start_alpha + i * alpha_step))
        try:
            tip_window.attributes("-alpha", alpha)
        except Exception as e:
            print(f"ERROR: TkToolTip.animation_utils.animate_fade() - {e}")
            pass
        if i < steps:
            tip_window.after(10, step, i + 1)
        else:
            try:
                tip_window.attributes("-alpha", max(0.0, min(opacity, end_alpha)))
            except Exception as e:
                print(f"ERROR: TkToolTip.animation_utils.animate_fade() - {e}")
                pass
            if on_complete:
                on_complete()
    step(0)


def animate_slide_fade(tip_window: Toplevel, duration: int, start_x: int, start_y: int, end_x: int, end_y: int, start_alpha: float, end_alpha: float, opacity: float, on_complete: Optional[Callable[[], None]] = None) -> None:
    """Slide and fade animation."""
    if not tip_window:
        return
    steps = max(1, duration // 10)
    dx = (end_x - start_x) / steps
    dy = (end_y - start_y) / steps
    da = (end_alpha - start_alpha) / steps

    def step(i):
        if not tip_window:
            return
        try:
            new_x = int(start_x + dx * i)
            new_y = int(start_y + dy * i)
            tip_window.wm_geometry(f"+{new_x}+{new_y}")
            alpha = max(0.0, min(opacity, start_alpha + da * i))
            tip_window.attributes("-alpha", alpha)
        except Exception as e:
            print(f"ERROR: TkToolTip.animation_utils.animate_slide_fade() - {e}")
            pass
        if i < steps:
            tip_window.after(10, step, i + 1)
        else:
            try:
                tip_window.attributes("-alpha", max(0.0, min(opacity, end_alpha)))
            except Exception as e:
                print(f"ERROR: TkToolTip.animation_utils.animate_slide_fade() - {e}")
                pass
            if on_complete:
                on_complete()
    step(0)


def get_slide_coords(tip_window: Toplevel, show: bool) -> Tuple[int, int]:
    """Calculate the starting and ending Y coordinates for slide animation."""
    geo = tip_window.geometry()
    parts = geo.split('+')
    base_x = int(parts[1])
    base_y = int(parts[2])
    start_y = base_y + SLIDE_ANIM_DISTANCE if show else base_y
    end_y = base_y if show else base_y + SLIDE_ANIM_DISTANCE
    return base_x, start_y, end_y
