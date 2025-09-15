"""
TkToolTip Demonstration
=======================

Showcases all features of the TkToolTip module in an interactive GUI.
"""


#region Imports


import os
import sys
import tkinter as tk
from tkinter import ttk, colorchooser, font as tkfont


#endregion
#region Path Setup


# Ensure local package is used when running as: python examples/demo.py
_EXAMPLES_DIR = os.path.abspath(os.path.dirname(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_EXAMPLES_DIR, '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


from TkToolTip import TkToolTip as Tip


#endregion
#region Main


# Main application setup
def main():
    root = tk.Tk()
    root.title('TkToolTip Demo')
    root.geometry('1000x900')
    setup_ui(root)
    root.mainloop()


#endregion
#region GUI Setup & Sections


def setup_ui(root):
    # This function creates a scrollable area for the demo, so all TkToolTip features can be shown in one window
    outer = ttk.Frame(root)
    outer.pack(fill='both', expand=True, padx=8, pady=8)
    canvas = tk.Canvas(outer, highlightthickness=0)
    vscroll = ttk.Scrollbar(outer, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=vscroll.set)
    vscroll.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    container = ttk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=container, anchor='nw')
    setup_scroll_bindings(canvas, container, window_id)
    # Build all demo sections that teach TkToolTip usage and configuration
    build_demo_sections(container)


def setup_scroll_bindings(canvas, container, window_id):
    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox('all'))
        canvas.itemconfig(window_id, width=canvas.winfo_width())

    def on_canvas_configure(event):
        canvas.itemconfig(window_id, width=event.width)

    def on_mousewheel(event):
        delta = int(-1 * (event.delta / 120))
        canvas.yview_scroll(delta, 'units')

    container.bind('<Configure>', configure_scrollregion)
    canvas.bind('<Configure>', on_canvas_configure)
    canvas.bind_all('<MouseWheel>', on_mousewheel)


def build_demo_sections(container):
    # This function organizes the main sections for TkToolTip:
    # 1. Anchor and follow_mouse section: shows anchor and follow_mouse features
    # 2. Dynamic section: lets users interactively configure tooltips
    build_anchor_follow_section(container)
    build_dynamic_section(container)
    ttk.Frame(container, height=20).pack()


# --- Two-column layout for anchor and follow sections ---
def build_anchor_follow_section(parent):
    # This section visually compares anchor-based and follow_mouse tooltips side by side
    two_col_frame = ttk.Frame(parent)
    two_col_frame.pack(fill='x', padx=10, pady=5)
    two_col_frame.columnconfigure(0, weight=1)
    two_col_frame.columnconfigure(1, weight=1)
    left_frame = ttk.Frame(two_col_frame)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
    right_frame = ttk.Frame(two_col_frame)
    right_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
    build_anchor_section(left_frame)
    build_follow_section(right_frame)


def build_anchor_section(parent):
    # Demonstrates how anchor positions affect tooltip placement when origin="widget"
    section_frame = create_section(parent, "Anchors (origin=widget)")
    container = ttk.Frame(section_frame)
    container.pack(pady=12, expand=True)
    grid_frame = ttk.Frame(container)
    grid_frame.pack()
    anchor_positions = {
        'nw': (0, 0), 'n': (0, 1), 'ne': (0, 2),
        'w': (1, 0), 'center': (1, 1), 'e': (1, 2),
        'sw': (2, 0), 's': (2, 1), 'se': (2, 2),
    }
    for i in range(3):
        grid_frame.columnconfigure(i, weight=1)
        grid_frame.rowconfigure(i, weight=1)
    for anchor, (row, col) in anchor_positions.items():
        button = ttk.Button(grid_frame, text=anchor, width=12)
        button.grid(row=row, column=col, padx=6, pady=6, sticky='nsew', ipadx=10, ipady=20)
        # Each button demonstrates a different anchor value for the tooltip
        Tip.bind(button, text=f'anchor={anchor}', origin='widget', anchor=anchor, padx=0, pady=0)


def build_follow_section(parent):
    # Shows how to use follow_mouse=True so the tooltip follows the cursor
    section_frame = create_section(parent, "Follow Mouse Tooltips")
    canvas = tk.Canvas(section_frame, background='#1e1e1e', highlightthickness=0)
    canvas.pack(fill='both', expand=True, padx=12, pady=12)
    canvas.create_text(10, 10, text="Move the mouse here", fill='white', font=('Segoe UI', 12), anchor='nw')
    # Bind a tooltip to the canvas that follows the mouse
    # A larger padding prevents mouse overlap issues
    Tip.bind(canvas, text="The tooltip tracks the cursor while over the canvas.", follow_mouse=True, padx=8, pady=12, show_delay=50, hide_delay=10000)


# --- Dynamic configuration section ---
def build_dynamic_section(parent):
    # This section lets users interactively change tooltip parameters and see the effect live
    section_frame = create_section(parent, "Live Configuration Panel")
    target_button = create_target_button(section_frame)
    # Bind a tooltip to the button so its config can be changed in real time
    dynamic_tip = Tip.bind(target_button, text="Editable tooltip.")
    # Arguments display field shows the current tooltip config as a string
    args_var = tk.StringVar(value="")
    args_frame = ttk.Frame(section_frame)
    args_frame.pack(fill='x', padx=8, pady=(0, 8))
    ttk.Label(args_frame, text="Tooltip Arguments:").pack(side='left')
    args_tooltip = create_arg_entry(args_var, args_frame)

    # Update tooltip text when args_var changes
    def update_tooltip(*_):
        args_tooltip.config(text=args_var.get())

    args_var.trace_add('write', update_tooltip)
    # Control panel lets users change all tooltip options
    control_panel = create_control_panel(section_frame)
    setup_configuration_groups(control_panel, dynamic_tip, args_var)


def create_arg_entry(args_var, args_frame):
    # Shows the current tooltip arguments and lets user copy them
    args_entry = ttk.Entry(args_frame, textvariable=args_var, state='readonly', width=80)
    args_entry.pack(side='left', fill='x', expand=True, padx=(4, 0))
    # Bind a tooltip to the entry to show the argument string
    args_tooltip = Tip.bind(args_entry, text=args_var.get(), wraplength=600, show_delay=300, hide_delay=5000, padx=8, pady=8)

    def copy_args():
        args_entry.clipboard_clear()
        args_entry.clipboard_append(args_var.get())

    copy_btn = ttk.Button(args_frame, text="Copy", command=copy_args)
    copy_btn.pack(side='left', padx=(4, 0))
    return args_tooltip


def create_target_button(parent):
    # Creates the button that is the target for the live-editable tooltip
    button_frame = ttk.Frame(parent)
    button_frame.pack(fill='x', padx=8, pady=8)
    target_button = ttk.Button(button_frame, text="Target Button")
    target_button.pack(fill='both', expand=True)
    return target_button


def create_control_panel(parent):
    control_frame = ttk.Frame(parent)
    control_frame.pack(fill='both', expand=True, padx=8, pady=(0, 8))
    for i in range(3):
        control_frame.columnconfigure(i, weight=1)
    for i in range(2):
        control_frame.rowconfigure(i, weight=1)
    return control_frame


def setup_configuration_groups(control_panel, tooltip, args_var=None):
    vars = create_configuration_vars()
    create_content_group(control_panel, vars)
    create_style_group(control_panel, vars)
    create_layout_group(control_panel, vars)
    create_position_group(control_panel, vars)
    create_border_group(control_panel, vars)
    create_timing_group(control_panel, vars)
    setup_variable_tracing(vars, tooltip, args_var)


#endregion
#region Config Groups & Utilities


def create_configuration_vars():
    return {
        'text': tk.StringVar(value='Editable tooltip.'),
        'state': tk.StringVar(value=Tip.STATE),
        'bg': tk.StringVar(value=Tip.BG),
        'fg': tk.StringVar(value=Tip.FG),
        'font_family': tk.StringVar(value=Tip.FONT[0]),
        'font_size': tk.IntVar(value=Tip.FONT[1]),
        'font_style': tk.StringVar(value=Tip.FONT[2]),
        'justify': tk.StringVar(value=Tip.JUSTIFY),
        'wraplength': tk.IntVar(value=Tip.WRAPLENGTH),
        'padx': tk.IntVar(value=Tip.PADX),
        'pady': tk.IntVar(value=Tip.PADY),
        'ipadx': tk.IntVar(value=Tip.IPADX),
        'ipady': tk.IntVar(value=Tip.IPADY),
        'origin': tk.StringVar(value=Tip.ORIGIN),
        'anchor': tk.StringVar(value=Tip.ANCHOR),
        'follow_mouse': tk.BooleanVar(value=Tip.FOLLOW_MOUSE),
        'borderwidth': tk.IntVar(value=Tip.BORDERWIDTH),
        'relief': tk.StringVar(value=Tip.RELIEF),
        'opacity': tk.DoubleVar(value=Tip.OPACITY),
        'show_delay': tk.IntVar(value=Tip.SHOW_DELAY),
        'hide_delay': tk.IntVar(value=Tip.HIDE_DELAY),
        'animation': tk.StringVar(value=Tip.ANIMATION),
        'anim_in': tk.IntVar(value=Tip.ANIM_IN),
        'anim_out': tk.IntVar(value=Tip.ANIM_OUT)
    }


def create_content_group(parent, vars):
    group = create_config_group(parent, 'Content / State', 0, 0)
    create_labeled_entry(group, 'Text:', vars['text'])
    create_labeled_combobox(group, 'State:', vars['state'], ['normal', 'disabled'], readonly=True)


def create_style_group(parent, vars):
    group = create_config_group(parent, 'Style', 0, 1)
    create_color_field(group, 'Background:', vars['bg'])
    create_color_field(group, 'Foreground:', vars['fg'])
    font_families = get_font_families()
    create_labeled_combobox(group, 'Font Family:', vars['font_family'], font_families, readonly=True, width=16)
    create_labeled_spinbox(group, 'Font Size:', vars['font_size'], 6, 24)
    create_labeled_combobox(group, 'Font Style:', vars['font_style'], ['normal', 'bold', 'italic', 'underline'], readonly=True)


def create_layout_group(parent, vars):
    group = create_config_group(parent, 'Layout', 0, 2)
    create_labeled_combobox(group, 'Justify:', vars['justify'], ['left', 'center', 'right'], readonly=True)
    create_labeled_spinbox(group, 'Wraplength:', vars['wraplength'], 0, 600, 20)
    create_labeled_spinbox(group, 'padx:', vars['padx'], -20, 50)
    create_labeled_spinbox(group, 'pady:', vars['pady'], -20, 50)
    create_labeled_spinbox(group, 'ipadx:', vars['ipadx'], 0, 50)
    create_labeled_spinbox(group, 'ipady:', vars['ipady'], 0, 50)


def create_position_group(parent, vars):
    group = create_config_group(parent, 'Positioning', 1, 0)
    create_labeled_combobox(group, 'Origin:', vars['origin'], ['mouse', 'widget'], readonly=True)
    create_labeled_combobox(group, 'Anchor:', vars['anchor'], ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'center'], readonly=True)
    create_labeled_checkbutton(group, 'Follow Mouse:', vars['follow_mouse'])


def create_border_group(parent, vars):
    group = create_config_group(parent, 'Border', 1, 1)
    create_labeled_spinbox(group, 'Border Width:', vars['borderwidth'], 0, 8)
    create_labeled_combobox(group, 'Relief:', vars['relief'], ['solid', 'raised', 'sunken', 'ridge', 'groove', 'flat'], readonly=True)
    create_labeled_spinbox(group, 'Opacity:', vars['opacity'], 0.0, 1.0, 0.01)


def create_timing_group(parent, vars):
    group = create_config_group(parent, 'Timing (ms)', 1, 2)
    create_labeled_spinbox(group, 'Show Delay:', vars['show_delay'], 0, 5000, 50)
    create_labeled_spinbox(group, 'Hide Delay:', vars['hide_delay'], 0, 15000, 250)
    create_labeled_combobox(group, 'Animation:', vars['animation'], ['fade', 'slide', 'none'], readonly=True)
    create_labeled_spinbox(group, 'Anim In:', vars['anim_in'], 0, 2000, 25)
    create_labeled_spinbox(group, 'Anim Out:', vars['anim_out'], 0, 2000, 25)


def setup_variable_tracing(vars, tooltip, args_var=None):
    # This function connects all config controls to the tooltip, so changes update it live.
    # It demonstrates how TkToolTip's config method can be used to update tooltip properties dynamically.
    # Every time a control changes, the tooltip is updated in real time, showing the effect of each parameter.
    def apply_changes(*_):
        # This function is called whenever a config control changes.
        # It collects all current values and calls tooltip.config.
        font_tuple = (vars['font_family'].get(), vars['font_size'].get(), vars['font_style'].get())
        try:
            tooltip.config(
                text=vars['text'].get(),
                state=vars['state'].get(),
                bg=vars['bg'].get(),
                fg=vars['fg'].get(),
                font=font_tuple,
                borderwidth=vars['borderwidth'].get(),
                relief=vars['relief'].get(),
                justify=vars['justify'].get(),
                wraplength=vars['wraplength'].get(),
                padx=vars['padx'].get(),
                pady=vars['pady'].get(),
                ipadx=vars['ipadx'].get(),
                ipady=vars['ipady'].get(),
                origin=vars['origin'].get(),
                anchor=vars['anchor'].get(),
                follow_mouse=vars['follow_mouse'].get(),
                show_delay=vars['show_delay'].get(),
                hide_delay=vars['hide_delay'].get(),
                animation=vars['animation'].get(),
                anim_in=vars['anim_in'].get(),
                anim_out=vars['anim_out'].get(),
                opacity=vars['opacity'].get()
            )
        except tk.TclError:
            return
        # Update arguments display to easily see and copy the current config string.
        if args_var is not None:
            try:
                args_dict = {
                    "text": vars['text'].get(),
                    "state": vars['state'].get(),
                    "bg": vars['bg'].get(),
                    "fg": vars['fg'].get(),
                    "font": font_tuple,
                    "borderwidth": vars['borderwidth'].get(),
                    "relief": vars['relief'].get(),
                    "justify": vars['justify'].get(),
                    "wraplength": vars['wraplength'].get(),
                    "padx": vars['padx'].get(),
                    "pady": vars['pady'].get(),
                    "ipadx": vars['ipadx'].get(),
                    "ipady": vars['ipady'].get(),
                    "origin": vars['origin'].get(),
                    "anchor": vars['anchor'].get(),
                    "follow_mouse": vars['follow_mouse'].get(),
                    "show_delay": vars['show_delay'].get(),
                    "hide_delay": vars['hide_delay'].get(),
                    "animation": vars['animation'].get(),
                    "anim_in": vars['anim_in'].get(),
                    "anim_out": vars['anim_out'].get(),
                    "opacity": vars['opacity'].get()
                }
            except tk.TclError:
                return
            # Format as a single-line string for display and learning.
            args_str = ', '.join(f"{k}={repr(v)}" for k, v in args_dict.items())
            args_var.set(args_str)
    # Attach tracing so every variable change triggers apply_changes, (live config updates).
    for variable in vars.values():
        variable.trace_add('write', apply_changes)
    # Initial update to show starting config.
    apply_changes()


#endregion
#region Widget Creation Utilities


def create_section(parent, title):
    frame = ttk.LabelFrame(parent, text=title, padding=(10, 8, 10, 10))
    frame.pack(fill='both', expand=True, padx=10, pady=8)
    return frame


def create_config_group(parent, title, row, column):
    group = ttk.LabelFrame(parent, text=title, padding=(8, 6, 8, 8))
    group.grid(row=row, column=column, sticky='nsew', padx=6, pady=6)
    return group


def create_labeled_widget(parent, label_text, widget_class, **widget_options):
    row_frame = ttk.Frame(parent)
    row_frame.pack(fill='x', pady=3)
    label = ttk.Label(row_frame, text=label_text, width=14, anchor='w')
    label.pack(side='left')
    widget = widget_class(row_frame, **widget_options)
    widget.pack(side='left', fill='x', expand=True, padx=(4, 0))
    return widget


def create_labeled_entry(parent, label_text, textvariable):
    return create_labeled_widget(parent, label_text, ttk.Entry, textvariable=textvariable)


def create_labeled_combobox(parent, label_text, textvariable, values, readonly=False, width=None):
    options = {'textvariable': textvariable, 'values': values}
    if readonly:
        options['state'] = 'readonly'
    if width:
        options['width'] = width
    return create_labeled_widget(parent, label_text, ttk.Combobox, **options)


def create_labeled_spinbox(parent, label_text, textvariable, from_val, to_val, increment=1):
    return create_labeled_widget(parent, label_text, ttk.Spinbox, textvariable=textvariable, from_=from_val, to=to_val, increment=increment, width=8)


def create_labeled_checkbutton(parent, label_text, variable):
    return create_labeled_widget(parent, label_text, ttk.Checkbutton, variable=variable)


def create_color_field(parent, label_text, color_var):
    row_frame = ttk.Frame(parent)
    row_frame.pack(fill='x', pady=3)
    label = ttk.Label(row_frame, text=label_text, width=14, anchor='w')
    label.pack(side='left')
    entry = ttk.Entry(row_frame, textvariable=color_var, width=10)
    entry.pack(side='left', fill='x', expand=True, padx=(4, 4))
    swatch = create_color_swatch(row_frame, color_var)
    picker_button = ttk.Button(row_frame, text='…', width=3, command=lambda: pick_color(color_var, label_text))
    picker_button.pack(side='left', padx=(4, 0))
    return entry


def create_color_swatch(parent, color_var):
    swatch = tk.Canvas(parent, width=20, height=20, highlightthickness=1, highlightbackground='#888', bd=0)
    swatch.pack(side='left')
    swatch_rect = swatch.create_rectangle(1, 1, 19, 19, outline='', fill=color_var.get())

    def update_swatch(*_):
        try:
            swatch.itemconfigure(swatch_rect, fill=color_var.get())
        except tk.TclError:
            pass

    color_var.trace_add('write', update_swatch)
    swatch.bind('<Button-1>', lambda e: pick_color(color_var, 'Color'))
    return swatch


def pick_color(color_var, label_text):
    initial_color = color_var.get() or '#ffffff'
    result = colorchooser.askcolor(color=initial_color, title=f"Select {label_text.strip(':')}")
    if result and result[1]:
        color_var.set(result[1])


def get_font_families():
    try:
        families = sorted(set(tkfont.families()))
        return ['TkDefaultFont'] + [f for f in families if f != 'TkDefaultFont']
    except Exception:
        return ['TkDefaultFont']


#endregion
#region Entrypoint


if __name__ == '__main__':
    main()


#endregion
