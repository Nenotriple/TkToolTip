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

## Install

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

### Bind a tooltip directly

```python
Tip.bind(widget, text="example")
```

### Bind and store a tooltip for later configuration

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

### Standard options (inherited from `tkinter.Label`)

> These options control the appearance and layout of the tooltip label itself.

| Parameter     | Type    | Default                        | Values / Range                                                | Description                                    |
| ------------- | ------- | ------------------------------ | ------------------------------------------------------------- | ---------------------------------------------- |
| `bg`          | `str`   | `"#ffffee"`                    | Color name / hex                                              | Tooltip background color.                      |
| `fg`          | `str`   | `"black"`                      | Color name / hex                                              | Text color.                                    |
| `font`        | `tuple` | `("TkDefaultFont", 8, "normal")` | `(family, size, style)`                                      | Font settings.                                 |
| `borderwidth` | `int`   | `1`                            | ≥ 0                                                           | Border thickness.                              |
| `relief`      | `str`   | `"solid"`                      | `solid`, `raised`, `sunken`, `ridge`, `groove`, `flat`        | Border style.                                  |
| `justify`     | `str`   | `"center"`                     | `left`, `center`, `right`                                     | Text alignment.                                |
| `wraplength`  | `int`   | `0`                            | ≥ 0 (`0` disables)                                            | Max width in pixels before wrapping.           |
| `padx`        | `int`   | `1`                            | Any                                                           | Horizontal offset from origin.                 |
| `pady`        | `int`   | `1`                            | Any                                                           | Vertical offset from origin.                   |
| `ipadx`       | `int`   | `2`                            | Any                                                           | Inner horizontal padding.                      |
| `ipady`       | `int`   | `2`                            | Any                                                           | Inner vertical padding.                        |

### Widget-specific options (unique to TkToolTip)

> Control behavior, positioning, animation, and dynamic features.

| Parameter        | Type                | Default   | Values / Range                                                             | Description                                                      |
| ---------------- | ------------------- | --------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `widget`         | `tkinter.Widget`    | —         | Any widget                                                                  | Widget the tooltip is attached to.                               |
| `text`           | `str` or `callable` | `""`      | String or function returning string                                        | Content displayed in the tooltip.                                |
| `state`          | `str`               | `"normal"` | `normal`, `disabled`                                                       | Activates or disables the tooltip.                               |
| `opacity`        | `float`             | `1.0`     | `0.0`–`1.0`                                                                | Transparency (1.0 = opaque).                                      |
| `origin`         | `str`               | `"mouse"` | `mouse`, `widget`                                                          | Reference point for positioning.                                 |
| `widget_anchor`  | `str`               | `"nw"`    | `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, `center`, `c`, `nesw`          | Widget anchor when origin is `widget`.                           |
| `tooltip_anchor` | `str`               | `"nw"`    | `n`, `ne`, `e`, `se`, `s`, `sw`, `w`, `nw`, `center`, `c`, `nesw`          | Tooltip anchor when origin is `widget`.                          |
| `follow_mouse`   | `bool`              | `False`   | `True`, `False`                                                            | Track mouse movement while hovering.                             |
| `show_delay`     | `int`               | `100`     | ≥ 0 (ms)                                                                   | Delay before showing.                                            |
| `hide_delay`     | `int`               | `5000`    | ≥ 0 (ms)                                                                   | Auto-hide delay.                                                 |
| `animation`      | `str`               | `"fade"`  | `fade`, `slide`, `none`                                                    | Show/hide animation style.                                       |
| `anim_in`        | `int`               | `75`      | ≥ 0 (ms)                                                                   | Enter animation duration.                                        |
| `anim_out`       | `int`               | `50`      | ≥ 0 (ms)                                                                   | Exit animation duration.                                         |

## Animation Styles

Set `animation` to control appearance and disappearance:

- `fade` (default): cross-fades from 0 → target opacity.
- `slide`: slides upward a few pixels while fading in; reverses when hiding.
- `none`: instant show/hide.

Use `anim_in` and `anim_out` to tune durations (milliseconds).

## Default Override

Class-level defaults can be changed before creating tooltips. All subsequently created tooltips inherit the new values unless explicitly overridden.

```python
from TkToolTip import TkToolTip as Tip

# Set global defaults before creating tooltips
Tip.SHOW_DELAY = 500
Tip.HIDE_DELAY = 10000
Tip.ANIMATION = "slide"

# Tooltips created after this use these defaults unless overridden
```

## API Reference (Essentials)

- `Tip.bind(widget, **options)` / `Tip.create(widget, **options)` → `TkToolTip`
- `tip.config(**options)` / `tip.configure(**options)`
- `tip.hide()`
- `tip.unbind()`

## Project Structure

```text
TkToolTip
  │
  ├── TkToolTip.py         # Tooltip implementation
  ├── position_utils.py    # Position calculations
  ├── animation_utils.py   # Animation logic
  ├── TkToolTip.pyi        # Type stubs for IDEs / type checking
  │
examples
  │
  └── demo.py              # Comprehensive GUI demo
```

## License

MIT License. See [LICENSE](LICENSE) for details.
