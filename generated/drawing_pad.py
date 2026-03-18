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
    "title": "Achillesferse Drawing Pad",
    "width": 960,
    "height": 700,
    "bg": "#1A1C22"
  },
  "vars": {
    "brush_color": "\"#FFFFFF\""
  },
  "widgets": [
    {
      "name": "header",
      "type": "LABEL",
      "options": {
        "text": "Drawing Pad",
        "bg": "#1A1C22",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "toolbar",
      "type": "FRAME",
      "options": {
        "bg": "#1A1C22",
        "padx": 10,
        "pady": 6
      }
    },
    {
      "name": "clear_btn",
      "type": "BUTTON",
      "options": {
        "parent": "toolbar",
        "text": "Clear",
        "padx": 8,
        "pady": 4,
        "action": "clear_all()"
      }
    },
    {
      "name": "white_btn",
      "type": "BUTTON",
      "options": {
        "parent": "toolbar",
        "text": "White",
        "padx": 8,
        "pady": 4,
        "action": "set_color('#FFFFFF')"
      }
    },
    {
      "name": "cyan_btn",
      "type": "BUTTON",
      "options": {
        "parent": "toolbar",
        "text": "Cyan",
        "padx": 8,
        "pady": 4,
        "action": "set_color('#66FCF1')"
      }
    },
    {
      "name": "pink_btn",
      "type": "BUTTON",
      "options": {
        "parent": "toolbar",
        "text": "Pink",
        "padx": 8,
        "pady": 4,
        "action": "set_color('#FF79C6')"
      }
    },
    {
      "name": "gold_btn",
      "type": "BUTTON",
      "options": {
        "parent": "toolbar",
        "text": "Gold",
        "padx": 8,
        "pady": 4,
        "action": "set_color('#FFD166')"
      }
    },
    {
      "name": "info",
      "type": "LABEL",
      "options": {
        "text": "Hold left mouse button and draw on the canvas.",
        "bg": "#1A1C22",
        "fg": "#CDD2DD",
        "font": "Segoe UI 10",
        "padx": 10,
        "pady": 4
      }
    },
    {
      "name": "pad",
      "type": "CANVAS",
      "options": {
        "width": 920,
        "height": 560,
        "bg": "#0B0D10",
        "padx": 12,
        "pady": 12
      }
    }
  ],
  "bindings": [
    {
      "widget": "pad",
      "event": "<B1-Motion>",
      "action": "paint()"
    }
  ],
  "functions": {
    "paint": {
      "params": [],
      "body": [
        {
          "type": "expr",
          "expr": "canvas_oval('pad', event_x()-3, event_y()-3, event_x()+3, event_y()+3, fill=brush_color, outline='')"
        }
      ]
    },
    "clear_all": {
      "params": [],
      "body": [
        {
          "type": "expr",
          "expr": "canvas_clear('pad')"
        }
      ]
    },
    "set_color": {
      "params": [
        "new_color"
      ],
      "body": [
        {
          "type": "set",
          "name": "brush_color",
          "expr": "str(new_color)"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "focus",
      "widget": "pad"
    }
  ],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
