# TkToolTip


Add customizable tooltips to any Tkinter widget.


<br>


# 💾 Install
![Static Badge](https://img.shields.io/badge/git-Python_3.10%2B-green)🚩

1) Install in your enviroment:

  - `pip install git+https://github.com/Nenotriple/TkToolTip.git`

2) Import within your python script:

  - `from TkToolTip.TkToolTip import TkToolTip as Tip`


<br>


# 📝 Usage:

A) Directly create a tooltip:

1) ```Tip.create(widget, text="example")```

B) Create and store a tooltip for later configuration:

1) ```tooltip = Tip.create(widget, text="example")```

2) ```tooltip.config(text="Example!")```


<br>


# 💡 Parameters

| Parameter     | Type                | Default                      | Description                                                                 |
|---------------|---------------------|------------------------------|-----------------------------------------------------------------------------|
| `widget`      | `tkinter.Widget`    | —                            | The widget to attach the tooltip to                                         |
| `text`        | `str`               | `""`                         | Tooltip text                                                                |
| `delay`       | `int`               | `0`                          | Delay before showing the tooltip (ms)                                       |
| `padx`        | `int`               | `0`                          | X-offset of the tooltip from the origin                                     |
| `pady`        | `int`               | `0`                          | Y-offset of the tooltip from the origin                                     |
| `ipadx`       | `int`               | `0`                          | Horizontal internal padding                                                 |
| `ipady`       | `int`               | `0`                          | Vertical internal padding                                                   |
| `state`       | `str`               | `None`                       | Tooltip state, `"normal"` or `"disabled"`                                   |
| `bg`          | `str`               | `"#ffffee"`                | Background color                                                            |
| `fg`          | `str`               | `"black"`                    | Foreground (text) color                                                     |
| `font`        | `tuple`             | `("TkDefaultFont", 8, "normal")` | Font of the text                                                        |
| `borderwidth` | `int`               | `1`                          | Border width                                                                |
| `relief`      | `str`               | `"solid"`                    | Border style                                                                |
| `justify`     | `str`               | `"center"`                   | Text justification                                                          |
| `wraplength`  | `int`               | `0`                          | Max line width for text wrapping (`0` disables wrapping)                    |
| `fade_in`     | `int`               | `125`                        | Fade-in time (ms)                                                           |
| `fade_out`    | `int`               | `50`                         | Fade-out time (ms)                                                          |
| `origin`      | `str`               | `"mouse"`                    | Origin point: `"mouse"` or `"widget"`                                       |
