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
    "title": "Achillesferse Starfield",
    "width": 900,
    "height": 620,
    "bg": "black"
  },
  "vars": {
    "stars": "[]",
    "star_count": "180",
    "speed": "18"
  },
  "widgets": [
    {
      "name": "headline",
      "type": "LABEL",
      "options": {
        "text": "Starfield Simulator (Achillesferse)",
        "bg": "black",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 10
      }
    },
    {
      "name": "scene",
      "type": "CANVAS",
      "options": {
        "width": 860,
        "height": 520,
        "bg": "black",
        "padx": 12,
        "pady": 12
      }
    }
  ],
  "bindings": [],
  "functions": {},
  "on_start": [
    {
      "type": "set",
      "name": "stars",
      "expr": "init_starfield(star_count, 860, 520)"
    },
    {
      "type": "expr",
      "expr": "draw_starfield('scene', stars)"
    }
  ],
  "on_tick": {
    "ms": 33,
    "body": [
      {
        "type": "set",
        "name": "stars",
        "expr": "step_starfield(stars, speed, 860, 520)"
      },
      {
        "type": "expr",
        "expr": "draw_starfield('scene', stars)"
      }
    ]
  }
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
