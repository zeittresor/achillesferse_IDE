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
    "title": "Achillesferse Todo List",
    "width": 520,
    "height": 520,
    "bg": "#1D1F24"
  },
  "vars": {},
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "Todo List",
        "bg": "#1D1F24",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "input",
      "type": "ENTRY",
      "options": {
        "width": 34,
        "padx": 10,
        "pady": 6
      }
    },
    {
      "name": "add_btn",
      "type": "BUTTON",
      "options": {
        "text": "Add",
        "width": 10,
        "padx": 10,
        "pady": 4,
        "action": "add_item()"
      }
    },
    {
      "name": "remove_btn",
      "type": "BUTTON",
      "options": {
        "text": "Remove selected",
        "width": 18,
        "padx": 10,
        "pady": 4,
        "action": "remove_item()"
      }
    },
    {
      "name": "tasks",
      "type": "LISTBOX",
      "options": {
        "width": 48,
        "height": 15,
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "hint",
      "type": "LABEL",
      "options": {
        "text": "Type a task, press Enter or click Add.",
        "bg": "#1D1F24",
        "fg": "#C8CDD8",
        "font": "Segoe UI 10",
        "padx": 10,
        "pady": 4
      }
    }
  ],
  "bindings": [
    {
      "widget": "input",
      "event": "<Return>",
      "action": "add_item()"
    }
  ],
  "functions": {
    "add_item": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "value",
          "expr": "text('input').strip()"
        },
        {
          "type": "if",
          "cond": "value == \"\"",
          "then": [
            {
              "type": "return"
            }
          ],
          "elifs": [],
          "else": []
        },
        {
          "type": "append",
          "widget": "tasks",
          "expr": "value"
        },
        {
          "type": "clear",
          "widget": "input"
        },
        {
          "type": "focus",
          "widget": "input"
        }
      ]
    },
    "remove_item": {
      "params": [],
      "body": [
        {
          "type": "expr",
          "expr": "listbox_delete_selected('tasks')"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "focus",
      "widget": "input"
    }
  ],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
