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

| Parameter     | Type             | Default                         | Description                                                                                                                                      |
| ------------- | ---------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------|
| `widget`      | `tkinter.Widget` | —                               | The widget to attach the tooltip to                                                                                                              |
| `text`        | `str`            | `""`                            | Tooltip text                                                                                                                                     |
| `delay`       | `int`            | `10`                            | Delay before showing the tooltip (ms)                                                                                                            |
| `padx`        | `int`            | `1`                             | X-offset of the tooltip from the origin                                                                                                          |
| `pady`        | `int`            | `1`                             | Y-offset of the tooltip from the origin                                                                                                          |
| `ipadx`       | `int`            | `2`                             | Horizontal internal padding                                                                                                                      |
| `ipady`       | `int`            | `2`                             | Vertical internal padding                                                                                                                        |
| `state`       | `str`            | `"normal"`                      | Tooltip state, `"normal"` or `"disabled"`                                                                                                        |
| `bg`          | `str`            | `"#ffffee"`                   | Background color                                                                                                                                 |
| `fg`          | `str`            | `"black"`                       | Foreground (text) color                                                                                                                          |
| `font`        | `tuple`          | `("TkDefaultFont", 8, "normal")`| Font of the text                                                                                                                                 |
| `borderwidth` | `int`            | `1`                             | Border width                                                                                                                                     |
| `relief`      | `str`            | `"solid"`                       | Border style                                                                                                                                     |
| `justify`     | `str`            | `"center"`                      | Text justification                                                                                                                               |
| `wraplength`  | `int`            | `0`                             | Max line width for text wrapping (`0` disables wrapping)                                                                                         |
| `fade_in`     | `int`            | `125`                           | Fade-in time (ms)                                                                                                                                |
| `fade_out`    | `int`            | `50`                            | Fade-out time (ms)                                                                                                                               |
| `hide_delay`  | `int`            | `3000`                          | Force hiding the tooltip after this many milliseconds; (ms) Tooltip will not reappear until the mouse leaves the widget and hovers back over it. |
| `origin`      | `str`            | `"mouse"`                       | Origin point: `"mouse"` or `"widget"`                                                                                                            |
| `anchor`      | `str`            | `"nw"`                          | Relative position to the widget when origin is `"widget"` (e.g. `"n"`, `"ne"`, `"e"`, `"se"`, `"s"`, `"sw"`, `"w"`, `"nw"`, `"nesw"`)            |
| `follow_mouse`| `bool`           | `False`                         | When True, the tooltip follows the mouse while hovering over the widget. This ignores "origin" and "anchor" when active.                         |
