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
    "title": "Achillesferse ELIZA",
    "width": 760,
    "height": 540,
    "bg": "#1d1f21"
  },
  "vars": {},
  "widgets": [
    {
      "name": "title",
      "type": "LABEL",
      "options": {
        "text": "ELIZA Chatbot",
        "bg": "#1d1f21",
        "fg": "white",
        "font": "Segoe UI 14",
        "padx": 10,
        "pady": 8
      }
    },
    {
      "name": "conversation",
      "type": "TEXT",
      "options": {
        "width": 86,
        "height": 22,
        "padx": 10,
        "pady": 6
      }
    },
    {
      "name": "user_input",
      "type": "ENTRY",
      "options": {
        "width": 68,
        "padx": 10,
        "pady": 6
      }
    },
    {
      "name": "send_btn",
      "type": "BUTTON",
      "options": {
        "text": "Send",
        "width": 10,
        "padx": 10,
        "pady": 6,
        "action": "send()"
      }
    }
  ],
  "bindings": [
    {
      "widget": "user_input",
      "event": "<Return>",
      "action": "send()"
    }
  ],
  "functions": {
    "send": {
      "params": [],
      "body": [
        {
          "type": "set",
          "name": "user_message",
          "expr": "text('user_input').strip()"
        },
        {
          "type": "if",
          "cond": "user_message == \"\"",
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
          "widget": "conversation",
          "expr": "\"You: \" + user_message + \"\\n\""
        },
        {
          "type": "set",
          "name": "bot_message",
          "expr": "eliza_reply(user_message)"
        },
        {
          "type": "append",
          "widget": "conversation",
          "expr": "\"Eliza: \" + bot_message + \"\\n\\n\""
        },
        {
          "type": "clear",
          "widget": "user_input"
        },
        {
          "type": "focus",
          "widget": "user_input"
        }
      ]
    }
  },
  "on_start": [
    {
      "type": "append",
      "widget": "conversation",
      "expr": "\"Eliza: Hello. How are you feeling today?\\n\\n\""
    },
    {
      "type": "focus",
      "widget": "user_input"
    }
  ],
  "on_tick": null
}""")

if __name__ == "__main__":
    AchillesferseApp(PROGRAM).run()
