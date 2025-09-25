# TkToolTip

![Python 3.10+](https://img.shields.io/badge/git-Python_3.10%2B-green)

Bind tooltips to any widget that inherits from `tkinter.Widget`, including custom widgets.

## Features

- Lightweight binding API: attach a tooltip with `Tip.bind(widget, ...)`.
- Works with any `tkinter.Widget`, including custom widgets.
- Live reconfiguration via `tooltip.config(...)` for text, style, timing, and behavior.
- Positioning options: `origin` (`mouse` or `widget`), `widget_anchor`, and `tooltip_anchor` (nine positions).
- Optional `follow_mouse` mode to track the cursor while hovering.
- Appearance controls: background, foreground, `font`, `borderwidth`, `relief`, `justify`, padding.
- Wrapping via `wraplength` and adjustable padding (`padx`, `pady`, `ipadx`, `ipady`).
- Timing controls: `show_delay`, `hide_delay`, and auto-hide behavior.
- Animations: `fade`, `slide`, or `none` with adjustable `anim_in` and `anim_out`.
- Opacity control (0.0–1.0) for translucent tooltips.
- Respects screen bounds and avoids mouse overlap when positioned from the pointer.
- Multi-item tooltips: pass `list[str]` to render multiple lines with separators; supports per-item alignment flags.

## Installation

1. Install from the repository:

   ```bash
   pip install git+https://github.com/Nenotriple/TkToolTip.git@main
   ```

2. Import in your Python script:

   ```python
   from TkToolTip import TkToolTip as Tip
   ```

> [!WARNING]
> **Breaking change:** `v1.12+` introduces API changes.
> For legacy support use:
> `pip install git+https://github.com/Nenotriple/TkToolTip.git@v1.11`

## Usage

Tooltips must be bound to a widget. Two common patterns:

### Bind a Tooltip Directly

```python
Tip.bind(widget, text="example")
```

### Bind and Store a Tooltip for Later Configuration

```python
tooltip = Tip.bind(widget, text="example")
tooltip.config(text="Example!")
```

## Quick Start

```python
import tkinter as tk
from TkToolTip import TkToolTip as Tip

root = tk.Tk()

btn = tk.Button(root, text="Hover me")
btn.pack(padx=40, pady=30)

Tip.bind(btn, text="Hello!")

root.mainloop()
```

## Parameters

### Standard Options (inherited from `tkinter.Label`)

> These options control the appearance and layout of the tooltip label itself.

| Parameter     | Type    | Default                          | Values / Range                                         | Description                          |
| ------------- | ------- | -------------------------------- | ------------------------------------------------------ | ------------------------------------ |
| `bg`          | `str`   | `"white"`                        | Color name / hex                                       | Tooltip background color.            |
| `fg`          | `str`   | `"black"`                        | Color name / hex                                       | Text color.                          |
| `font`        | `tuple` | `("TkDefaultFont", 8, "normal")` | `(family, size, style)`                                | Font settings.                       |
| `borderwidth` | `int`   | `1`                              | ≥ 0                                                    | Border thickness.                    |
| `relief`      | `str`   | `"solid"`                        | `solid`, `raised`, `sunken`, `ridge`, `groove`, `flat` | Border style.                        |
| `justify`     | `str`   | `"center"`                       | `left`, `center`, `right`                              | Text alignment.                      |
| `wraplength`  | `int`   | `0`                              | ≥ 0 (`0` disables)                                     | Max width in pixels before wrapping. |
| `padx`        | `int`   | `1`                              | Any                                                    | Horizontal offset from origin.       |
| `pady`        | `int`   | `1`                              | Any                                                    | Vertical offset from origin.         |
| `ipadx`       | `int`   | `2`                              | Any                                                    | Inner horizontal padding.            |
| `ipady`       | `int`   | `2`                              | Any                                                    | Inner vertical padding.              |

### Widget-Specific Options (Unique to TkToolTip)

> Control behavior, positioning, animation, and dynamic features.

| Parameter        | Type                             | Default    | Values / Range                                                    | Description                             |
| ---------------- | -------------------------------- | ---------- | ----------------------------------------------------------------- | --------------------------------------- |
| `widget`         | `tkinter.Widget`                 | —          | Any widget                                                        | Widget the tooltip is attached to.      |
| `text`           | `str` · `list[str]` · `callable` | `""`       | String, list of strings, or function returning either             | Tooltip content.                        |
| `state`          | `str`                            | `"normal"` | `normal`, `disabled`                                              | Activates or disables the tooltip.      |
| `opacity`        | `float`                          | `1.0`      | `0.0`–`1.0`                                                       | Transparency (1.0 = opaque).            |
| `origin`         | `str`                            | `"mouse"`  | `mouse`, `widget`                                                 | Reference point for positioning.        |
| `widget_anchor`  | `str`                            | `"nw"`     | `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, `center`, `c`, `nesw` | Widget anchor when origin is `widget`.  |
| `tooltip_anchor` | `str`                            | `"nw"`     | `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, `center`, `c`, `nesw` | Tooltip anchor when origin is `widget`. |
| `follow_mouse`   | `bool`                           | `False`    | `True`, `False`                                                   | Track mouse movement while hovering.    |
| `show_delay`     | `int`                            | `100`      | ≥ 0 (ms)                                                          | Delay before showing.                   |
| `hide_delay`     | `int`                            | `5000`     | ≥ 0 (ms)                                                          | Auto-hide delay.                        |
| `animation`      | `str`                            | `"fade"`   | `fade`, `slide`, `none`                                           | Show/hide animation style.              |
| `anim_in`        | `int`                            | `75`       | ≥ 0 (ms)                                                          | Enter animation duration.               |
| `anim_out`       | `int`                            | `50`       | ≥ 0 (ms)                                                          | Exit animation duration.                |

## Default Overrides

Class-level defaults can be changed before creating tooltips. All subsequently created tooltips inherit the new values unless explicitly overridden.

```python
from TkToolTip import TkToolTip as Tip

# Set global defaults before creating tooltips
Tip.SHOW_DELAY = 500
Tip.HIDE_DELAY = 10000
Tip.ANIMATION = "slide"

# Tooltips created after this use these defaults unless overridden
```

## Animation Styles

Set `animation` to control appearance and disappearance:

- `fade` (default): cross-fades from 0 → target opacity.
- `slide`: slides upward a few pixels while fading in; reverses when hiding.
- `none`: instant show/hide.

Use `anim_in` and `anim_out` to tune durations (milliseconds).

## Multi-Item Tooltips and Per-Item Flags

Pass a list of strings to render multiple items. A thin separator is added between items. When a list is used, the container Frame holds the border/relief; individual Labels are borderless.

Per-item flags (only for list items) can be added at the start of an item:

- [l] or [left] → justify=left, anchor=w
- [c] or [center] → justify=center, anchor=center
- [r] or [right] → justify=right, anchor=e
- [a=anchor] → anchor override (n, ne, e, se, s, sw, w, nw, center)

Example:

```python
from TkToolTip import TkToolTip as Tip

Tip.bind(widget, text=[
    "First line",
    "[l] Left-aligned item",
    "[r] Right-aligned item",
    "[a=ne] NE-anchored item",
    "Last line"
])
```

> Note:
>
> - Flags can be combined, e.g., `[r][a=ne]`.
> - For single-string text, a single `Label` is used and the border/relief are applied directly to it.

## API Reference (Essentials)

- `Tip.bind(widget, **options)` / `Tip.create(widget, **options)` → `TkToolTip`
- `tip.config(**options)` / `tip.configure(**options)`
- `tip.hide()`
- `tip.unbind()`

## Project Structure

```text
TkToolTip/
  ├── TkToolTip.py           # Tooltip implementation
  ├── TkToolTip.pyi          # Type stubs for IDEs / type checking
  ├── position_utils.py      # Position calculations
  ├── animation_utils.py     # Animation logic
  └── __init__.py            # Package init
examples/
  └── demo.py                # Comprehensive GUI demo
tests/
  └── test_tktooltip.py      # Unit tests
setup.py                     # Packaging setup
README.md                    # Documentation
LICENSE                      # License
CHANGELOG.md                 # Changelog
```

## License

MIT License. See [LICENSE](LICENSE) for details.
