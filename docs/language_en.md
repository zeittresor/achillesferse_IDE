# Achillesferse – Language Reference (EN)

## Overview
Achillesferse is a block-based DSL for small GUI, graphics and text programs. The language intentionally stays compact and moves many capabilities into the runtime.

## Overall structure
A typical Achillesferse program consists of:
- `APP` – window metadata
- `VAR` – initial variables
- `WIDGET` – UI elements
- `BIND` – event bindings
- `FUNC` – functions
- `ON_START` – startup logic
- `ON_TICK` – periodic logic

## Top-level statements

### APP
```text
APP title="Title" width=900 height=600 bg="#202225"
```

### VAR
```text
VAR counter = 0
VAR name = "Mischa"
VAR values = [1, 2, 3]
```

### WIDGET
```text
WIDGET send_btn BUTTON text="Send" width=10 action="send()"
```

General form:
```text
WIDGET name TYPE option=value option=value ...
```

Supported widget types:
- `LABEL`
- `ENTRY`
- `BUTTON`
- `TEXT`
- `CANVAS`
- `FRAME`
- `LISTBOX`

Common options:
- `text`
- `width`, `height`
- `bg`, `fg`
- `font`
- `padx`, `pady`
- `row`, `column`, `rowspan`, `columnspan`, `sticky`
- `side`, `fill`, `expand`
- `readonly=true` for `ENTRY` or `TEXT`
- `action="function()"` for `BUTTON`
- `parent="container_name"`

### BIND
```text
BIND user_input <Return> send()
BIND canvas <Left> move_left()
BIND canvas <B1-Motion> paint()
```

### FUNC
```text
FUNC add(a, b)
    RETURN a + b
END
```

### ON_START
Runs shortly after the window has been built.

```text
ON_START
    CALL initialize()
END
```

### ON_TICK
Runs every N milliseconds.

```text
ON_TICK 33
    CALL update_scene()
END
```

## Statements

### SET
```text
SET score = score + 10
```

### UISET
Sets the text content of an `ENTRY`, `TEXT`, `LABEL` or `LISTBOX`.

```text
UISET display, "Ready"
UISET tasks, "A\nB\nC"
```

### APPEND
Appends text to `ENTRY`, `TEXT`, `LABEL`, or adds new rows to a `LISTBOX`.

```text
APPEND conversation, "Hello\n"
APPEND tasks, "Milk"
```

### CLEAR
```text
CLEAR input
CLEAR tasks
```

### FOCUS
```text
FOCUS input
```

### CALL / EXPR
Executes an expression.

```text
CALL send()
CALL sound_beep(1200, 80)
CALL canvas_oval('scene', 10, 10, 30, 30, fill='white', outline='')
```

### RETURN
```text
RETURN
RETURN value
```

### IF / ELIF / ELSE
```text
IF score > 100
    UISET info, "Won"
ELIF score > 50
    UISET info, "Almost there"
ELSE
    UISET info, "Keep going"
END
```

### FOR
```text
FOR item IN range(10)
    CALL canvas_line('scene', 0, item * 10, 100, item * 10, fill='gray')
END
```

### WHILE
```text
WHILE running
    SET counter = counter + 1
END
```

## Available expression helpers

### Standard functions
- `str`, `int`, `float`, `bool`
- `len`, `min`, `max`, `sum`, `range`, `round`, `abs`
- `math`, `random`, `json`, `time`

### Widget access
- `text('widget')` – read widget text
- `ui('widget')` – get the direct widget object
- `state` – dictionary with state values
- `widgets` – dictionary of all widgets

### Canvas helpers
- `canvas_rect(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_oval(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_line(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_text(widget, x, y, text, **kwargs)`
- `canvas_clear(widget)`

### Sound / app
- `sound_beep(freq, duration_ms)`
- `app_exit()`

### Example/special helpers
- `safe_eval(expr)`
- `calculate_expression(expr)`
- `eliza_reply(text)`
- `init_starfield(count, width, height)`
- `step_starfield(stars, speed, width, height)`
- `draw_starfield(widget, stars)`
- `draw_mandelbrot(widget, center_x, center_y, zoom, max_iter, block)`
- `breakout_new(width, height, brick_rows, brick_cols)`
- `breakout_step(state, width, height)`
- `breakout_move_paddle(state, delta, width)`
- `breakout_draw(widget, state)`
- `now_text(format)`
- `listbox_delete_selected(widget)`

### Event helpers
Useful inside `BIND` actions:
- `event_x()`
- `event_y()`
- `event_keysym()`

Example:
```text
FUNC paint()
    CALL canvas_oval('pad', event_x()-3, event_y()-3, event_x()+3, event_y()+3, fill='white', outline='')
END
```

## Layout rules
- `pack` is used by default
- as soon as `row=` or `column=` is present, the runtime switches to `grid`

## Import behavior of generated Python files
The generated Python files search the runtime automatically:
- in their own folder
- in the parent folder
- in a `src` subfolder

That makes runtime discovery more robust than in the first package version.

## Practical notes
- Achillesferse intentionally stays small. More complex features are exposed through runtime helpers.
- It is a good fit for quick GUI tools, small games, visual demos and text programs.
- For larger projects, future additions such as modules, static type checks and imports would make sense.
