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
    "title": "Achillesferse Breakout",
    "width": 920,
    "height": 690,
    "bg": "#0F1115"
  },
  "vars": {
    "game": "{}",
    "paddle_speed": "24"
  },
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "Breakout",
        "bg": "#0F1115",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "hint",
      "type": "LABEL",
      "options": {
        "text": "Left/Right move, R restarts",
        "bg": "#0F1115",
        "fg": "#CDD2DD",
        "font": "Segoe UI 10",
        "padx": 10,
        "pady": 4
      }
    },
    {
      "name": "scene",
      "type": "CANVAS",
      "options": {
        "width": 880,
        "height": 600,
        "bg": "#10131A",
        "padx": 10,
        "pady": 10
      }
    }
  ],
  "bindings": [
    {
      "widget": "scene",
      "event": "<Left>",
      "action": "move_left()"
    },
    {
      "widget": "scene",
      "event": "<Right>",
      "action": "move_right()"
    },
    {
      "widget": "scene",
      "event": "<KeyPress-r>",
      "action": "restart_game()"
    },
    {
      "widget": "scene",
      "event": "<KeyPress-R>",
      "action": "restart_game()"
    }
  ],
  "functions": {
    "redraw": {
      "params": [],
      "body": [
        {
          "type": "expr",
          "expr": "breakout_draw('scene', game)"
        }
      ]
    },
    "move_left": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "game",
          "expr": "breakout_move_paddle(game, -paddle_speed, 880)"
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
          "name": "game",
          "expr": "breakout_move_paddle(game, paddle_speed, 880)"
        },
        {
          "type": "expr",
          "expr": "redraw()"
        }
      ]
    },
    "restart_game": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "game",
          "expr": "breakout_new(880, 600, 5, 9)"
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
      "type": "set",
      "name": "game",
      "expr": "breakout_new(880, 600, 5, 9)"
    },
    {
      "type": "focus",
      "widget": "scene"
    },
    {
      "type": "expr",
      "expr": "redraw()"
    }
  ],
  "on_tick": {
    "ms": 16,
    "body": [
      {
        "type": "set",
        "name": "game",
        "expr": "breakout_step(game, 880, 600)"
      },
      {
        "type": "expr",
        "expr": "redraw()"
      }
    ]
  }
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
