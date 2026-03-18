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
    "title": "Achillesferse Piano",
    "width": 560,
    "height": 300,
    "bg": "#1B1D23"
  },
  "vars": {},
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "Mini Piano / Beep Demo",
        "bg": "#1B1D23",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "info",
      "type": "LABEL",
      "options": {
        "text": "Buttons trigger simple beeps via the runtime.",
        "bg": "#1B1D23",
        "fg": "#D1D5DE",
        "font": "Segoe UI 10",
        "padx": 10,
        "pady": 4
      }
    },
    {
      "name": "panel",
      "type": "FRAME",
      "options": {
        "bg": "#1B1D23",
        "padx": 12,
        "pady": 12
      }
    },
    {
      "name": "c4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 0,
        "text": "C",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(262)"
      }
    },
    {
      "name": "d4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 1,
        "text": "D",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(294)"
      }
    },
    {
      "name": "e4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 2,
        "text": "E",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(330)"
      }
    },
    {
      "name": "f4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 3,
        "text": "F",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(349)"
      }
    },
    {
      "name": "g4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 4,
        "text": "G",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(392)"
      }
    },
    {
      "name": "a4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 5,
        "text": "A",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(440)"
      }
    },
    {
      "name": "b4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 6,
        "text": "B",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(494)"
      }
    },
    {
      "name": "c5",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 7,
        "text": "C5",
        "width": 8,
        "padx": 4,
        "pady": 4,
        "action": "play(523)"
      }
    },
    {
      "name": "status",
      "type": "LABEL",
      "options": {
        "text": "Ready",
        "bg": "#1B1D23",
        "fg": "#EEF2F8",
        "font": "Segoe UI 11",
        "padx": 10,
        "pady": 8
      }
    }
  ],
  "bindings": [],
  "functions": {
    "play": {
      "params": [
        "freq"
      ],
      "body": [
        {
          "type": "uiset",
          "widget": "status",
          "expr": "\"Playing \" + str(freq) + \" Hz\""
        },
        {
          "type": "expr",
          "expr": "sound_beep(freq, 120)"
        }
      ]
    }
  },
  "on_start": [],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
