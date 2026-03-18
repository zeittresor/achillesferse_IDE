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
    "title": "Achillesferse Mandelbrot",
    "width": 920,
    "height": 720,
    "bg": "#101114"
  },
  "vars": {
    "center_x": "-0.5",
    "center_y": "0.0",
    "zoom": "1.0",
    "max_iter": "42",
    "info": "\"Arrows move, +/- zoom, R reset\""
  },
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "Mandelbrot Explorer",
        "bg": "#101114",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "status",
      "type": "LABEL",
      "options": {
        "text": "",
        "bg": "#101114",
        "fg": "#D5D9E3",
        "font": "Segoe UI 10",
        "padx": 10,
        "pady": 4
      }
    },
    {
      "name": "view",
      "type": "CANVAS",
      "options": {
        "width": 880,
        "height": 620,
        "bg": "black",
        "padx": 10,
        "pady": 10
      }
    }
  ],
  "bindings": [
    {
      "widget": "view",
      "event": "<Left>",
      "action": "move_left()"
    },
    {
      "widget": "view",
      "event": "<Right>",
      "action": "move_right()"
    },
    {
      "widget": "view",
      "event": "<Up>",
      "action": "move_up()"
    },
    {
      "widget": "view",
      "event": "<Down>",
      "action": "move_down()"
    },
    {
      "widget": "view",
      "event": "<plus>",
      "action": "zoom_in()"
    },
    {
      "widget": "view",
      "event": "<minus>",
      "action": "zoom_out()"
    },
    {
      "widget": "view",
      "event": "<KeyPress-r>",
      "action": "reset_view()"
    },
    {
      "widget": "view",
      "event": "<KeyPress-R>",
      "action": "reset_view()"
    }
  ],
  "functions": {
    "redraw": {
      "params": [],
      "body": [
        {
          "type": "uiset",
          "widget": "status",
          "expr": "info + \" | center=(\" + str(round(center_x, 5)) + \", \" + str(round(center_y, 5)) + \") zoom=\" + str(round(zoom, 3))"
        },
        {
          "type": "expr",
          "expr": "draw_mandelbrot('view', center_x, center_y, zoom, max_iter, 4)"
        }
      ]
    },
    "move_left": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "center_x",
          "expr": "center_x - 0.15 / zoom"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "move_right": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "center_x",
          "expr": "center_x + 0.15 / zoom"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "move_up": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "center_y",
          "expr": "center_y - 0.15 / zoom"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "move_down": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "center_y",
          "expr": "center_y + 0.15 / zoom"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "zoom_in": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "zoom",
          "expr": "zoom * 1.4"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "zoom_out": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "zoom",
          "expr": "max(0.2, zoom / 1.4)"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "reset_view": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "center_x",
          "expr": "-0.5"
        },
        {
          "type": "set",
          "name": "center_y",
          "expr": "0.0"
        },
        {
          "type": "set",
          "name": "zoom",
          "expr": "1.0"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "focus",
      "widget": "view"
    },
    {
      "type": "expr",
      "expr": "redraw()"
    }
  ],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
