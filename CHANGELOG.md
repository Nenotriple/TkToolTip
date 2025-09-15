# Changelog

## v1.12

### ✨ New

* Added **callback text tooltips** support callable text
* Added **opacity** parameter for adjustable window transparency
* Added **animation options** (`animation`, `anim_in`, `anim_out`) with fade, slide, and instant styles
* Added **comprehensive demo script** (`examples/demo.py`)

### ⚙️ Changed

* Moved **animation logic** to a separate `animation_utils.py` module
* Added **type stubs** and annotations for simplified IDE hints
* Refactored **parameter handling** (centralized `PARAMS`, keyword-only API, `_apply_kwargs` helper)
* Updated and adjusted parameter position and names
* Renamed internal `widget_id` → `show_after_id`
* Altered parameters *(from > to)*:
  * `create` > `bind`
  * `delay` > `show_delay`
  * `fade_in` > `anim_in`
  * `fade_out` > `anim_out`

### 🐛 Fixed

* Tooltip now hides on `<ButtonPress>` and `<ButtonRelease>` events
* Prevented tooltips from appearing off-screen
