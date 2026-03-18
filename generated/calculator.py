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
    "title": "Achillesferse Calculator",
    "width": 360,
    "height": 420,
    "bg": "#202020"
  },
  "vars": {
    "expression": "\"\""
  },
  "widgets": [
    {
      "name": "panel",
      "type": "FRAME",
      "options": {
        "bg": "#202020",
        "padx": 12,
        "pady": 12
      }
    },
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "parent": "panel",
        "row": 0,
        "column": 0,
        "columnspan": 4,
        "text": "Calculator",
        "bg": "#202020",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 4,
        "pady": 4
      }
    },
    {
      "name": "display",
      "type": "ENTRY",
      "options": {
        "parent": "panel",
        "row": 1,
        "column": 0,
        "columnspan": 4,
        "width": 28,
        "padx": 4,
        "pady": 8,
        "readonly": true
      }
    },
    {
      "name": "clear_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 2,
        "column": 0,
        "text": "C",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "clear_all()"
      }
    },
    {
      "name": "back_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 2,
        "column": 1,
        "text": "<-",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "backspace()"
      }
    },
    {
      "name": "div_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 2,
        "column": 2,
        "text": "/",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('/')"
      }
    },
    {
      "name": "mul_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 2,
        "column": 3,
        "text": "*",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('*')"
      }
    },
    {
      "name": "b7",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 3,
        "column": 0,
        "text": 7,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('7')"
      }
    },
    {
      "name": "b8",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 3,
        "column": 1,
        "text": 8,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('8')"
      }
    },
    {
      "name": "b9",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 3,
        "column": 2,
        "text": 9,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('9')"
      }
    },
    {
      "name": "sub_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 3,
        "column": 3,
        "text": "-",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('-')"
      }
    },
    {
      "name": "b4",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 4,
        "column": 0,
        "text": 4,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('4')"
      }
    },
    {
      "name": "b5",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 4,
        "column": 1,
        "text": 5,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('5')"
      }
    },
    {
      "name": "b6",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 4,
        "column": 2,
        "text": 6,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('6')"
      }
    },
    {
      "name": "add_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 4,
        "column": 3,
        "text": "+",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('+')"
      }
    },
    {
      "name": "b1",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 5,
        "column": 0,
        "text": 1,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('1')"
      }
    },
    {
      "name": "b2",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 5,
        "column": 1,
        "text": 2,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('2')"
      }
    },
    {
      "name": "b3",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 5,
        "column": 2,
        "text": 3,
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('3')"
      }
    },
    {
      "name": "eq_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 5,
        "column": 3,
        "rowspan": 2,
        "text": "=",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "calculate()"
      }
    },
    {
      "name": "b0",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 6,
        "column": 0,
        "columnspan": 2,
        "text": 0,
        "width": 14,
        "padx": 4,
        "pady": 4,
        "action": "append_token('0')"
      }
    },
    {
      "name": "dot_btn",
      "type": "BUTTON",
      "options": {
        "parent": "panel",
        "row": 6,
        "column": 2,
        "text": ".",
        "width": 6,
        "padx": 4,
        "pady": 4,
        "action": "append_token('.')"
      }
    }
  ],
  "bindings": [],
  "functions": {
    "refresh_display": {
      "params": [],
      "body": [
        {
          "type": "uiset",
          "widget": "display",
          "expr": "expression"
        }
      ]
    },
    "append_token": {
      "params": [
        "token"
      ],
      "body": [
        {
          "type": "set",
          "name": "expression",
          "expr": "expression + str(token)"
        },
        {
          "type": "expr",
          "expr": "refresh_display()"
        },
        {
          "type": "expr",
          "expr": "sound_beep(1000, 35)"
        }
      ]
    },
    "clear_all": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "expression",
          "expr": "\"\""
        },
        {
          "type": "expr",
          "expr": "refresh_display()"
        }
      ]
    },
    "backspace": {
      "params": [],
      "body": [
        {
          "type": "if",
          "cond": "len(expression) > 0",
          "then": [
            {
              "type": "set",
              "name": "expression",
              "expr": "expression[:-1]"
            },
            {
              "type": "expr",
              "expr": "refresh_display()"
            }
          ],
          "elifs": [],
          "else": []
        }
      ]
    },
    "calculate": {
      "params": [],
      "body": [
        {
          "type": "if",
          "cond": "expression == \"\"",
          "then": [
            {
              "type": "return"
            }
          ],
          "elifs": [],
          "else": []
        },
        {
          "type": "set",
          "name": "expression",
          "expr": "calculate_expression(expression)"
        },
        {
          "type": "expr",
          "expr": "refresh_display()"
        },
        {
          "type": "expr",
          "expr": "sound_beep(1300, 55)"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "expr",
      "expr": "refresh_display()"
    }
  ],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
