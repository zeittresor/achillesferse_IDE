# Achillesferse

Achillesferse ist eine kleine, echte Programmiersprache mit **IDE, Compiler, Runtime und Windows-Build-Skripten**. Das Projekt ist so angelegt, dass du nicht nur die mitgelieferten Beispiele ausführen kannst, sondern die Sprache und Runtime auch selbst erweitern kannst.

## Was in dieser Version verbessert wurde
- die IDE ist visuell sauberer strukturiert
- die **Sprachauswahl sitzt jetzt in einem Dropdown-Menü**
- die Beispiele werden **dynamisch aus dem Ordner `examples/`** geladen
- die fest verdrahteten Beispiel-Buttons wurden entfernt
- die Dokumentation wurde aufgeräumt und erweitert
- zusätzliche Beispielprogramme sind enthalten
- die Runtime unterstützt jetzt mehr Hilfsfunktionen für Grafik, Listen und Events

## Architektur
Achillesferse arbeitet in zwei Stufen:

1. `.af`-Quellcode wird vom Compiler nach Python übersetzt
2. das erzeugte Python-Programm nutzt die Achillesferse-Runtime

Für Windows kann daraus anschließend eine `.exe` gebaut werden.

Das hat Vorteile:
- die Sprache bleibt leicht erweiterbar
- Fehler lassen sich einfacher analysieren
- die Runtime bleibt zentral wartbar
- neue Grafik-/Sound-/UI-Helfer können ergänzt werden, ohne den Compiler komplett neu zu schreiben

## Enthaltene Dateien
- `achillesferse_compiler.py` – Compiler
- `achillesferse_runtime.py` – Runtime mit GUI-, Grafik-, Sound- und Event-Helfern
- `ide.py` – aufgeräumte IDE mit Beispielbrowser und Sprach-Dropdown
- `examples/` – mehrere vollständige Achillesferse-Beispiele
- `generated/` – Zielordner für erzeugte Python-Dateien
- `docs/language_de.md` – Sprachreferenz auf Deutsch
- `docs/language_en.md` – Sprachreferenz auf Englisch
- `build_windows_pyinstaller.bat` – EXE-Build mit PyInstaller
- `build_windows_nuitka.bat` – EXE-Build mit Nuitka
- `tests/run_tests.py` – automatisierte Prüfungen

## Mitgelieferte Beispiele
- `calculator.af` – Taschenrechner
- `eliza.af` – ELIZA-Chatbot
- `starfield.af` – Sternenflug-Simulation
- `mandelbrot.af` – Mandelbrot-Explorer mit Pfeiltasten und Zoom
- `breakout.af` – kleines Breakout-Spiel
- `drawing_pad.af` – Zeichenfläche mit Maus
- `piano.af` – kleines Ton-/Button-Demo-Programm
- `todo_list.af` – einfache Aufgabenliste
- `digital_clock.af` – Uhr mit periodischem Update

## Schnellstart unter Windows
### IDE starten
```bat
run_ide_windows.bat
```

### Ein Beispiel kompilieren und starten
```bat
py -3 achillesferse_compiler.py examples\calculator.af generated\calculator.py
py -3 generated\calculator.py
```

### Eine EXE erzeugen
```bat
build_windows_pyinstaller.bat examples\calculator.af
```

oder

```bat
build_windows_nuitka.bat examples\calculator.af
```

## Zur IDE
Die IDE verwendet in dieser Version **bewusst Tkinter/ttk** statt PyQt.

Grund:
- keine externe Pflicht-Abhängigkeit
- einfacher Start auf frischen Windows-Systemen
- die Runtime und die Beispielprogramme bleiben im Standard-Python-Umfeld lauffähig

Für eine spätere, noch luxuriösere IDE-Version wäre **PyQt absolut sinnvoll**, besonders für Docking, Syntax-Highlighting, Menüs, Projektbäume und komfortableres Packaging.

## Fähigkeiten der Runtime
Aktuell enthalten:
- Fenster, Labels, Buttons, Eingabefelder, Textfelder, Canvas, Frames, Listboxen
- periodische Updates über `ON_TICK`
- Canvas-Zeichnen
- Event-Bindings über `BIND`
- Zugriff auf Maus-/Tastatur-Ereignisse
- Sound-Beeps
- ELIZA-Helfer
- Starfield-Helfer
- Mandelbrot-Helfer
- Breakout-Helfer
- Listen-Helfer für Listboxen

## Erweiterbarkeit
Achillesferse ist absichtlich offen konstruiert. Typische nächste Ausbaustufen wären:
- Bilder / Sprites
- Dateidialoge direkt aus der Sprache
- Menüs
- Module / Imports
- Audio-Dateien statt nur Beep
- mehr Zeichenprimitive
- Tilemaps / Spielobjekte
- optional später ein Bytecode- oder C-Backend

## Test-Hinweis
Die Beispiele und die Python-Generierung wurden automatisiert geprüft. Die GUI-Programme wurden in einer virtuellen Anzeige gestartet, damit Startverhalten und Runtime getestet werden konnten.

Die Windows-EXE-Builds sind im Paket vorbereitet, wurden hier aber nicht auf einem echten Windows-Desktop ausgeführt.
