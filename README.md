# TkToolTips


Add customizable tooltips to any Tkinter widget.


# Install


1) Install in your enviroment:

  - `pip install git+https://github.com/Nenotriple/TkToolTips.git`

2) Import within your python script:

  - `from TkToolTips.TkToolTips import TkToolTips as ToolTip`


<br>


# Usage:

A) Directly create a tooltip:

1) ```TkToolTip.create(widget, text="example")```

B) Create and store a tooltip for later configuration:

1) ```tooltip = TkToolTip.create(widget, text="example")```

2) ```tooltip.config(text="Example!")```


<br>


# Parameters

`widget` : `tkinter.Widget`
- The widget to attach the tooltip to

`text` : `str, optional`
- Tooltip text (default is an empty string)

`delay` : `int, optional`
- Delay before showing the tooltip in milliseconds (default is 0)

`padx` : `int, optional`
- X-offset of the tooltip from the origin (default is 0)

`pady` : `int, optional`
- Y-offset of the tooltip from the origin (default is 0)

`ipadx` : `int, optional`
- Horizontal internal padding (default is 0)

`ipady` : `int, optional`
- Vertical internal padding (default is 0)

`state` : `str, optional`
- Tooltip state, "normal" or "disabled" (default is None)

`bg` : str, `optional`
- Background color (default is "#ffffee")

`fg` : str, `optional`
- Foreground (text) color (default is "black")

`font` : `tuple, optional`
- Font of the text (default is ("TkDefaultFont", 8, "normal"))

`borderwidth` : `int, optional`
- Border width (default is 1)

`relief` : `str, optional`
- Border style (default is "solid")

`justify` : `str, optional`
- Text justification (default is "center")

`wraplength` : `int, optional`
- Maximum line width for text wrapping (default is 0, which disables wrapping)

`fade_in` : `int, optional`
- Fade-in time in milliseconds (default is 125)

`fade_out` : `int, optional`
- Fade-out time in milliseconds (default is 50)

`origin` : `str, optional`
- Origin point of the tooltip, "mouse" or "widget" (default is "mouse")
