import os
import sys
import unittest
import tkinter as tk

# Ensure local package is used when running as: python tests\test_tktooltip.py
_TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_TESTS_DIR, '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from TkToolTip import TkToolTip


class TkToolTipTestCase(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.btn = tk.Button(self.root, text="Test")
        self.btn.pack()


    def tearDown(self):
        self.btn.destroy()
        self.root.destroy()


    def test_bind_and_configure(self):
        tip = TkToolTip.bind(self.btn, text="Hello", bg="yellow")
        self.assertIsInstance(tip, TkToolTip)
        self.assertEqual(tip.text, "Hello")
        self.assertEqual(tip.bg, "yellow")
        tip.config(text="World", fg="blue")
        self.assertEqual(tip.text, "World")
        self.assertEqual(tip.fg, "blue")
        tip.configure(bg="green")
        self.assertEqual(tip.bg, "green")


    def test_create_alias(self):
        tip = TkToolTip.create(self.btn, text="Alias")
        self.assertEqual(tip.text, "Alias")


    def test_unbind(self):
        tip = TkToolTip.bind(self.btn, text="unbind")
        tip.unbind()
        # Should not raise error when unbinding again
        tip.unbind()


    def test_hide(self):
        tip = TkToolTip.bind(self.btn, text="hide")
        tip.hide()
        self.assertIsNone(tip.tip_window)


    def test_disabled_state(self):
        tip = TkToolTip.bind(self.btn, text="Should not show", state="disabled")
        self.assertEqual(tip.state, "disabled")
        # Should not show tooltip when disabled
        tip._show_tip(event=type("Event", (), {"x_root": 0, "y_root": 0})())
        self.assertIsNone(tip.tip_window)


    def test_opacity_edge_cases(self):
        tip = TkToolTip.bind(self.btn, text="opacity", opacity=0.0)
        self.assertEqual(tip.opacity, 0.0)
        tip.config(opacity=1.0)
        self.assertEqual(tip.opacity, 1.0)
        with self.assertRaises(AssertionError):
            tip.config(opacity=-0.1)
        with self.assertRaises(AssertionError):
            tip.config(opacity=1.1)


    def test_callback_text(self):
        tip = TkToolTip.bind(self.btn, text=lambda: "callback")
        self.assertTrue(callable(tip.text))
        self.assertEqual(tip._get_text(), "callback")


    def test_callback_text_exception(self):
        tip = TkToolTip.bind(self.btn, text=lambda: 1 / 0)
        # Should handle exception and return empty string
        self.assertEqual(tip._get_text(), "")


    def test_invalid_param(self):
        with self.assertRaises(TypeError):
            TkToolTip.bind(self.btn, not_a_param="fail")


    def test_all_params(self):
        tip = TkToolTip.bind(
            self.btn,
            text="AllParams",
            state="normal",
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            borderwidth=2,
            opacity=0.5,
            relief="groove",
            justify="left",
            wraplength=100,
            padx=5,
            pady=5,
            ipadx=4,
            ipady=4,
            origin="widget",
            widget_anchor="se",
            tooltip_anchor="nw",
            follow_mouse=True,
            show_delay=10,
            hide_delay=100,
            animation="slide",
            anim_in=10,
            anim_out=10
        )
        self.assertEqual(tip.text, "AllParams")
        self.assertEqual(tip.state, "normal")
        self.assertEqual(tip.bg, "red")
        self.assertEqual(tip.fg, "white")
        self.assertEqual(tip.font, ("Arial", 10, "bold"))
        self.assertEqual(tip.borderwidth, 2)
        self.assertEqual(tip.opacity, 0.5)
        self.assertEqual(tip.relief, "groove")
        self.assertEqual(tip.justify, "left")
        self.assertEqual(tip.wraplength, 100)
        self.assertEqual(tip.padx, 5)
        self.assertEqual(tip.pady, 5)
        self.assertEqual(tip.ipadx, 4)
        self.assertEqual(tip.ipady, 4)
        self.assertEqual(tip.origin, "widget")
        self.assertEqual(tip.widget_anchor, "se")
        self.assertEqual(tip.tooltip_anchor, "nw")
        self.assertTrue(tip.follow_mouse)
        self.assertEqual(tip.show_delay, 10)
        self.assertEqual(tip.hide_delay, 100)
        self.assertEqual(tip.animation, "slide")
        self.assertEqual(tip.anim_in, 10)
        self.assertEqual(tip.anim_out, 10)


    def test_configure_alias(self):
        tip = TkToolTip.bind(self.btn, text="foo")
        tip.configure(text="bar")
        self.assertEqual(tip.text, "bar")


    def test_follow_mouse_and_origin(self):
        tip = TkToolTip.bind(self.btn, text="follow", follow_mouse=True, origin="mouse")
        # Simulate event
        event = type("Event", (), {"x_root": 50, "y_root": 60})()
        pos = tip._calculate_follow_position(event)
        self.assertEqual(pos, (50 + tip.padx, 60 + tip.pady))
        # Should move tip if tip_window exists
        tip.tip_window = None  # No window yet
        tip._schedule_show_tip(event)
        # Should not error


    def test_widget_anchor_and_tooltip_anchor(self):
        tip = TkToolTip.bind(self.btn, text="anchor", origin="widget", widget_anchor="center", tooltip_anchor="se")
        # Simulate event
        event = type("Event", (), {"x_root": 0, "y_root": 0})()
        pos = tip._current_follow_position()
        self.assertIsInstance(pos, tuple)


    def test_hide_delay_and_suppression(self):
        tip = TkToolTip.bind(self.btn, text="hide_delay", hide_delay=10)
        tip._schedule_auto_hide()
        # Simulate auto-hide
        tip._auto_hide()
        self.assertTrue(tip._suppress_until_leave)
        tip._on_leave()
        self.assertFalse(tip._suppress_until_leave)


    def test_update_tip_label_and_error_handling(self):
        tip = TkToolTip.bind(self.btn, text="label")
        class DummyLabel:
            def config(self, **kwargs):
                raise Exception("fail")
        label = DummyLabel()
        tip._update_tip_label(label)  # Should print error but not raise


    def test_show_tip_with_empty_text(self):
        tip = TkToolTip.bind(self.btn, text="")
        event = type("Event", (), {"x_root": 0, "y_root": 0})()
        tip._show_tip(event)
        self.assertIsNone(tip.tip_window)


    def test_show_tip_with_none_text(self):
        tip = TkToolTip.bind(self.btn, text=None)
        event = type("Event", (), {"x_root": 0, "y_root": 0})()
        tip._show_tip(event)
        self.assertIsNone(tip.tip_window)


    def test_animation_parameter(self):
        tip = TkToolTip.bind(self.btn, text="anim", animation="fade")
        self.assertEqual(tip.animation, "fade")
        tip.config(animation="slide")
        self.assertEqual(tip.animation, "slide")
        tip.config(animation="none")
        self.assertEqual(tip.animation, "none")


    def test_borderwidth_and_relief(self):
        tip = TkToolTip.bind(self.btn, text="border", borderwidth=3, relief="ridge")
        self.assertEqual(tip.borderwidth, 3)
        self.assertEqual(tip.relief, "ridge")


    def test_wraplength_and_justify(self):
        tip = TkToolTip.bind(self.btn, text="wrap", wraplength=200, justify="right")
        self.assertEqual(tip.wraplength, 200)
        self.assertEqual(tip.justify, "right")


    def test_padding_params(self):
        tip = TkToolTip.bind(self.btn, text="pad", padx=10, pady=15, ipadx=5, ipady=7)
        self.assertEqual(tip.padx, 10)
        self.assertEqual(tip.pady, 15)
        self.assertEqual(tip.ipadx, 5)
        self.assertEqual(tip.ipady, 7)


    def test_font_param(self):
        tip = TkToolTip.bind(self.btn, text="font", font=("Courier", 12, "italic"))
        self.assertEqual(tip.font, ("Courier", 12, "italic"))


    def test_state_param_invalid(self):
        with self.assertRaises(AssertionError):
            TkToolTip.bind(self.btn, text="badstate", state="bad")


    def test_origin_param(self):
        tip = TkToolTip.bind(self.btn, text="origin", origin="mouse")
        self.assertEqual(tip.origin, "mouse")
        tip.config(origin="widget")
        self.assertEqual(tip.origin, "widget")


    def test_tooltip_anchor_param(self):
        tip = TkToolTip.bind(self.btn, text="anchor", tooltip_anchor="center")
        self.assertEqual(tip.tooltip_anchor, "center")


    def test_follow_mouse_param(self):
        tip = TkToolTip.bind(self.btn, text="follow", follow_mouse=True)
        self.assertTrue(tip.follow_mouse)


    def test_show_hide_animation(self):
        tip = TkToolTip.bind(self.btn, text="anim", animation="fade")
        # Should not raise error
        tip._animate(show=True)
        tip._animate(show=False)


    def test_config_no_kwargs(self):
        tip = TkToolTip.bind(self.btn, text="foo")
        tip.config()
        self.assertEqual(tip.text, "foo")


    def test_config_invalid_type(self):
        tip = TkToolTip.bind(self.btn, text="foo")
        with self.assertRaises(TypeError):
            tip.config(not_a_param="fail")


if __name__ == "__main__":
    unittest.main()
