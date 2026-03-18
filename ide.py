from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from achillesferse_compiler import ParseError, compile_file, parse_program


ROOT = Path(__file__).resolve().parent
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"
DOCS = ROOT / "docs"


UI_TEXT = {
    "de": {
        "window_title": "Achillesferse IDE",
        "header_title": "Achillesferse IDE",
        "header_subtitle": "Editor, Compiler und Beispielbrowser für die Achillesferse-Sprache",
        "language": "Sprache",
        "new": "Neu",
        "open": "Öffnen",
        "save": "Speichern",
        "validate": "Prüfen",
        "compile": "Kompilieren",
        "run": "Ausführen",
        "build": "EXE-Hinweis",
        "refresh_examples": "Beispiele neu laden",
        "examples": "Beispiele",
        "examples_hint": "Doppelklick lädt eine .af-Datei aus dem examples-Ordner.",
        "editor": "Editor",
        "output": "Ausgabe",
        "quick_help": "Sprachhilfe",
        "readme": "README",
        "status_ready": "Bereit.",
        "no_file": "(noch keine Datei)",
        "welcome": 'APP title="Achillesferse App" width=860 height=540 bg="#202225"\nWIDGET info LABEL text="Öffne links ein Beispiel oder beginne mit einem neuen Programm." fg="white" bg="#202225" padx=16 pady=16\n',
        "opened": "Geöffnet: {path}",
        "saved": "Gespeichert: {path}",
        "new_doc": "Neues Dokument erstellt.",
        "validation_ok": "Prüfung erfolgreich. Widgets: {widgets}, Funktionen: {functions}",
        "parse_error_title": "Parserfehler",
        "compiled": "Kompiliert nach: {path}",
        "running": "Starte: {name}",
        "exit_code": "Rückgabecode: {code}",
        "build_help_title": "Windows-EXE bauen",
        "build_help": "Nutze die Batch-Dateien im Paketstamm.\n\nBeispiele:\n- build_windows_pyinstaller.bat examples\\calculator.af\n- build_windows_nuitka.bat examples\\breakout.af\n\nDie IDE selbst bleibt absichtlich ohne zusätzliche Pflicht-Abhängigkeiten.",
        "example_loaded": "Beispiel geladen: {name}",
        "no_examples": "Keine Beispiele gefunden.",
        "choose_language": "Deutsch",
    },
    "en": {
        "window_title": "Achillesferse IDE",
        "header_title": "Achillesferse IDE",
        "header_subtitle": "Editor, compiler and example browser for the Achillesferse language",
        "language": "Language",
        "new": "New",
        "open": "Open",
        "save": "Save",
        "validate": "Validate",
        "compile": "Compile",
        "run": "Run",
        "build": "EXE Help",
        "refresh_examples": "Reload examples",
        "examples": "Examples",
        "examples_hint": "Double-click to load a .af file from the examples folder.",
        "editor": "Editor",
        "output": "Output",
        "quick_help": "Language Help",
        "readme": "README",
        "status_ready": "Ready.",
        "no_file": "(no file yet)",
        "welcome": 'APP title="Achillesferse App" width=860 height=540 bg="#202225"\nWIDGET info LABEL text="Open an example from the left or start a new program." fg="white" bg="#202225" padx=16 pady=16\n',
        "opened": "Opened: {path}",
        "saved": "Saved: {path}",
        "new_doc": "New document created.",
        "validation_ok": "Validation OK. Widgets: {widgets}, Functions: {functions}",
        "parse_error_title": "Parse error",
        "compiled": "Compiled to: {path}",
        "running": "Running: {name}",
        "exit_code": "Exit code: {code}",
        "build_help_title": "Build Windows EXE",
        "build_help": "Use the batch files in the package root.\n\nExamples:\n- build_windows_pyinstaller.bat examples\\calculator.af\n- build_windows_nuitka.bat examples\\breakout.af\n\nThe IDE itself intentionally stays free of extra mandatory dependencies.",
        "example_loaded": "Loaded example: {name}",
        "no_examples": "No examples found.",
        "choose_language": "English",
    },
}


def read_text_if_exists(path: Path, fallback: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return fallback


class AchillesferseIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_file: Path | None = None
        self.example_paths: list[Path] = []
        self.ui_lang = "de"
        self.status_var = tk.StringVar(value=UI_TEXT[self.ui_lang]["status_ready"])
        self.path_var = tk.StringVar(value=UI_TEXT[self.ui_lang]["no_file"])
        self.lang_display_var = tk.StringVar(value=UI_TEXT[self.ui_lang]["choose_language"])
        self._configure_window()
        self._build_ui()
        self._reload_examples()
        self._load_welcome_text()
        self._refresh_localized_texts()

    def tr(self, key: str, **kwargs) -> str:
        text = UI_TEXT[self.ui_lang][key]
        return text.format(**kwargs) if kwargs else text

    def _configure_window(self):
        self.title(UI_TEXT[self.ui_lang]["window_title"])
        self.geometry("1340x860")
        self.minsize(1040, 700)
        self.configure(bg="#1E1F22")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Root.TFrame", background="#1E1F22")
        style.configure("Panel.TFrame", background="#25262B")
        style.configure("Card.TFrame", background="#2B2D31")
        style.configure("Header.TLabel", background="#1E1F22", foreground="#F5F5F5", font=("Segoe UI", 18, "bold"))
        style.configure("SubHeader.TLabel", background="#1E1F22", foreground="#B8BCC8", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background="#25262B", foreground="#F5F5F5", font=("Segoe UI", 11, "bold"))
        style.configure("Hint.TLabel", background="#25262B", foreground="#B8BCC8", font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#18191C", foreground="#D7D7D7", font=("Segoe UI", 9))
        style.configure("Toolbar.TButton", font=("Segoe UI", 9), padding=6)
        style.configure("TNotebook", background="#25262B", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 8), font=("Segoe UI", 9))
        style.configure("TCombobox", padding=4)

    def _build_ui(self):
        root = ttk.Frame(self, style="Root.TFrame", padding=(14, 12, 14, 10))
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="Root.TFrame")
        header.pack(fill="x")

        title_box = ttk.Frame(header, style="Root.TFrame")
        title_box.pack(side="left", fill="x", expand=True)
        self.header_title = ttk.Label(title_box, style="Header.TLabel")
        self.header_title.pack(anchor="w")
        self.header_subtitle = ttk.Label(title_box, style="SubHeader.TLabel")
        self.header_subtitle.pack(anchor="w", pady=(2, 0))

        lang_box = ttk.Frame(header, style="Root.TFrame")
        lang_box.pack(side="right", anchor="ne")
        self.language_label = ttk.Label(lang_box, style="SubHeader.TLabel")
        self.language_label.pack(side="left", padx=(0, 8))
        self.language_combo = ttk.Combobox(
            lang_box,
            state="readonly",
            width=16,
            values=["Deutsch", "English"],
            textvariable=self.lang_display_var,
        )
        self.language_combo.pack(side="left")
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)

        toolbar_card = ttk.Frame(root, style="Card.TFrame", padding=10)
        toolbar_card.pack(fill="x", pady=(12, 10))
        self.toolbar_buttons = {}
        toolbar_specs = [
            ("new", self.new_file),
            ("open", self.open_file),
            ("save", self.save_file),
            ("validate", self.validate_source),
            ("compile", self.compile_current),
            ("run", self.run_current),
            ("build", self.show_build_help),
            ("refresh_examples", self._reload_examples),
        ]
        for key, cmd in toolbar_specs:
            btn = ttk.Button(toolbar_card, style="Toolbar.TButton", command=cmd)
            btn.pack(side="left", padx=(0, 8))
            self.toolbar_buttons[key] = btn

        self.file_label = ttk.Label(root, style="SubHeader.TLabel", textvariable=self.path_var)
        self.file_label.pack(fill="x", pady=(0, 8))

        body = ttk.Panedwindow(root, orient="horizontal")
        body.pack(fill="both", expand=True)

        sidebar = ttk.Frame(body, style="Panel.TFrame", padding=10)
        body.add(sidebar, weight=1)
        self.examples_label = ttk.Label(sidebar, style="Section.TLabel")
        self.examples_label.pack(anchor="w")
        self.examples_hint = ttk.Label(sidebar, style="Hint.TLabel", wraplength=250, justify="left")
        self.examples_hint.pack(anchor="w", pady=(2, 8))

        search_box = ttk.Frame(sidebar, style="Panel.TFrame")
        search_box.pack(fill="x", pady=(0, 8))
        self.example_filter_var = tk.StringVar()
        self.example_filter_var.trace_add("write", lambda *_: self._reload_examples())
        filter_entry = tk.Entry(
            search_box,
            textvariable=self.example_filter_var,
            bg="#1E1F22",
            fg="#F5F5F5",
            insertbackground="#F5F5F5",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#3B3E45",
            highlightcolor="#5A8CFF",
            font=("Segoe UI", 10),
        )
        filter_entry.pack(fill="x")

        list_frame = ttk.Frame(sidebar, style="Panel.TFrame")
        list_frame.pack(fill="both", expand=True)
        self.example_list = tk.Listbox(
            list_frame,
            bg="#1E1F22",
            fg="#F5F5F5",
            selectbackground="#5A8CFF",
            selectforeground="#FFFFFF",
            activestyle="none",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#3B3E45",
            highlightcolor="#5A8CFF",
            font=("Consolas", 10),
        )
        ysb = ttk.Scrollbar(list_frame, orient="vertical", command=self.example_list.yview)
        self.example_list.configure(yscrollcommand=ysb.set)
        self.example_list.pack(side="left", fill="both", expand=True)
        ysb.pack(side="right", fill="y")
        self.example_list.bind("<Double-Button-1>", self._load_selected_example)
        self.example_list.bind("<Return>", self._load_selected_example)

        editor_area = ttk.Frame(body, style="Panel.TFrame", padding=10)
        body.add(editor_area, weight=4)
        self.editor_label = ttk.Label(editor_area, style="Section.TLabel")
        self.editor_label.pack(anchor="w", pady=(0, 8))

        editor_card = ttk.Frame(editor_area, style="Card.TFrame")
        editor_card.pack(fill="both", expand=True)

        self.editor = tk.Text(
            editor_card,
            wrap="none",
            undo=True,
            bg="#111216",
            fg="#F4F4F4",
            insertbackground="#F4F4F4",
            selectbackground="#324A76",
            relief="flat",
            padx=12,
            pady=10,
            font=("Consolas", 11),
        )
        editor_y = ttk.Scrollbar(editor_card, orient="vertical", command=self.editor.yview)
        editor_x = ttk.Scrollbar(editor_card, orient="horizontal", command=self.editor.xview)
        self.editor.configure(yscrollcommand=editor_y.set, xscrollcommand=editor_x.set)
        self.editor.pack(side="left", fill="both", expand=True)
        editor_y.pack(side="right", fill="y")
        editor_x.pack(side="bottom", fill="x")

        bottom = ttk.Notebook(editor_area)
        bottom.pack(fill="both", expand=False, pady=(10, 0))
        self.output = tk.Text(
            bottom,
            wrap="word",
            height=10,
            bg="#101114",
            fg="#ECECEC",
            insertbackground="#ECECEC",
            relief="flat",
            padx=10,
            pady=8,
            font=("Consolas", 10),
        )
        self.docs = tk.Text(
            bottom,
            wrap="word",
            height=10,
            bg="#101114",
            fg="#ECECEC",
            insertbackground="#ECECEC",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10),
        )
        self.readme = tk.Text(
            bottom,
            wrap="word",
            height=10,
            bg="#101114",
            fg="#ECECEC",
            insertbackground="#ECECEC",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10),
        )
        bottom.add(self.output)
        bottom.add(self.docs)
        bottom.add(self.readme)
        self.bottom_notebook = bottom

        status = ttk.Frame(root, style="Root.TFrame")
        status.pack(fill="x", pady=(10, 0))
        self.status_label = ttk.Label(status, style="Status.TLabel", textvariable=self.status_var, padding=(8, 6))
        self.status_label.pack(fill="x")

    def _load_docs_for_language(self):
        lang_suffix = "de" if self.ui_lang == "de" else "en"
        quick_help = read_text_if_exists(DOCS / f"language_{lang_suffix}.md", fallback="")
        readme_name = "README_DE.md" if self.ui_lang == "de" else "README_EN.md"
        readme_text = read_text_if_exists(ROOT / readme_name, fallback="")
        for widget, text in ((self.docs, quick_help), (self.readme, readme_text)):
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            widget.insert("1.0", text)
            widget.configure(state="disabled")

    def _refresh_localized_texts(self):
        self.title(self.tr("window_title"))
        self.header_title.configure(text=self.tr("header_title"))
        self.header_subtitle.configure(text=self.tr("header_subtitle"))
        self.language_label.configure(text=self.tr("language"))
        self.examples_label.configure(text=self.tr("examples"))
        self.examples_hint.configure(text=self.tr("examples_hint"))
        self.editor_label.configure(text=self.tr("editor"))
        for key, btn in self.toolbar_buttons.items():
            btn.configure(text=self.tr(key))
        self.bottom_notebook.tab(0, text=self.tr("output"))
        self.bottom_notebook.tab(1, text=self.tr("quick_help"))
        self.bottom_notebook.tab(2, text=self.tr("readme"))
        if self.current_file is None:
            self.path_var.set(self.tr("no_file"))
        self.status_var.set(self.tr("status_ready"))
        self._load_docs_for_language()
        self._update_language_combo_text()

    def _update_language_combo_text(self):
        display = "Deutsch" if self.ui_lang == "de" else "English"
        self.lang_display_var.set(display)

    def change_language(self, event=None):
        selected = self.language_combo.get().strip().lower()
        self.ui_lang = "de" if "deutsch" in selected else "en"
        self._refresh_localized_texts()
        if self.current_file is None and not self.editor.get("1.0", "end-1c").strip():
            self._load_welcome_text()

    def _load_welcome_text(self):
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", self.tr("welcome"))

    def log(self, text: str):
        self.output.insert("end", text.rstrip() + "\n")
        self.output.see("end")
        self.status_var.set(text.rstrip())

    def get_source(self):
        return self.editor.get("1.0", "end-1c")

    def set_current_file(self, path: Path | None):
        self.current_file = path
        self.path_var.set(str(path) if path else self.tr("no_file"))

    def new_file(self):
        self.set_current_file(None)
        self._load_welcome_text()
        self.log(self.tr("new_doc"))

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Achillesferse", "*.af"), ("All files", "*.*")])
        if not path:
            return
        path = Path(path)
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", path.read_text(encoding="utf-8"))
        self.set_current_file(path)
        self.log(self.tr("opened", path=path))

    def save_file(self):
        path = self.current_file
        if path is None:
            chosen = filedialog.asksaveasfilename(defaultextension=".af", filetypes=[("Achillesferse", "*.af")])
            if not chosen:
                return
            path = Path(chosen)
        path.write_text(self.get_source(), encoding="utf-8")
        self.set_current_file(path)
        self.log(self.tr("saved", path=path))

    def validate_source(self):
        try:
            program = parse_program(self.get_source())
            self.log(self.tr("validation_ok", widgets=len(program["widgets"]), functions=len(program["functions"])))
        except ParseError as exc:
            self.log(f"{self.tr('parse_error_title')}: {exc}")
            messagebox.showerror(self.tr("parse_error_title"), str(exc))

    def compile_current(self):
        if self.current_file is None:
            self.save_file()
        if self.current_file is None:
            return None
        GENERATED.mkdir(exist_ok=True)
        output_path = GENERATED / f"{self.current_file.stem}.py"
        compile_file(self.current_file, output_path)
        self.log(self.tr("compiled", path=output_path))
        return output_path

    def run_current(self):
        compiled = self.compile_current()
        if not compiled:
            return
        self.log(self.tr("running", name=compiled.name))
        proc = subprocess.Popen(
            [sys.executable, str(compiled)],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        out, _ = proc.communicate()
        if out:
            self.log(out)
        self.log(self.tr("exit_code", code=proc.returncode))

    def show_build_help(self):
        messagebox.showinfo(self.tr("build_help_title"), self.tr("build_help"))

    def _reload_examples(self):
        self.example_list.delete(0, "end")
        self.example_paths.clear()
        EXAMPLES.mkdir(exist_ok=True)
        needle = self.example_filter_var.get().strip().lower() if hasattr(self, "example_filter_var") else ""
        paths = sorted(EXAMPLES.rglob("*.af"))
        for path in paths:
            label = path.relative_to(EXAMPLES).as_posix()
            if needle and needle not in label.lower():
                continue
            self.example_paths.append(path)
            self.example_list.insert("end", label)
        if not self.example_paths:
            self.example_list.insert("end", self.tr("no_examples"))

    def _load_selected_example(self, event=None):
        sel = self.example_list.curselection()
        if not sel or not self.example_paths:
            return
        index = sel[0]
        if index >= len(self.example_paths):
            return
        path = self.example_paths[index]
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", path.read_text(encoding="utf-8"))
        self.set_current_file(path)
        self.log(self.tr("example_loaded", name=path.relative_to(EXAMPLES).as_posix()))


if __name__ == "__main__":
    AchillesferseIDE().mainloop()
