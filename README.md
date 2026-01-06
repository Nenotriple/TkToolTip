
> ⚠️ **Important! Project Has Moved**
>
> This project has been incorperated into the [NenoTk library](https://github.com/Nenotriple/NenoTk).
>
> Please use and contribute to that repository instead — this repo may be out of date and will not receive updates or support.

# TkToolTip

Bind tooltips to any widget that inherits from `tkinter.Widget`, including custom widgets.

![Python 3.10+](https://img.shields.io/badge/git-Python_3.10%2B-green)

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
> `v1.12+` introduces breaking changes to the API.
>
> For legacy support use `git+https://github.com/Nenotriple/TkToolTip.git@v1.11`

## Usage

Tooltips must be associated with a widget. There are two common patterns.

### Bind a tooltip directly

```python
Tip.bind(widget, text="example")
```

### Bind and store a tooltip for later configuration

```python
tooltip = Tip.bind(widget, text="example")
tooltip.config(text="Example!")
```

## Features

- Lightweight binding API: attach a tooltip with `Tip.bind(widget, ...)`.
- Works with any `tkinter.Widget`, including custom widgets.
- Live reconfiguration via `tooltip.config(...)` for text, style, timing, and behavior.
- Positioning options: `origin` (`mouse` or `widget`) and `anchor` (nine positions).
- Optional `follow_mouse` mode to track the cursor while hovering.
- Appearance controls: background, foreground, `font`, `borderwidth`, `relief`, `justify`, padding.
- Wrapping support via `wraplength` and adjustable padding (`padx`, `pady`, `ipadx`, `ipady`).
- Timing controls: `show_delay`, `hide_delay`, and auto-hide behavior.
- Animations: `fade`, `slide`, or `none` with adjustable `anim_in` and `anim_out`.
- Opacity control (0.0–1.0) for translucent tooltips.
- Respects screen bounds and avoids mouse overlap when positioned from the pointer.

## Parameters

| Parameter      | Type             | Default                          | Possible Values                                                                         | Description                                                                           |
| -------------- | ---------------- | -------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `widget`       | `tkinter.Widget` | —                                | Any Tkinter widget                                                                      | The widget to which the tooltip will be attached.                                     |
| `text`         | `str`            | `""`                             | Any string                                                                              | The content displayed inside the tooltip.                                             |
| `state`        | `str`            | `"normal"`                       | `"normal"`, `"disabled"`                                                                | Controls whether the tooltip is active.                                               |
| `bg`           | `str`            | `"#ffffee"`                    | Valid color name / hex                                                                  | Tooltip background color.                                                             |
| `fg`           | `str`            | `"black"`                        | Valid color name / hex                                                                  | Text color used in the tooltip.                                                       |
| `font`         | `tuple`          | `("TkDefaultFont", 8, "normal")` | `(family, size, style)`                                                                 | Font settings for the tooltip text.                                                   |
| `borderwidth`  | `int`            | `1`                              | Any integer ≥ 0                                                                         | Thickness of the tooltip border.                                                      |
| `opacity`      | `float`          | `1.0`                            | `0.0` to `1.0`                                                                          | Tooltip transparency (0.0 = transparent, 1.0 = opaque).                               |
| `relief`       | `str`            | `"solid"`                        | `"solid"`, `"raised"`, `"sunken"`, `"ridge"`, `"groove"`, `"flat"`                      | Style of the tooltip border.                                                          |
| `justify`      | `str`            | `"center"`                       | `"left"`, `"center"`, `"right"`                                                         | Alignment of the tooltip text.                                                        |
| `wraplength`   | `int`            | `0`                              | Any integer ≥ 0                                                                         | Max width (px) before wrapping. `0` disables wrapping.                                |
| `padx`         | `int`            | `1`                              | Any integer                                                                             | Horizontal offset of the tooltip from its origin.                                     |
| `pady`         | `int`            | `1`                              | Any integer                                                                             | Vertical offset of the tooltip from its origin.                                       |
| `ipadx`        | `int`            | `2`                              | Any integer                                                                             | Additional horizontal padding inside the tooltip.                                     |
| `ipady`        | `int`            | `2`                              | Any integer                                                                             | Additional vertical padding inside the tooltip.                                       |
| `origin`       | `str`            | `"mouse"`                        | `"mouse"`, `"widget"`                                                                   | Reference point for positioning the tooltip.                                          |
| `anchor`       | `str`            | `"nw"`                           | `"n"`, `"ne"`, `"e"`, `"se"`, `"s"`, `"sw"`, `"w"`, `"nw"`, `"center"`, `"c"`, `"nesw"` | Position relative to widget when using widget origin.                                 |
| `follow_mouse` | `bool`           | `False`                          | `True`, `False`                                                                         | If `True`, the tooltip follows the mouse while hovering.                              |
| `show_delay`   | `int`            | `100`                            | Any integer ≥ 0                                                                         | Milliseconds to wait before showing after hover.                                      |
| `hide_delay`   | `int`            | `5000`                           | Any integer ≥ 0                                                                         | Milliseconds before the tooltip automatically hides.                                  |
| `animation`    | `str`            | `"fade"`                         | `"fade"`, `"slide"`, `"none"`                                                           | Animation style for showing / hiding.                                                 |
| `anim_in`      | `int`            | `75`                             | Any integer ≥ 0                                                                         | Duration (ms) of the show (enter) animation.                                          |
| `anim_out`     | `int`            | `50`                             | Any integer ≥ 0                                                                         | Duration (ms) of the hide (exit) animation.                                           |

## Animation styles

Set `animation` to control how the tooltip appears and disappears:

- `fade` (default): cross-fade opacity from 0 → `opacity`.
- `slide`: slides upward a few pixels while fading in; reverses when hiding.
- `none`: instantly shows and hides with no transitions.

Use `anim_in` and `anim_out` to tune durations (milliseconds).

## Project structure

```text
TkToolTip/
  TkToolTip.py         # Tooltip implementation
  position_utils.py    # Position calculations
  animation_utils.py   # Animation logic
  TkToolTip.pyi        # Type stubs for IDEs / type checking
examples/
  demo.py              # Comprehensive GUI demo
```

## License

MIT License. See [LICENSE](LICENSE) for details.
