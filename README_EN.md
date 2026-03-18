# Achillesferse

Achillesferse is a small but real programming language with an **IDE, compiler, runtime and Windows build scripts**. The goal is not just to ship demos, but to provide a functional and extendable base.

## What was improved in this version
- the IDE is visually cleaner and better structured
- the **language selector now lives in a dropdown**
- examples are **loaded dynamically from the `examples/` folder**
- hard-wired example buttons were removed
- the documentation was rewritten and expanded
- additional example programs are included
- the runtime now exposes more helpers for graphics, lists and events

## Architecture
Achillesferse works in two steps:

1. `.af` source code is compiled to Python
2. the generated Python program runs on the Achillesferse runtime

A Windows `.exe` can then be built from that result.

Advantages:
- the language stays easy to extend
- generated code is easier to inspect when something fails
- the runtime remains centrally maintainable
- new graphics/sound/UI helpers can be added without rewriting the whole compiler

## Included files
- `achillesferse_compiler.py` – compiler
- `achillesferse_runtime.py` – runtime with GUI, graphics, sound and event helpers
- `ide.py` – cleaned-up IDE with example browser and language dropdown
- `examples/` – multiple complete Achillesferse examples
- `generated/` – output folder for generated Python files
- `docs/language_de.md` – German language reference
- `docs/language_en.md` – English language reference
- `build_windows_pyinstaller.bat` – EXE build with PyInstaller
- `build_windows_nuitka.bat` – EXE build with Nuitka
- `tests/run_tests.py` – automated checks

## Included examples
- `calculator.af` – calculator
- `eliza.af` – ELIZA chatbot
- `starfield.af` – starfield simulation
- `mandelbrot.af` – Mandelbrot explorer with arrow keys and zoom
- `breakout.af` – small breakout game
- `drawing_pad.af` – mouse drawing pad
- `piano.af` – small tone/button demo
- `todo_list.af` – simple task list
- `digital_clock.af` – clock with periodic updates

## Quick start on Windows
### Start the IDE
```bat
run_ide_windows.bat
```

### Compile and run an example
```bat
py -3 achillesferse_compiler.py examples\calculator.af generated\calculator.py
py -3 generated\calculator.py
```

### Build an EXE
```bat
build_windows_pyinstaller.bat examples\calculator.af
```

or

```bat
build_windows_nuitka.bat examples\calculator.af
```

## About the IDE
This revision deliberately keeps the IDE on **Tkinter/ttk** instead of PyQt.

Reason:
- no external mandatory dependency
- easier startup on fresh Windows systems
- the runtime and sample programs stay in standard Python territory

A later, more feature-rich IDE would absolutely be a good use case for **PyQt**, especially for docking, syntax highlighting, project trees, menus and more advanced packaging.

## Runtime capabilities
Currently included:
- windows, labels, buttons, entries, text widgets, canvas, frames and listboxes
- periodic updates via `ON_TICK`
- canvas drawing
- event bindings via `BIND`
- access to mouse and keyboard event data
- sound beeps
- ELIZA helper
- starfield helper
- Mandelbrot helper
- Breakout helper
- list helpers for listboxes

## Extendability
Achillesferse is intentionally open-ended. Natural next steps would be:
- images / sprites
- file dialogs directly from the language
- menus
- modules / imports
- audio files instead of beep only
- more drawing primitives
- tilemaps / game objects
- optional bytecode or C backend later

## Testing note
The examples and the Python generation were checked automatically. The GUI programs were launched in a virtual display so startup behavior and runtime integration could be exercised.

The Windows EXE build scripts are included, but they were not executed on a real Windows desktop in this environment.
