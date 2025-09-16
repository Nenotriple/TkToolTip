# Typing
from __future__ import annotations
from typing import Optional, Tuple, Literal, Callable, Union

# Standard - GUI
from tkinter import Widget, Toplevel, Event


class TkToolTip:
    """
    Attach a Tooltip to any tkinter widget.

    Parameters
    ----------
    widget : tkinter.Widget, optional
        The widget to attach the tooltip to

    text : str or callable, optional
        Tooltip text or a function returning text ("")

    state : str, optional
        Tooltip state, "normal" or "disabled" ("normal")

    bg : str, optional
        Background color ("#ffffee")

    fg : str, optional
        Foreground (text) color ("black")

    font : tuple, optional
        Font of the text (("TkDefaultFont", 8, "normal"))

    borderwidth : int, optional
        Border width (1)

    opacity : float, optional
        Opacity of the tooltip (1.0)

    relief : str, optional
        Border style ("solid")

    justify : str, optional
        Text justification ("center")

    wraplength : int, optional
        Maximum line width for text wrapping (0 disables wrapping)

    padx : int, optional
        X-offset of the tooltip from the origin (1)

    pady : int, optional
        Y-offset of the tooltip from the origin (1)

    ipadx : int, optional
        Horizontal internal padding (2)

    ipady : int, optional
        Vertical internal padding (2)

    origin : str, optional
        Origin point of the tooltip, "mouse" or "widget" ("mouse")

    widget_anchor : str, optional
        Specifies the point on the widget used for alignment when origin is "widget" ("nw").
        Valid values are combinations of n, e, s, w. Special values "center" or "c"
        center the tooltip. "nesw" also treated as center.

    tooltip_anchor : str, optional
        Specifies the point on the tooltip used for alignment when origin is "widget" ("nw").
        Valid values are combinations of n, e, s, w. Special values "center" or "c"
        center the tooltip. "nesw" also treated as center.

    follow_mouse : bool, optional
        When True, tooltip follows the mouse while hovering (overrides origin/widget_anchor).

    show_delay : int, optional
        Delay before showing in ms (100)

    hide_delay : int, optional
        Auto-hide after this many ms (5000). Suppresses re-show until leave/enter.

    animation : str, optional
        Animation style: "fade", "slide", or "none" ("fade")

    anim_in : int, optional
        Animation duration entering in ms (75)

    anim_out : int, optional
        Animation duration exiting in ms (50)

    Methods
    -------
    bind(widget, **kwargs)
        Create and return a tooltip for widget.
    config(**kwargs)
        Update tooltip configuration.
    unbind()
        Remove all bindings.
    hide()
        Hide the tooltip immediately.
    """


    # Class-level defaults
    TEXT: str
    STATE: Literal["normal", "disabled"]
    BG: str
    FG: str
    FONT: Optional[Tuple[str, int, str]]
    BORDERWIDTH: int
    OPACITY: float
    RELIEF: str
    JUSTIFY: str
    WRAPLENGTH: int
    PADX: int
    PADY: int
    IPADX: int
    IPADY: int
    ORIGIN: str
    WIDGET_ANCHOR: str
    TOOLTIP_ANCHOR: str
    FOLLOW_MOUSE: bool
    SHOW_DELAY: int
    HIDE_DELAY: int
    ANIMATION: str
    ANIM_IN: int
    ANIM_OUT: int
    PARAMS: list[str]

    # Magic numbers
    SLIDE_DISTANCE = int


    # Instance attributes (after initialization)
    widget: Optional[Widget]
    text: Union[str, Callable[[], str]]
    state: Literal["normal", "disabled"]
    bg: str
    fg: str
    font: Optional[Tuple[str, int, str]]
    borderwidth: int
    opacity: float
    relief: str
    justify: str
    wraplength: int
    padx: int
    pady: int
    ipadx: int
    ipady: int
    origin: str
    widget_anchor: str
    tooltip_anchor: str
    follow_mouse: bool
    show_delay: int
    hide_delay: int
    animation: str
    anim_in: int
    anim_out: int
    tip_window: Optional[Toplevel]
    show_after_id: Optional[int]
    hide_id: Optional[int]


    def __init__(
        self,
        widget: Optional[Widget] = None,
        *,
        text: Union[str, Callable[[], str]] = "",
        state: Literal["normal", "disabled"] = TkToolTip.STATE,
        bg: str = TkToolTip.BG,
        fg: str = TkToolTip.FG,
        font: Optional[Tuple[str, int, str]] = TkToolTip.FONT,
        borderwidth: int = TkToolTip.BORDERWIDTH,
        opacity: float = TkToolTip.OPACITY,
        relief: str = TkToolTip.RELIEF,
        justify: str = TkToolTip.JUSTIFY,
        wraplength: int = TkToolTip.WRAPLENGTH,
        padx: int = TkToolTip.PADX,
        pady: int = TkToolTip.PADY,
        ipadx: int = TkToolTip.IPADX,
        ipady: int = TkToolTip.IPADY,
        origin: str = TkToolTip.ORIGIN,
        widget_anchor: str = TkToolTip.WIDGET_ANCHOR,
        tooltip_anchor: str = TkToolTip.TOOLTIP_ANCHOR,
        follow_mouse: bool = TkToolTip.FOLLOW_MOUSE,
        show_delay: int = TkToolTip.SHOW_DELAY,
        hide_delay: int = TkToolTip.HIDE_DELAY,
        animation: str = TkToolTip.ANIMATION,
        anim_in: int = TkToolTip.ANIM_IN,
        anim_out: int = TkToolTip.ANIM_OUT
    ) -> None: ...


    @classmethod
    def bind(
        cls,
        widget: Widget,
        *,
        text: Union[str, Callable[[], str]] = "",
        state: Literal["normal", "disabled"] = TkToolTip.STATE,
        bg: str = TkToolTip.BG,
        fg: str = TkToolTip.FG,
        font: Optional[Tuple[str, int, str]] = TkToolTip.FONT,
        borderwidth: int = TkToolTip.BORDERWIDTH,
        opacity: float = TkToolTip.OPACITY,
        relief: str = TkToolTip.RELIEF,
        justify: str = TkToolTip.JUSTIFY,
        wraplength: int = TkToolTip.WRAPLENGTH,
        padx: int = TkToolTip.PADX,
        pady: int = TkToolTip.PADY,
        ipadx: int = TkToolTip.IPADX,
        ipady: int = TkToolTip.IPADY,
        origin: str = TkToolTip.ORIGIN,
        widget_anchor: str = TkToolTip.WIDGET_ANCHOR,
        tooltip_anchor: str = TkToolTip.TOOLTIP_ANCHOR,
        follow_mouse: bool = TkToolTip.FOLLOW_MOUSE,
        show_delay: int = TkToolTip.SHOW_DELAY,
        hide_delay: int = TkToolTip.HIDE_DELAY,
        animation: str = TkToolTip.ANIMATION,
        anim_in: int = TkToolTip.ANIM_IN,
        anim_out: int = TkToolTip.ANIM_OUT
    ) -> TkToolTip: ...


    def config(
        self,
        *,
        text: Optional[Union[str, Callable[[], str]]] = None,
        state: Optional[Literal["normal", "disabled"]] = None,
        bg: Optional[str] = None,
        fg: Optional[str] = None,
        font: Optional[Tuple[str, int, str]] = None,
        borderwidth: Optional[int] = None,
        opacity: Optional[float] = None,
        relief: Optional[str] = None,
        justify: Optional[str] = None,
        wraplength: Optional[int] = None,
        padx: Optional[int] = None,
        pady: Optional[int] = None,
        ipadx: Optional[int] = None,
        ipady: Optional[int] = None,
        origin: Optional[str] = None,
        widget_anchor: Optional[str] = None,
        tooltip_anchor: Optional[str] = None,
        follow_mouse: Optional[bool] = None,
        show_delay: Optional[int] = None,
        hide_delay: Optional[int] = None,
        animation: Optional[str] = None,
        anim_in: Optional[int] = None,
        anim_out: Optional[int] = None
    ) -> None: ...


    def unbind(self) -> None: ...


    def hide(self, event: Event | None = None) -> None: ...


    def _get_text(self) -> str: ...
