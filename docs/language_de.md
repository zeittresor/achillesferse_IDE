# Achillesferse – Sprachreferenz (DE)

## Überblick
Achillesferse ist eine blockbasierte DSL für kleine GUI-, Grafik- und Textprogramme. Die Sprache bleibt absichtlich kompakt und verlagert viele Fähigkeiten in die Runtime.

## Grundstruktur
Ein Achillesferse-Programm besteht typischerweise aus:
- `APP` – Fenstermetadaten
- `VAR` – Anfangsvariablen
- `WIDGET` – UI-Elemente
- `BIND` – Event-Bindings
- `FUNC` – Funktionen
- `ON_START` – Startlogik
- `ON_TICK` – periodische Logik

## Top-Level-Anweisungen

### APP
```text
APP title="Titel" width=900 height=600 bg="#202225"
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

Allgemeines Schema:
```text
WIDGET name TYPE option=value option=value ...
```

Unterstützte Widget-Typen:
- `LABEL`
- `ENTRY`
- `BUTTON`
- `TEXT`
- `CANVAS`
- `FRAME`
- `LISTBOX`

Häufige Optionen:
- `text`
- `width`, `height`
- `bg`, `fg`
- `font`
- `padx`, `pady`
- `row`, `column`, `rowspan`, `columnspan`, `sticky`
- `side`, `fill`, `expand`
- `readonly=true` für `ENTRY` oder `TEXT`
- `action="funktion()"` für `BUTTON`
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
Wird kurz nach dem Fensteraufbau ausgeführt.

```text
ON_START
    CALL initialize()
END
```

### ON_TICK
Wird periodisch alle N Millisekunden ausgeführt.

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
Setzt den Textinhalt eines `ENTRY`, `TEXT`, `LABEL` oder `LISTBOX`.

```text
UISET display, "Ready"
UISET tasks, "A\nB\nC"
```

### APPEND
Hängt Text an `ENTRY`, `TEXT`, `LABEL` oder neue Zeilen an eine `LISTBOX` an.

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
Führt einen Ausdruck aus.

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
    UISET info, "Gewonnen"
ELIF score > 50
    UISET info, "Fast geschafft"
ELSE
    UISET info, "Weiter"
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

## Verfügbare Ausdruckshilfen

### Standardfunktionen
- `str`, `int`, `float`, `bool`
- `len`, `min`, `max`, `sum`, `range`, `round`, `abs`
- `math`, `random`, `json`, `time`

### Widget-Zugriff
- `text('widget')` – Text eines Widgets lesen
- `ui('widget')` – direktes Widget-Objekt erhalten
- `state` – Wörterbuch mit Zustandswerten
- `widgets` – Wörterbuch aller Widgets

### Canvas-Helfer
- `canvas_rect(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_oval(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_line(widget, x1, y1, x2, y2, **kwargs)`
- `canvas_text(widget, x, y, text, **kwargs)`
- `canvas_clear(widget)`

### Sound / App
- `sound_beep(freq, duration_ms)`
- `app_exit()`

### Beispiel-/Spezialhelfer
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

### Event-Helfer
Diese sind nützlich in `BIND`-Aktionen:
- `event_x()`
- `event_y()`
- `event_keysym()`

Beispiel:
```text
FUNC paint()
    CALL canvas_oval('pad', event_x()-3, event_y()-3, event_x()+3, event_y()+3, fill='white', outline='')
END
```

## Layout-Regeln
- Standardmäßig wird `pack` verwendet
- sobald `row=` oder `column=` gesetzt ist, nutzt die Runtime automatisch `grid`

## Import-Verhalten der generierten Python-Dateien
Die vom Compiler erzeugten Python-Dateien suchen die Runtime automatisch:
- im eigenen Ordner
- im Elternordner
- in einem Unterordner `src`

Dadurch ist die Runtime robuster auffindbar als in der ersten Paketfassung.

## Praktische Hinweise
- Achillesferse ist bewusst klein. Komplexere Dinge laufen über Runtime-Helfer.
- Für schnelle GUI-Tools, kleine Spiele, visuelle Demos und Textprogramme ist das Modell gut geeignet.
- Für sehr große Projekte wären später Module, Typprüfung und Import-Systeme sinnvoll.
