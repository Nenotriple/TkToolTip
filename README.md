# TkToolTip

Add customizable tooltips to any Tkinter widget.

![Python 3.10+](https://img.shields.io/badge/git-Python_3.10%2B-green) 🚩

## 💾 Install

1. Install in your environment:

   ```bash
   pip install git+https://github.com/Nenotriple/TkToolTip.git
   ```

2. Import in your Python script:

   ```python
   from TkToolTip import TkToolTip as Tip
   ```

## 📝 Usage

Tooltips can be created and configured in several ways but they must be associated with a widget.

### Create a tooltip directly

```python
Tip.create(widget, text="example")
```

### Create and store a tooltip for later configuration

```python
tooltip = Tip.create(widget, text="example")
tooltip.config(text="Example!")
```

## 💡 Parameters

| Parameter     | Type             | Default                           | Possible Values                                                                          | Description                                                                            |
| ------------- | ---------------- | ----------------------------------|------------------------------------------------------------------------------------------| -------------------------------------------------------------------------------------  |
| `widget`      | `tkinter.Widget` | —                                 | Any Tkinter widget                                                                       | The Tkinter widget to which the tooltip will be attached.                              |
| `text`        | `str`            | `""`                              | Any string                                                                               | The content displayed inside the tooltip.                                              |
| `state`       | `str`            | `"normal"`                        | `"normal"`, `"disabled"`                                                                 | Controls whether the tooltip is active or disabled.                                    |
| `bg`          | `str`            | `"#ffffee"`                     | Valid color name/hex                                                                     | Background color of the tooltip.                                                       |
| `fg`          | `str`            | `"black"`                         | Valid color name/hex                                                                     | Text color used in the tooltip.                                                        |
| `font`        | `tuple`          | `("TkDefaultFont", 8, "normal")`  | `(family, size, style)`                                                                  | Font settings for the tooltip text.                                                    |
| `borderwidth` | `int`            | `1`                               | Any integer ≥ 0                                                                          | Thickness of the tooltip border.                                                       |
| `relief`      | `str`            | `"solid"`                         | `"solid"`, `"raised"`, `"sunken"`, `"ridge"`, `"groove"`, `"flat"`                       | Style of the tooltip border.                                                           |
| `justify`     | `str`            | `"center"`                        | `"left"`, `"center"`, `"right"`                                                          | Alignment of the tooltip text.                                                         |
| `wraplength`  | `int`            | `0`                               | Any integer ≥ 0                                                                          | Maximum width for tooltip text before wrapping to a new line. (`0` disables wrapping)  |
| `padx`        | `int`            | `1`                               | Any integer                                                                              | Horizontal offset of the tooltip from its origin point.                                |
| `pady`        | `int`            | `1`                               | Any integer                                                                              | Vertical offset of the tooltip from its origin point.                                  |
| `ipadx`       | `int`            | `2`                               | Any integer                                                                              | Additional horizontal padding inside the tooltip.                                      |
| `ipady`       | `int`            | `2`                               | Any integer                                                                              | Additional vertical padding inside the tooltip.                                        |
| `origin`      | `str`            | `"mouse"`                         | `"mouse"`, `"widget"`                                                                    | Reference point for positioning the tooltip.                                           |
| `anchor`      | `str`            | `"nw"`                            | `"n"`, `"ne"`, `"e"`, `"se"`, `"s"`, `"sw"`, `"w"`, `"nw"`, `"center"`, `"c"`, `"nesw"`  | Position of the tooltip relative to the widget when using widget origin.               |
| `follow_mouse`| `bool`           | `False`                           | `True`, `False`                                                                          | If enabled, the tooltip moves with the mouse while hovering over the widget.           |
| `show_delay`  | `int`            | `10`                              | Any integer ≥ 0                                                                          | Time in milliseconds to wait before showing the tooltip after hovering.                |
| `hide_delay`  | `int`            | `3000`                            | Any integer ≥ 0                                                                          | Time in milliseconds before the tooltip automatically hides.                           |
| `fade_in`     | `int`            | `125`                             | Any integer ≥ 0                                                                          | Duration of the fade-in animation when the tooltip appears.                            |
| `fade_out`    | `int`            | `50`                              | Any integer ≥ 0                                                                          | Duration of the fade-out animation when the tooltip disappears.                        |
