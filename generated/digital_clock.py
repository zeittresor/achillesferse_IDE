from __future__ import annotations

import json
import sys
from pathlib import Path

_THIS_FILE = Path(__file__).resolve()
_SEARCH_DIRS = [
    _THIS_FILE.parent,
    _THIS_FILE.parent.parent,
    _THIS_FILE.parent.parent / "src",
]
for _candidate in _SEARCH_DIRS:
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

from achillesferse_runtime import AchillesferseApp

PROGRAM = json.loads(r"""{
  "app": {
    "title": "Achillesferse Digital Clock",
    "width": 420,
    "height": 220,
    "bg": "#0E1014"
  },
  "vars": {},
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "Digital Clock",
        "bg": "#0E1014",
        "fg": "#D4D9E3",
        "font": "Segoe UI 12",
        "padx": 10,
        "pady": 6
      }
    },
    {
      "name": "clock",
      "type": "LABEL",
      "options": {
        "text": "00:00:00",
        "bg": "#0E1014",
        "fg": "white",
        "font": "Consolas 32",
        "padx": 10,
        "pady": 12
      }
    },
    {
      "name": "date",
      "type": "LABEL",
      "options": {
        "text": "",
        "bg": "#0E1014",
        "fg": "#D4D9E3",
        "font": "Segoe UI 11",
        "padx": 10,
        "pady": 4
      }
    }
  ],
  "bindings": [],
  "functions": {
    "redraw": {
      "params": [],
      "body": [
        {
          "type": "uiset",
          "widget": "clock",
          "expr": "now_text(\"%H:%M:%S\")"
        },
        {
          "type": "uiset",
          "widget": "date",
          "expr": "now_text(\"%A, %d %B %Y\")"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "expr",
      "expr": "redraw()"
    }
  ],
  "on_tick": {
    "ms": 250,
    "body": [
      {
        "type": "expr",
        "expr": "redraw()"
      }
    ]
  }
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
